import re
import threading
import time

import psycopg2
from psycopg2 import sql, pool
from ..common.out import nprint
from .dstatus import Commit_Status, Sql_Status, Isolation_Status
from typing import Union, List, Tuple, Any,Optional

__all__ = ["n_postgresql"]

'''
    PostgreSQL操作库(同步)
    支持连接池/直接使用
    连接池拥有健康状况查询线程(未实现线程安全),需手动开启
'''

class n_postgresql:
    _connection_pool: Optional[pool.SimpleConnectionPool] = None
    _healthcheck_thread: Optional[threading.Thread] = None
    _healthcheck_running = False
    debug = False

    @classmethod
    def set_pool_debug(cls, debug: bool) -> None:
        """
        设置连接池调试模式（类级别）

        Args:
            debug: 是否启用调试输出
        """
        cls.debug = debug
        if cls.debug:
            nprint(f"已启用连接池调试模式 (cls.debug = {cls.debug})")

    def set_connect_debug(self,debug:bool) -> None:
        self.debug = debug
        if self.debug:
            nprint('已启用connect-debug')

    @classmethod
    def initialize_pool(cls, minconn: int = 1, maxconn: int = 10, **kwargs):
        """初始化连接池"""
        if cls._connection_pool is not None:
            cls.close_pool()

        # 从 kwargs 中提取并设置 debug 状态（默认为 False）
        cls.debug = kwargs.pop('debug', False)

        # 确保必要参数存在
        required_params = ['host', 'user', 'password']
        if not all(param in kwargs for param in required_params):
            if cls.debug:
                nprint("缺少必要的连接参数 (host, user, password)")
            raise ValueError("Missing required connection parameters (host, user, password)")

        # 设置默认值
        kwargs.setdefault('port', 5432)

        # 转换 charset 为 client_encoding
        if 'charset' in kwargs:
            kwargs['client_encoding'] = kwargs.pop('charset')

        # 保存连接参数（包含 debug 状态）用于自动重连
        cls._connection_params = {
            'minconn': minconn,
            'maxconn': maxconn,
            'debug': cls.debug,  # 持久化 debug 状态
            **kwargs
        }

        try:
            if cls.debug:
                nprint(f"正在初始化连接池，参数: {kwargs}")

            cls._connection_pool = pool.SimpleConnectionPool(
                minconn=minconn,
                maxconn=maxconn,
                **kwargs
            )

            if cls.debug:
                nprint("连接池初始化成功")

        except psycopg2.Error as e:
            if cls.debug:
                nprint(f"连接池初始化失败: {e}")
            raise

    @classmethod
    def start_healthcheckthread(cls, interval: float = 15.0):
        """启动连接池健康检查线程"""
        if cls._healthcheck_thread is not None and cls._healthcheck_thread.is_alive():
            if cls.debug:
                nprint("健康检查线程已在运行")
            return

        cls._healthcheck_running = True

        def healthcheck_loop():
            while cls._healthcheck_running:
                try:
                    if cls._connection_pool is not None:
                        try:
                            conn = cls._connection_pool.getconn()
                            cursor = conn.cursor()
                            cursor.execute("SELECT 1")
                            cursor.close()
                            cls._connection_pool.putconn(conn)
                            if cls.debug:
                                nprint("连接池健康检查通过")
                        except Exception as e:
                            if cls.debug:
                                nprint(f"连接池健康检查失败: {e}")
                            # 尝试重置连接池
                            try:
                                cls.close_pool()
                                # 自动重连逻辑
                                if hasattr(cls, '_connection_params'):
                                    cls.initialize_pool(**cls._connection_params)
                                    if cls.debug:
                                        nprint("连接池已自动重新初始化")
                            except Exception as reconn_e:
                                if cls.debug:
                                    nprint(f"连接池自动重连失败: {reconn_e}")
                    else:
                        if cls.debug:
                            nprint("连接池未初始化")
                        # 自动重连逻辑
                        if hasattr(cls, '_connection_params'):
                            try:
                                cls.initialize_pool(**cls._connection_params)
                                if cls.debug:
                                    nprint("连接池已自动初始化")
                            except Exception as init_e:
                                if cls.debug:
                                    nprint(f"连接池自动初始化失败: {init_e}")
                except Exception as outer_e:
                    if cls.debug:
                        nprint(f"健康检查线程发生未捕获错误: {outer_e}")
                time.sleep(interval)

        cls._healthcheck_thread = threading.Thread(
            target=healthcheck_loop,
            daemon=True,
            name="PGConnectionPoolHealthCheck"
        )
        cls._healthcheck_thread.start()

    @classmethod
    def stop_healthcheckthread(cls):
        """停止连接池健康检查线程"""
        cls._healthcheck_running = False
        if cls._healthcheck_thread is not None:
            cls._healthcheck_thread.join(timeout=2)
            if cls.debug:
                nprint("连接池健康检查线程已停止")
        cls._healthcheck_thread = None

    @classmethod
    def close_pool(cls):
        """关闭连接池"""
        if cls._connection_pool is not None:
            try:
                cls._connection_pool.closeall()
            except Exception as e:
                if hasattr(cls, 'debug') and cls.debug:
                    nprint(f"关闭连接池时出错: {e}")
            finally:
                cls._connection_pool = None

    def __init__(self,
                 host: Union[str, None] = None,
                 port: Union[int, None] = None,
                 user: Union[str, None] = None,
                 password: Union[str, None] = None,
                 charset: str = 'utf8',
                 debug: bool = False,
                 use_pool: bool = False):  # 添加这个参数
        self.host = host
        self.port = port or 5432
        self.user = user
        self.password = password
        self.charset = charset
        self.connection: Union[psycopg2.extensions.connection, None] = None
        self.debug = debug
        self.use_pool = use_pool  # 添加这个属性
        self._using_pool_connection = False
        self._current_db: Optional[str] = None

    @classmethod
    def getInstance(cls,
                    connect: Union[psycopg2.extensions.connection, None] = None,
                    *,
                    host: str = None,
                    port: int = None,
                    user: str = None,
                    password: str = None,
                    charset: str = 'utf8',
                    debug: bool = False) -> 'n_postgresql | None':
        if connect is not None:
            return cls(connect.host, connect.port, connect.user,
                       connect.password, connect.encoding, debug)  # 使用传入的debug参数
        if host and port and user and password:
            return cls(host, port, user, password, charset, debug)
        else:
            return None

    def connect_server(self, commit_status: Commit_Status = Commit_Status.auto_commit):
        """连接到服务器"""
        try:
            if self.use_pool and self._connection_pool is not None:
                self.connection = self._connection_pool.getconn()
                self._using_pool_connection = True
                if self.debug:
                    nprint("从连接池获取数据库连接")
            else:
                # 构建连接参数
                conn_params = {
                    'host': self.host,
                    'port': self.port,
                    'user': self.user,
                    'password': self.password,
                    'client_encoding': self.charset,
                    'connect_timeout': 10
                }
                # 如果有当前数据库，添加到连接参数
                if self._current_db:
                    conn_params['dbname'] = self._current_db
                self.connection = psycopg2.connect(**conn_params)
                self._using_pool_connection = False
                if self.debug:
                    nprint("创建新的直接数据库连接")
            # 设置自动提交模式
            self.connection.autocommit = bool(commit_status.value)
        except psycopg2.Error as e:
            if self.debug:
                nprint(f"PostgreSQL数据库连接失败: {e}")
            raise

    def setup(self, db_name: str, is_start_transaction: bool = False) -> None:
        self.use_database(db_name)
        if is_start_transaction:
            self.startTransAction()

    def use_database(self, db_name: str) -> None:
        """使用指定数据库"""
        if not db_name:
            raise ValueError("Database name cannot be empty")
        # 更新当前数据库
        self._current_db = db_name
        try:
            # 检查数据库是否存在
            if not self.exists_db(db_name):
                self.create_database(db_name)
                if self.__class__.debug:
                    nprint(f"数据库 {db_name} 不存在，已创建")
            # 关闭当前连接
            self._safe_disconnect()
            if self.use_pool and self._connection_pool is not None:
                # 连接池模式下的处理
                self.close_pool()
                self.initialize_pool(
                    minconn=1,
                    maxconn=10,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    dbname=db_name,
                    client_encoding=self.charset,
                    debug=self.__class__.debug
                )
            # 重新连接（无论是否使用连接池）
            self.connect_server()
        except psycopg2.Error as e:
            if self.__class__.debug:
                nprint(f"切换数据库失败: {e}")
            raise

    def exec_cmd(self, cmd: str) -> Union[str, List[Tuple[Any, ...]], None]:
        """执行 PostgreSQL/MySQL 兼容命令，支持 psql 元命令和 MySQL 语法"""
        cursor = None
        try:
            cmd = cmd.strip()
            # ===== 0. 去除命令末尾的分号(如果有) =====
            if cmd.endswith(';'):
                cmd = cmd[:-1].strip()
            # ===== 1. 处理 psql 元命令（\ 开头）=====
            if cmd.startswith("\\"):
                return self._handle_psql_meta_command(cmd)
            # ===== 2. 处理 MySQL 命令 =====
            cmd_lower = cmd.lower()

            # USE <dbname>（切换数据库）
            if cmd_lower.startswith("use "):
                new_db = cmd.split()[1]
                self.connection.close()
                self.connection = psycopg2.connect(
                    dbname=new_db,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                return f"Database changed to: {new_db}"

            # DESCRIBE <table> 或 DESC <table>
            elif cmd_lower.startswith("describe ") or cmd_lower.startswith("desc "):
                table_name = re.sub(r"(describe|desc)\s+", "", cmd_lower, flags=re.IGNORECASE)
                cursor = self.connection.cursor()
                cursor.execute("""
                    SELECT 
                        column_name as "Field",
                        data_type as "Type",
                        is_nullable as "Null",
                        column_default as "Default",
                        '' as "Extra"
                    FROM information_schema.columns 
                    WHERE table_name = %s
                    ORDER BY ordinal_position
                """, (table_name,))
                return cursor.fetchall()

            # SHOW 命令
            elif cmd_lower.startswith("show "):
                return self._handle_mysql_show_command(cmd)

            # ===== 3. 默认情况：执行普通 SQL =====
            else:
                cursor = self.connection.cursor()
                cursor.execute(cmd)
                # 尝试获取结果（如果是 SELECT 或返回数据的命令）
                try:
                    result = cursor.fetchall()
                    return result if result else None
                except psycopg2.ProgrammingError:
                    return None  # 无返回结果（如 INSERT/UPDATE/DELETE）
        except Exception as e:
            if self.debug:
                print("执行数据库命令发生错误:", e)
            raise
        finally:
            if cursor is not None:
                cursor.close()

    def exec_language(
            self,
            sql_language: str,
            params=None,  # 新增参数，用于参数化查询
            fetch=None
    ) -> Union[Tuple[Tuple[Any, ...], ...], None]:
        """
        执行SQL语句

        Args:
            sql_language: SQL语句字符串
            params: 可选的参数元组/字典，用于参数化查询
            fetch: 是否获取结果集
                如果为None，则自动判断（SELECT/WITH/RETURNING语句自动fetch）
                如果为True/False，则强制指定是否fetch

        Returns:
            查询结果集（如果是查询语句）或None
        """
        if sql_language is None:
            nprint('sql_language = null')
            return ()

        lg = sql_language.replace("None", "NULL")
        cursor = None

        try:
            cursor = self.connection.cursor()

            # 修改这里：支持参数化查询
            if params is not None:
                cursor.execute(lg, params)
            else:
                cursor.execute(lg)

            # 自动判断是否需要 fetch
            if fetch is None:
                fetch = lg.strip().lower().startswith(("select", "with", "returning"))

            if fetch:
                result = cursor.fetchall()
                return result

            self.connection.commit()  # 非查询命令需要提交
            return None

        except psycopg2.Error:
            if self.debug:
                nprint("执行sql语句发生数据库错误: " + lg)
            raise
        except psycopg2.ProgrammingError as e:
            if fetch and "no results to fetch" in str(e):
                return ()  # 对于不返回结果的命令返回空元组
            if self.debug:
                nprint("数据库操作错误: " + e.__str__())
            raise
        finally:
            if cursor is not None:
                cursor.close()

    @property
    def isolation(self) -> Union[Isolation_Status, None]:
        """
        获取当前事务的隔离级别

        Returns:
            str: 当前事务隔离级别，可能的值为:
                - "read uncommitted" (PostgreSQL实际上不支持)
                - "read committed"
                - "repeatable read"
                - "serializable"
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW transaction_isolation")
            isolation_level = cursor.fetchone()[0]

            # 标准化返回的隔离级别字符串
            isolation_level = isolation_level.lower().strip()

            # PostgreSQL 实际上不支持 "read uncommitted"，但为了完整性我们还是处理它
            if isolation_level == "read uncommitted":
                return Isolation_Status.read_uncommitted
            elif isolation_level == "read committed":
                return Isolation_Status.read_committed
            elif isolation_level == "repeatable read":
                return Isolation_Status.repeatable_read
            elif isolation_level == "serializable":
                return Isolation_Status.serializable
            else:
                if self.debug:
                    nprint(f"未知的事务隔离级别: {isolation_level}")
                return None

        except psycopg2.Error as e:
            if self.debug:
                nprint(f"获取事务隔离级别失败: {e}")
            raise
        finally:
            if cursor is not None:
                cursor.close()

    @isolation.setter
    def isolation(self, iso_status: Isolation_Status):
        """
        设置事务隔离级别

        Args:
            iso_status: 要设置的隔离级别枚举值

        Raises:
            psycopg2.Error: 如果设置失败
            ValueError: 如果传入无效的隔离级别或连接不可用
        """
        if self.connection is None or self.connection.closed:
            raise ValueError("数据库连接不可用")

        if not isinstance(iso_status, Isolation_Status):
            raise ValueError("必须提供 isolation_status 枚举值")

        # 将枚举值映射到PostgreSQL的隔离级别字符串
        isolation_mapping = {
            Isolation_Status.read_uncommitted: "READ UNCOMMITTED",
            Isolation_Status.read_committed: "READ COMMITTED",
            Isolation_Status.repeatable_read: "REPEATABLE READ",
            Isolation_Status.serializable: "SERIALIZABLE"
        }

        cursor = None
        try:
            cursor = self.connection.cursor()
            isolation_level = isolation_mapping[iso_status]

            if iso_status == Isolation_Status.read_uncommitted and self.debug:
                nprint("警告: PostgreSQL实际上不支持READ UNCOMMITTED隔离级别，将自动转为READ COMMITTED")

            cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")

            if self.debug:
                nprint(f"事务隔离级别已设置为: {isolation_level}")

        except KeyError:
            raise ValueError(f"不支持的隔离级别: {iso_status}")
        except psycopg2.Error as e:
            if self.debug:
                nprint(f"设置事务隔离级别失败: {e}")
            raise
        finally:
            if cursor is not None:
                cursor.close()

    def quick_select(self, name: str, limit: Union[int, None] = None) -> Union[list, None]:
        """
        快速查询表或视图的内容

        Args:
            name: 表名或视图名
            limit: 可选，限制返回的记录数。如果为None，则返回所有记录

        Returns:
            查询结果列表，每个元素是一个元组表示一行记录；如果查询失败返回None

        Raises:
            psycopg2.Error: 如果查询过程中发生数据库错误
        """
        cursor = None
        try:
            # 检查表或视图是否存在
            if not (self.exists_table(name) or self.exists_view(name)):
                if self.debug:
                    nprint(f"表或视图 '{name}' 不存在")
                return None

            # 构建SQL查询
            query = sql.SQL("SELECT * FROM {}").format(
                sql.Identifier(name)
            )

            # 添加LIMIT子句
            if limit is not None and limit > 0:
                query = sql.SQL("{} LIMIT {}").format(
                    query,
                    sql.Literal(limit)
                )

            if self.debug:
                nprint(f"执行查询: {query.as_string(self.connection)}")

            # 执行查询
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            return result

        except psycopg2.Error as e:
            if self.debug:
                nprint(f"快速查询失败: {e}")
            raise
        finally:
            if cursor is not None:
                cursor.close()

    def _handle_psql_meta_command(self, cmd: str) -> Union[str, List[Tuple[Any, ...]], None]:
        """处理 psql 元命令（\dt, \c, \d 等）"""
        cursor = self.connection.cursor()

        # \dt 或 \dt+（列出表）
        if cmd in ("\\dt", "\\dt+"):
            cursor.execute("""
                SELECT table_name, table_type 
                FROM information_schema.tables 
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            """)
            return cursor.fetchall()

        # \l 或 \list（列出数据库）
        elif cmd in ("\\l", "\\list"):
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
            return cursor.fetchall()

        # \c <dbname>（切换数据库）
        elif cmd.startswith("\\c "):
            new_db = cmd.split()[1]
            self.connection.close()
            self.connection = psycopg2.connect(
                dbname=new_db,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return f"Switched to database: {new_db}"

        # \d <table>（描述表结构）
        elif cmd.startswith("\\d "):
            table_name = cmd.split()[1]
            cursor.execute("""
                SELECT 
                    column_name, data_type, 
                    is_nullable, column_default 
                FROM information_schema.columns 
                WHERE table_name = %s
            """, (table_name,))
            return cursor.fetchall()

        # \du（列出用户/角色）
        elif cmd == "\\du":
            cursor.execute("SELECT rolname, rolcanlogin FROM pg_roles")
            return cursor.fetchall()

        # \dn（列出 schema）
        elif cmd == "\\dn":
            cursor.execute("SELECT nspname FROM pg_namespace")
            return cursor.fetchall()

        # \df（列出函数）
        elif cmd == "\\df":
            cursor.execute("""
                SELECT routine_name, routine_type 
                FROM information_schema.routines 
                WHERE routine_schema NOT IN ('pg_catalog', 'information_schema')
            """)
            return cursor.fetchall()

        # 其他未识别的 \ 命令
        else:
            return f"Unsupported psql meta-command: {cmd}"

    def _handle_mysql_show_command(self, cmd: str) -> Union[str, List[Tuple[Any, ...]], None]:
        """处理 MySQL SHOW 命令（转换为 PostgreSQL 查询）"""
        cmd_lower = cmd.lower()
        cursor = self.connection.cursor()
        # 新增的
        if cmd_lower == "show transaction_isolation" or cmd_lower == "show transaction_isolation;":
            cursor.execute("SHOW transaction_isolation")
            return cursor.fetchone()
        elif cmd_lower == "" or cmd_lower == ";":
            cursor.execute("")
            return cursor.fetchone()
        # SHOW TABLES → PostgreSQL 查询
        elif cmd_lower == "show tables" or cmd_lower == "show tables;":
            cursor.execute("""
                SELECT table_name as "Tables_in_<database>"
                FROM information_schema.tables 
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            """)
            return cursor.fetchall()
        # SHOW DATABASES → PostgreSQL 查询
        elif cmd_lower == "show databases" or cmd_lower == "show databases;":
            cursor.execute("SELECT datname as Database FROM pg_database WHERE datistemplate = false")
            return cursor.fetchall()
        # SHOW COLUMNS FROM <table> → PostgreSQL 查询
        elif cmd_lower.startswith("show columns from "):
            table_name = re.sub(r"show columns from ", "", cmd_lower, flags=re.IGNORECASE)
            cursor.execute("""
                SELECT 
                    column_name as "Field",
                    data_type as "Type",
                    is_nullable as "Null",
                    column_default as "Default",
                    '' as "Extra"
                FROM information_schema.columns 
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, (table_name,))
            return cursor.fetchall()
        # SHOW CREATE TABLE <table> → PostgreSQL 查询
        elif cmd_lower.startswith("show create table "):
            table_name = re.sub(r"show create table ", "", cmd_lower, flags=re.IGNORECASE)
            cursor.execute("""
                SELECT pg_get_tabledef(%s) as "Create Table"
            """, (table_name,))
            return cursor.fetchone()
        # SHOW INDEX FROM <table>
        elif cmd_lower.startswith("show index from "):
            table_name = re.sub(r"show index from ", "", cmd_lower, flags=re.IGNORECASE)
            cursor.execute("""
                SELECT
                    indexname as "Key_name",
                    indexdef as "Index_type"
                FROM pg_indexes
                WHERE tablename = %s
            """, (table_name,))
            return cursor.fetchall()
        # SHOW TABLE STATUS
        elif cmd_lower == "show table status" or cmd_lower == "show table status;":
            cursor.execute("""
                SELECT 
                    table_name as "Name",
                    'InnoDB' as "Engine",
                    0 as "Version",
                    'Dynamic' as "Row_format",
                    0 as "Rows",
                    0 as "Avg_row_length",
                    0 as "Data_length",
                    0 as "Max_data_length",
                    0 as "Index_length",
                    0 as "Data_free",
                    NULL as "Auto_increment",
                    NULL as "Create_time",
                    NULL as "Update_time",
                    NULL as "Check_time",
                    'utf8_general_ci' as "Collation",
                    NULL as "Checksum",
                    '' as "Create_options",
                    '' as "Comment"
                FROM information_schema.tables
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            """)
            return cursor.fetchall()
        # 其他未识别的 SHOW 命令
        else:
            return f"Unsupported MySQL SHOW command: {cmd}"

    @property
    def commit_status(self) -> Commit_Status:
        """获取当前提交模式（只读属性）"""
        if self.connection is None:
            raise RuntimeError("Database connection is not established")
        return Commit_Status.auto_commit if self.connection.autocommit else Commit_Status.manual_commit

    @commit_status.setter
    def commit_status(self, status: Commit_Status):
        """设置提交模式（可写属性）"""
        if self.connection is None:
            raise RuntimeError("Database connection is not established")

        before = self.connection.autocommit
        self.connection.autocommit = bool(status.value)

        if self.debug:
            old_mode = '自动' if before else '手动'
            new_mode = '自动' if self.connection.autocommit else '手动'
            nprint(f"提交模式从'{old_mode}'改为'{new_mode}'")

    @property
    def current_db(self) -> Union[str, None]:
        """获取当前连接的数据库名"""
        if self.connection is None or self.connection.closed:
            return self._current_db  # 返回缓存的数据库名

        try:
            if self.use_pool and self._connection_pool is not None:
                # 连接池模式下从连接信息获取
                return self.connection.info.dbname
            else:
                # 直接连接模式下返回缓存的数据库名
                return self._current_db
        except Exception as e:
            if self.debug:
                nprint(f"获取当前数据库名失败: {e}")
            return self._current_db  # 出错时返回缓存值

    @current_db.setter
    def current_db(self, db_name: str):
        """切换当前数据库"""
        if not db_name:
            raise ValueError("Database name cannot be empty")
        # 检查是否已经是当前数据库
        current = self.current_db
        if current and current.lower() == db_name.lower():
            if self.__class__.debug:
                nprint(f"已经是数据库 {db_name}，无需切换")
            return
        try:
            # 检查数据库是否存在
            if not self.exists_db(db_name):
                raise ValueError(f"Database '{db_name}' does not exist")
            # 关闭当前连接
            self._safe_disconnect()
            # 更新当前数据库跟踪
            self._current_db = db_name
            if self.use_pool and self._connection_pool is not None:
                # 连接池模式下的处理
                self.close_pool()
                self.initialize_pool(
                    minconn=1,
                    maxconn=10,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    dbname=db_name,
                    client_encoding=self.charset,
                    debug=self.__class__.debug
                )
            else:
                # 直接连接模式下的处理 - 只需更新_current_db，下次connect_server会自动使用
                pass
            # 重新连接
            self.connect_server()
            if self.__class__.debug:
                nprint(f"已切换到数据库: {db_name}")
        except psycopg2.Error as e:
            if self.__class__.debug:
                nprint(f"切换数据库失败: {e}")
            raise

    def startTransAction(self) -> None:
        self.exec_cmd("BEGIN")

    def commit(self) -> None:
        self.exec_cmd("COMMIT")

    def rollback(self) -> None:
        self.exec_cmd("ROLLBACK")

    @property
    def connect_status(self) -> Sql_Status:
        if self.connection is None:
            return Sql_Status.unconnected
        try:
            self.connection.cursor().execute("SELECT 1")
            return Sql_Status.connected
        except psycopg2.Error:
            return Sql_Status.disconnected

    def exists_db(self, database_name: str) -> bool:
        cursor = self.connection.cursor()
        query = "SELECT datname FROM pg_database WHERE datname = %s"
        cursor.execute(query, (database_name,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def create_database(self, database_name: str) -> None:
        """
        创建新数据库（PostgreSQL 专用）

        注意：此操作不能在事务块中执行，会临时切换到自动提交模式

        Args:
            database_name: 要创建的数据库名称
        """
        original_autocommit = self.connection.autocommit
        cursor = None
        try:
            # 临时启用自动提交模式
            self.connection.autocommit = True

            cursor = self.connection.cursor()
            # 使用 psycopg2 的 sql 模块安全地构建查询
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(database_name)
                )
            )

            if self.debug:
                nprint(f"数据库 {database_name} 创建成功")
        except psycopg2.Error as e:
            if self.debug:
                nprint(f"创建数据库失败: {e}")
            raise
        finally:
            # 恢复原来的自动提交设置
            self.connection.autocommit = original_autocommit
            if cursor is not None:
                cursor.close()

    def exists_table(self, tb_name: str, schema: str = "public") -> bool:
        """
        检查表是否存在（PostgreSQL 专用）

        Args:
            tb_name: 表名（自动转为小写比较）
            schema: 模式名，默认为 'public'

        Returns:
            bool: 表是否存在
        """
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = %s
                AND LOWER(table_name) = LOWER(%s)
            )
            """
            cursor.execute(query, (schema, tb_name))
            return cursor.fetchone()[0]
        except psycopg2.Error as e:
            if self.debug:
                nprint(f"查询表是否存在时发生错误: {e}")
            return False
        finally:
            cursor.close()

    def showDatabases(self) -> list[str]:
        """列出所有数据库"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
            return [row[0] for row in cursor.fetchall()]
        except psycopg2.Error as e:
            if self.debug:
                nprint(f"获取数据库列表失败: {e}")
            raise
        finally:
            if cursor is not None:
                cursor.close()

    def showViews(self) -> list[str]:
        """列出当前数据库中的所有视图"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.views 
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            """)
            return [row[0] for row in cursor.fetchall()]
        except psycopg2.Error as e:
            if self.debug:
                nprint(f"获取视图列表失败: {e}")
            raise
        finally:
            if cursor is not None:
                cursor.close()

    def showTables(self) -> list[str]:
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            result = cursor.fetchall()
            table_names = [row[0] for row in result]
            return table_names
        except Exception as e:
            if self.debug:
                nprint("查询表失败:", e)
            raise
        finally:
            if cursor is not None:
                cursor.close()

    def exists_view(self, view_name: str, schema: str = "public") -> bool:
        """
        检查视图是否存在（PostgreSQL 专用）

        Args:
            view_name: 视图名称（自动转为小写比较）
            schema: 模式名，默认为 'public'

        Returns:
            bool: 视图是否存在

        Example:
            >>> db.exists_view("student_view")
            >>> db.exists_view("report_view", schema="analytics")
        """
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.views 
                WHERE table_schema = %s
                AND LOWER(table_name) = LOWER(%s)
            )
            """
            cursor.execute(query, (schema, view_name))
            return cursor.fetchone()[0]
        except psycopg2.Error as e:  # 明确捕获 PostgreSQL 错误
            if self.debug:
                nprint(f"查询视图是否存在时发生错误: {e}")
            return False
        finally:
            cursor.close()

    def drop_table(self, tb_name: str):
        safe_sql = sql.SQL("DROP TABLE IF EXISTS {}").format(
            sql.Identifier(tb_name)  # 自动转义标识符
        )
        self.exec_cmd(safe_sql)

    def drop_database(self, db_name: str) -> None:
        """删除数据库"""
        # 需要确保没有活动连接才能删除数据库
        try:
            # 先断开当前连接（如果连接到要删除的数据库）
            if (self.connection is not None and
                    self.connection.info.dbname == db_name):
                self._safe_disconnect()

            # 创建新连接到template1数据库来执行删除命令
            temp_conn = None
            from_pool = False  # 标记连接是否来自连接池

            try:
                if self.use_pool and self._connection_pool is not None:
                    # 尝试从连接池获取连接
                    temp_conn = self._connection_pool.getconn()
                    from_pool = True

                    # 如果连接不是template1数据库，关闭它并创建新连接
                    if temp_conn.info.dbname != 'template1':
                        temp_conn.close()
                        temp_conn = psycopg2.connect(
                            host=self.host,
                            port=self.port,
                            user=self.user,
                            password=self.password,
                            dbname='template1',
                            client_encoding=self.charset
                        )
                        from_pool = False  # 这是新连接，不是来自池
                else:
                    # 直接创建新连接
                    temp_conn = psycopg2.connect(
                        host=self.host,
                        port=self.port,
                        user=self.user,
                        password=self.password,
                        dbname='template1',
                        client_encoding=self.charset
                    )
                    from_pool = False

                temp_conn.autocommit = True  # 必须设置为自动提交

                with temp_conn.cursor() as cursor:
                    # 终止所有连接到目标数据库的会话
                    cursor.execute(f"""
                        SELECT pg_terminate_backend(pg_stat_activity.pid)
                        FROM pg_stat_activity
                        WHERE pg_stat_activity.datname = '{db_name}'
                        AND pid <> pg_backend_pid()
                    """)
                    # 执行删除数据库
                    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")

                    if self.debug:
                        nprint(f"数据库 {db_name} 已成功删除")

            finally:
                if temp_conn:
                    if self.use_pool and from_pool and self._connection_pool is not None:
                        # 只有从池中获取的连接才放回池中
                        self._connection_pool.putconn(temp_conn)
                        if self.debug:
                            nprint("连接已归还到连接池")
                    else:
                        # 直接关闭非池化连接
                        temp_conn.close()
                        if self.debug:
                            nprint("直接连接已关闭")
        except psycopg2.Error as e:
            if self.debug:
                nprint(f"删除数据库失败: {e}")
            raise

    def drop_view(self, view_name: str):
        """删除视图"""
        self.exec_cmd(f'DROP VIEW IF EXISTS {view_name}')

    def getEncryAccountPassword(self, username: str) -> str:
        """
        获取PostgreSQL角色的密码（仅限有权限的用户）

        Args:
            username: 要查询的PostgreSQL角色名

        Returns:
            角色的密码哈希字符串

        Raises:
            ValueError: 如果角色不存在
            psycopg2.Error: 如果查询过程中发生数据库错误或权限不足
        """
        if not username:
            raise ValueError("角色名不能为空")

        cursor = None
        try:
            cursor = self.connection.cursor()

            # 方法1：查询pg_shadow（需要超级用户权限）
            try:
                query = """
                    SELECT passwd FROM pg_shadow 
                    WHERE usename = %s
                """
                cursor.execute(query, (username,))
                result = cursor.fetchone()

                if result:
                    return result[0]
            except psycopg2.Error:
                # 如果没有权限查询pg_shadow，尝试方法2
                pass

            # 方法2：查询pg_authid（需要超级用户权限）
            query = """
                SELECT rolpassword FROM pg_authid 
                WHERE rolname = %s
            """
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result is None:
                raise ValueError(f"角色 '{username}' 不存在")

            password_hash = result[0]
            if not password_hash:
                raise ValueError(f"角色 '{username}' 没有设置密码")

            return password_hash

        except psycopg2.Error as e:
            if self.debug:
                nprint(f"查询角色密码失败: {e}")
            raise
        finally:
            if cursor is not None:
                cursor.close()

    def resetPassword(self, new_password: str, username: Optional[str] = None,
                      require_old_password: bool = False, old_password: Optional[str] = None):
        """重置PostgreSQL用户密码"""
        if not new_password:
            raise ValueError("新密码不能为空")

        target_user = username or self.user
        is_current_user = (target_user == self.user)

        try:
            # 确保连接到postgres数据库
            original_db = self._current_db
            if self.current_db != 'postgres':
                self.current_db = 'postgres'

            # 构建ALTER ROLE语句
            query = sql.SQL("ALTER ROLE {} WITH PASSWORD {}").format(
                sql.Identifier(target_user),
                sql.Literal(new_password)
            )

            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()

            if self.debug:
                nprint(f"用户 {target_user} 的密码已更新")

            # 如果修改的是当前用户密码，需要重新连接
            if is_current_user:
                self.password = new_password
                self._safe_disconnect()
                self.connect_server()
                if self.debug:
                    nprint("已使用新密码重新连接数据库")

        except psycopg2.Error as e:
            if self.debug:
                nprint(f"重置密码失败: {e}")
            raise
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            # 恢复原始数据库连接
            if original_db and original_db != 'postgres':
                self.current_db = original_db

    def createAdminAccount(self, username: str, password: str) -> bool:
        """创建管理员账户"""
        if not username or not password:
            if self.debug:
                nprint("用户名和密码不能为空")
            return False

        original_db = self._current_db
        try:
            # 确保连接到postgres数据库
            if self.current_db != 'postgres':
                self.current_db = 'postgres'

            # 创建用户并设置密码
            self.exec_cmd(f"CREATE USER {username} WITH PASSWORD '{password}'")
            # 授予超级用户权限
            self.exec_cmd(f"ALTER USER {username} WITH SUPERUSER")
            if self.debug:
                nprint(f"已创建管理员账户 {username}")
            return True
        except psycopg2.Error as e:
            if self.debug:
                nprint(f"创建管理员账户失败: {e}")
            return False
        finally:
            # 恢复原始数据库连接
            if original_db and original_db != 'postgres':
                self.current_db = original_db

    def createOnlyReadAccount(self, username: str, password: str) -> bool:
        """创建只读账户"""
        if not username or not password:
            if self.debug:
                nprint("用户名和密码不能为空")
            return False

        original_db = self._current_db
        try:
            # 确保连接到正确的数据库
            if not self._current_db:
                raise RuntimeError("当前未选择数据库")

            # 创建用户并设置密码
            self.exec_cmd(f"CREATE USER {username} WITH PASSWORD '{password}'")
            # 授予连接到当前数据库的权限
            self.exec_cmd(f"GRANT CONNECT ON DATABASE {self._current_db} TO {username}")
            # 授予所有表的只读权限
            self.exec_cmd(f"GRANT USAGE ON SCHEMA public TO {username}")
            self.exec_cmd(f"GRANT SELECT ON ALL TABLES IN SCHEMA public TO {username}")
            # 设置默认权限
            self.exec_cmd(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO {username}")

            if self.debug:
                nprint(f"已创建只读账户 {username}")
            return True
        except psycopg2.Error as e:
            if self.debug:
                nprint(f"创建只读账户失败: {e}")
            return False
        finally:
            # 恢复原始数据库连接
            if original_db and original_db != self._current_db:
                self.current_db = original_db

    def createDefaultAccount(self, username: str, password: str) -> bool:
        """创建默认权限账户"""
        if not username or not password:
            if self.debug:
                nprint("用户名和密码不能为空")
            return False

        original_db = self._current_db
        try:
            # 确保连接到正确的数据库
            if not self._current_db:
                raise RuntimeError("当前未选择数据库")

            # 创建用户并设置密码
            self.exec_cmd(f"CREATE USER {username} WITH PASSWORD '{password}'")
            # 授予连接到当前数据库的权限
            self.exec_cmd(f"GRANT CONNECT ON DATABASE {self._current_db} TO {username}")
            # 授予所有表的读写权限
            self.exec_cmd(f"GRANT USAGE ON SCHEMA public TO {username}")
            self.exec_cmd(f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {username}")
            # 授予序列的使用权限
            self.exec_cmd(f"GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO {username}")
            # 设置默认权限
            self.exec_cmd(
                f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {username}")
            self.exec_cmd(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO {username}")

            if self.debug:
                nprint(f"已创建默认权限账户 {username}")
            return True
        except psycopg2.Error as e:
            if self.debug:
                nprint(f"创建默认权限账户失败: {e}")
            return False
        finally:
            # 恢复原始数据库连接
            if original_db and original_db != self._current_db:
                self.current_db = original_db

    def deleteAccountAnyWay(self, account_name: str) -> bool:
        """强制删除账户以及级联的数据"""
        if not account_name:
            if self.debug:
                nprint("用户名不能为空")
            return False

        original_db = self._current_db
        conn_params = {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'client_encoding': self.charset
        }

        temp_conn = None
        try:
            # 连接到管理数据库（如 postgres）
            admin_conn_params = conn_params.copy()
            admin_conn_params['dbname'] = 'postgres'

            # 获取连接
            if self.use_pool and self._connection_pool is not None:
                temp_conn = self._connection_pool.getconn()
                if temp_conn.info.dbname != 'postgres':
                    # 如果连接不是postgres数据库，关闭它并创建新连接
                    temp_conn.close()
                    temp_conn = psycopg2.connect(**admin_conn_params)
                    from_pool = False  # 标记这不是池化连接
                else:
                    from_pool = True  # 标记这是池化连接
            else:
                temp_conn = psycopg2.connect(**admin_conn_params)
                from_pool = False

            temp_conn.autocommit = True

            with temp_conn.cursor() as cursor:
                # 终止所有关联到该用户的会话
                cursor.execute("""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.usename = %s
                    AND pid <> pg_backend_pid()
                """, (account_name,))

                # 获取所有数据库列表
                cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
                all_dbs = [row[0] for row in cursor.fetchall()]

            # 处理每个数据库
            for db_name in all_dbs:
                db_conn = None
                db_from_pool = False
                try:
                    db_conn_params = conn_params.copy()
                    db_conn_params['dbname'] = db_name

                    if self.use_pool and self._connection_pool is not None:
                        db_conn = self._connection_pool.getconn()
                        if db_conn.info.dbname != db_name:
                            db_conn.close()
                            db_conn = psycopg2.connect(**db_conn_params)
                            db_from_pool = False
                        else:
                            db_from_pool = True
                    else:
                        db_conn = psycopg2.connect(**db_conn_params)
                        db_from_pool = False

                    db_conn.autocommit = True

                    with db_conn.cursor() as db_cursor:
                        # 转移所有权
                        db_cursor.execute(
                            sql.SQL("REASSIGN OWNED BY {} TO {}").format(
                                sql.Identifier(account_name),
                                sql.Identifier(self.user)
                            )
                        )

                        # 删除用户拥有的所有对象
                        db_cursor.execute(
                            sql.SQL("DROP OWNED BY {} CASCADE").format(
                                sql.Identifier(account_name)
                            )
                        )

                        # 撤销所有权限
                        db_cursor.execute(f"REVOKE ALL ON DATABASE {db_name} FROM {account_name}")

                        # 获取所有非系统模式
                        db_cursor.execute("""
                            SELECT schema_name 
                            FROM information_schema.schemata 
                            WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
                        """)
                        schemas = [row[0] for row in db_cursor.fetchall()]

                        for schema in schemas:
                            db_cursor.execute(f"REVOKE USAGE ON SCHEMA {schema} FROM {account_name}")
                            db_cursor.execute(f"REVOKE ALL ON ALL TABLES IN SCHEMA {schema} FROM {account_name}")
                            db_cursor.execute(f"REVOKE ALL ON ALL SEQUENCES IN SCHEMA {schema} FROM {account_name}")
                            db_cursor.execute(f"REVOKE ALL ON ALL FUNCTIONS IN SCHEMA {schema} FROM {account_name}")

                    if self.debug:
                        nprint(f"数据库 {db_name} 中的账户 {account_name} 相关对象已成功删除")

                except psycopg2.Error as e:
                    if self.debug:
                        nprint(f'处理数据库 {db_name} 时出错: {e}')
                    continue
                finally:
                    if db_conn:
                        if self.use_pool and db_from_pool:
                            self._connection_pool.putconn(db_conn)
                        else:
                            db_conn.close()

            # 删除用户角色
            temp_conn = psycopg2.connect(**admin_conn_params)
            temp_conn.autocommit = True
            with temp_conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("DROP ROLE IF EXISTS {}").format(
                        sql.Identifier(account_name)
                    )
                )
                if self.debug:
                    nprint(f"账户 {account_name} 已成功从系统中删除")
            return True

        except psycopg2.Error as e:
            if self.debug:
                nprint(f"删除账户失败: {e}")
            return False
        finally:
            if temp_conn:
                if self.use_pool and from_pool:
                    self._connection_pool.putconn(temp_conn)
                else:
                    temp_conn.close()
            # 恢复原始连接
            if original_db:
                self.use_database(original_db)

    def showAllAccountWithPermission(self) -> list:
        """
        显示所有账户及其权限

        Returns:
            list: 包含账户信息的列表，每个元素是一个元组 (用户名, 是否是超级用户, 权限列表)
        """
        cursor = None
        try:
            cursor = self.connection.cursor()

            # 查询所有用户及其权限
            cursor.execute("""
                SELECT 
                    r.rolname AS username,
                    r.rolsuper AS is_superuser,
                    r.rolcreaterole AS can_create_roles,
                    r.rolcreatedb AS can_create_db,
                    r.rolcanlogin AS can_login,
                    ARRAY(
                        SELECT privilege_type 
                        FROM information_schema.role_table_grants 
                        WHERE grantee = r.rolname
                        AND table_schema NOT IN ('pg_catalog', 'information_schema')
                        UNION
                        SELECT 'CONNECT' 
                        FROM pg_database d
                        WHERE has_database_privilege(r.rolname, d.datname, 'CONNECT')
                        AND d.datname = current_database()
                    ) AS privileges
                FROM pg_roles r
                WHERE r.rolname NOT LIKE 'pg_%'
                ORDER BY r.rolname
            """)

            result = cursor.fetchall()

            # 格式化结果
            formatted_result = []
            for row in result:
                username, is_superuser, can_create_roles, can_create_db, can_login, privileges = row
                formatted_result.append((
                    username,
                    bool(is_superuser),
                    {
                        'can_create_roles': bool(can_create_roles),
                        'can_create_db': bool(can_create_db),
                        'can_login': bool(can_login),
                        'privileges': list(privileges) if privileges else []
                    }
                ))

            return formatted_result

        except psycopg2.Error as e:
            if self.debug:
                nprint(f"获取账户权限信息失败: {e}")
            raise
        finally:
            if cursor is not None:
                cursor.close()

    @staticmethod
    def print_as_table(data: list, headers=None):
        """
        将列表数据打印为表格形式，支持嵌套数据结构

        参数:
            data: 要打印的数据列表，可以是单列或多列
            headers: 可选，表头列表
        """
        if not data:
            print("No data to display")
            return

        # 处理单列数据（如 ['a', 'b', 'c']）
        if not isinstance(data[0], (list, tuple)):
            data = [[item] for item in data]

        # 预处理数据：将字典和嵌套结构转换为字符串
        processed_data = []
        for row in data:
            processed_row = []
            for item in row:
                if isinstance(item, dict):
                    # 格式化字典为多行字符串
                    dict_str = "\n".join(f"{k}: {v}" for k, v in item.items())
                    processed_row.append(dict_str)
                elif isinstance(item, (list, tuple)):
                    # 格式化列表为逗号分隔的字符串
                    processed_row.append(", ".join(str(x) for x in item))
                else:
                    processed_row.append(str(item))
            processed_data.append(processed_row)

        # 如果有表头，添加到数据前面用于计算列宽
        temp_data = list(processed_data)
        if headers:
            temp_data = [headers] + temp_data

        # 计算每列的最大显示宽度（考虑中文字符和多行内容）
        num_columns = len(temp_data[0])
        col_widths = [0] * num_columns
        for row in temp_data:
            for i, item in enumerate(row):
                max_line_width = 0
                for line in str(item).split('\n'):
                    width = 0
                    for char in line:
                        if '\u4e00' <= char <= '\u9fff':  # 中文字符算2个宽度
                            width += 2
                        else:
                            width += 1
                    max_line_width = max(max_line_width, width)
                col_widths[i] = max(col_widths[i], max_line_width)

        # 创建分隔线
        def make_border(widths):
            parts = []
            for w in widths:
                parts.append('-' * (w + 2))
            return '+' + '+'.join(parts) + '+'

        border = make_border(col_widths)

        # 打印表格
        print(border)

        # 打印表头（如果有）
        if headers:
            header_str = "|"
            for i, header in enumerate(headers):
                # 内联 pad_cjk 逻辑
                text = str(header)
                current_width = 0
                for char in text:
                    if '\u4e00' <= char <= '\u9fff':
                        current_width += 2
                    else:
                        current_width += 1
                if current_width >= col_widths[i]:
                    padded_text = text
                else:
                    padded_text = text + ' ' * (col_widths[i] - current_width)
                header_str += ' ' + padded_text + ' |'
            print(header_str)
            print(border)

        # 打印数据行
        for row in processed_data:
            # 计算需要多少行来显示这个数据（考虑多行内容）
            max_lines = max(len(str(item).split('\n')) for item in row)

            # 为每个单元格创建行列表
            cell_lines = []
            for item in row:
                lines = str(item).split('\n')
                # 填充不足的行
                lines += [''] * (max_lines - len(lines))
                cell_lines.append(lines)

            # 打印每一组行
            for line_num in range(max_lines):
                row_str = "|"
                for i in range(num_columns):
                    # 内联 pad_cjk 逻辑
                    text = cell_lines[i][line_num]
                    current_width = 0
                    for char in text:
                        if '\u4e00' <= char <= '\u9fff':
                            current_width += 2
                        else:
                            current_width += 1
                    if current_width >= col_widths[i]:
                        padded_text = text
                    else:
                        padded_text = text + ' ' * (col_widths[i] - current_width)
                    row_str += ' ' + padded_text + ' |'
                print(row_str)

        print(border)

    def disconnect_server(self):
        """断开PostgreSQL服务器连接"""
        self._safe_disconnect()

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出时自动关闭连接"""
        self._safe_disconnect()

    def _safe_disconnect(self):
        """安全的断开连接方法"""
        try:
            if self.connection is not None and not self.connection.closed:
                try:
                    if self._using_pool_connection and self._connection_pool is not None:
                        self._connection_pool.putconn(self.connection)
                        if self.debug:
                            nprint("连接已归还到连接池")
                    else:
                        self.connection.close()
                        if self.debug:
                            nprint("直接连接已关闭")
                except Exception as e:
                    if self.debug:
                        nprint(f"关闭连接时发生错误: {e}")
                finally:
                    self.connection = None
                    self._using_pool_connection = False
        except Exception as e:
            if self.debug:
                nprint(f"断开连接时发生错误: {e}")

    def __del__(self):
        self._safe_disconnect()