import asyncio
import inspect
from enum import Enum

__all__ = ["n_asythread_status", "n_asyncThreadPool"]

class n_asythread_status(Enum):
    unstart: int = 0
    running: int = 1
    finish: int = 2

class n_asyerror(Exception):
    def __init__(self, message):
        self.message = message
        self.line_number = inspect.currentframe().f_back.f_lineno
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} (line {self.line_number})"

class n_asyncThreadPool:
    def __init__(self, max_workers: int = None, group: int = 0, time_interval: float = 0.0):
        self.max_workers = 5 if max_workers is None else max_workers
        self._status = n_asythread_status.unstart
        self._asythreads: list = []
        self._results = None
        self._group_size = group  # 默认不分组
        self._group_interval = time_interval  # 默认无间隔

    def setGroupExecInterval(self, group: int, time_interval: float):
        """设置分组执行参数
        Args:
            group: 每组任务数，0表示禁用分组
            time_interval: 组间间隔秒数
        """
        if group < 0:
            raise n_asyerror("Group size cannot be negative")
        if time_interval < 0:
            raise n_asyerror("Time interval cannot be negative")
        self._group_size = group
        self._group_interval = time_interval

    @property
    def getStatus(self) -> n_asythread_status:
        return self._status

    def put(self, func, *args, **kwargs):
        self._asythreads.append([func, args, kwargs])

    def __enter__(self):
        """上下文管理器入口，仅返回self不自动执行"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口，仅处理异常不自动执行"""
        if exc_type is not None and self._status == n_asythread_status.running:
            # 如果有异常且正在运行，尝试终止
            self._status = n_asythread_status.finish
        # 不抑制任何异常
        return False

    # 函数完成后不会清空任务列表 需要调用clear函数手动清除
    def start(self) -> list:
        if self._status == n_asythread_status.running:
            raise n_asyerror('Exist Task is Running, Start Failed')
        self._status = n_asythread_status.running

        async def _in():
            all_results = []
            # 准备所有任务
            tasks = []
            for item in self._asythreads:
                func, args, kwargs = item
                tasks.append(func(*args, **kwargs))

            # 分组执行逻辑
            if self._group_size > 0:
                for i in range(0, len(tasks), self._group_size):
                    group_tasks = tasks[i:i + self._group_size]
                    group_results = await self._execute_tasks(group_tasks)
                    all_results.extend(group_results)

                    # 非最后一组且间隔>0时睡眠
                    if i + self._group_size < len(tasks) and self._group_interval > 0:
                        await asyncio.sleep(self._group_interval)
            else:
                all_results = await self._execute_tasks(tasks)

            return all_results

        try:
            result = asyncio.run(_in())
            self._status = n_asythread_status.finish
            return result
        except Exception as e:
            self._status = n_asythread_status.finish
            raise n_asyerror(f"Error during concurrent execution: {str(e)}")

    async def _execute_tasks(self, tasks):
        """执行任务组的内部方法"""
        if self.max_workers is not None:
            semaphore = asyncio.Semaphore(self.max_workers)

            async def sem_task(task):
                async with semaphore:
                    return await task

            tasks = [sem_task(task) for task in tasks]
        return await asyncio.gather(*tasks, return_exceptions=True)

    def get_results(self):
        return self._results

    @classmethod
    def single_submit(cls, func, *args, **kwargs) -> any:
        async def _main():
            if not args and not kwargs:
                coro = func()
            else:
                coro = func(*args, **kwargs)
            return await coro

        return asyncio.run(_main())

    def clear(self):
        if self._status == n_asythread_status.running:
            raise n_asyerror('Exist Task is Running, Start Failed')
        self._asythreads.clear()
        self._status = n_asythread_status.unstart
        self._group_size = 0
        self._group_interval = 0.0

    def map(self, func, *args) -> list:
        if self._status == n_asythread_status.running:
            raise n_asyerror('Exist Task is Running, Start Failed')
        self._status = n_asythread_status.running

        async def _in():
            all_results = []
            # 参数处理
            if len(args) == 1 and isinstance(args[0], (list, tuple)):
                arg_sets = args[0]
            else:
                arg_sets = [(arg,) if not isinstance(arg, (list, tuple)) else arg for arg in args]

            # 准备所有任务
            tasks = [func(*arg_set) for arg_set in arg_sets]

            # 分组执行逻辑
            if self._group_size > 0:
                for i in range(0, len(tasks), self._group_size):
                    group_tasks = tasks[i:i + self._group_size]
                    group_results = await self._execute_tasks(group_tasks)
                    all_results.extend(group_results)

                    if i + self._group_size < len(tasks) and self._group_interval > 0:
                        await asyncio.sleep(self._group_interval)
            else:
                all_results = await self._execute_tasks(tasks)

            # 检查异常
            for res in all_results:
                if isinstance(res, Exception):
                    raise n_asyerror(f"Task execution failed: {str(res)}")
            return all_results

        try:
            result = asyncio.run(_in())
            self._status = n_asythread_status.finish
            return result
        except Exception as e:
            self._status = n_asythread_status.finish
            raise n_asyerror(f"Error during map execution: {str(e)}")

