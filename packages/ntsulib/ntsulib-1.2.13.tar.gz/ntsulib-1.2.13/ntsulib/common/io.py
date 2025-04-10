import sys
import os
from enum import Enum
import inspect
from pathlib import Path

__all__ = ["Auto_Mode","getProjectPath","get_temp_path"]

class Auto_Mode(Enum):
    disable = 0  # 禁用自动查找，仅按层级查找 会获取当前使用的py文件所在的位置
    normal = 1  # 普通模式：仅检测常规Python项目标记
    high = 2  # 高敏感模式：额外检测.venv/.idea等特殊标记
    highest = 3  # 最高敏感模式：合并normal和high的所有标记


def get_temp_path(relative_path=""):
    """
    获取应用程序资源路径（兼容普通运行和PyInstaller打包环境）
    总是基于调用者脚本的位置进行解析

    参数:
        relative_path (str): 相对于基础路径的子路径

    返回:
        str: 完整的资源路径
    """
    try:
        # PyInstaller打包后，从临时目录_MEIPASS加载
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            # 获取调用者脚本的路径
            frame = inspect.stack()[1]
            caller_path = frame.filename
            base_path = str(Path(caller_path).parent.absolute())

        # 拼接完整路径并规范化路径分隔符
        full_path = os.path.normpath(os.path.join(base_path, relative_path))
        return full_path
    except Exception as e:
        raise RuntimeError(f"Failed to determine resource path: {e}") from e

def getProjectPath(layer: int = 0, auto: Auto_Mode = Auto_Mode.normal ) -> str:
    """
    获取调用此库的主工程路径，支持四种模式：
    1. 禁用自动查找（auto=Auto_Mode.disable）
    2. 普通自动查找（auto=Auto_Mode.normal）
    3. 高敏感度查找（auto=Auto_Mode.high）
    4. 最高敏感度查找（auto=Auto_Mode.highest，合并normal和high的标记）

    参数:
        layer: 在找到工程路径后，再向上查找的目录层数 (0=不向上查找)
        auto: 自动查找模式（参见Auto_Mode枚举）
    返回:
        str: 项目路径
    异常:
        ValueError: 如果layer是负数
        RuntimeError: 如果无法确定路径
    """
    if layer < 0:
        raise ValueError("layer参数不能为负数")

    # 处理打包成exe的情况（忽略所有参数）
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)

    # 获取主模块路径
    main_module = sys.modules.get('__main__')
    if main_module is None or not hasattr(main_module, '__file__'):
        raise RuntimeError("无法确定主模块路径")

    # 获取主模块文件绝对路径
    main_file = os.path.abspath(main_module.__file__)
    current_path = os.path.dirname(main_file)

    # 非自动模式：直接使用当前路径作为工程路径
    if auto == Auto_Mode.disable:
        project_path = current_path
    else:
        # 自动模式：定义项目标记检测逻辑
        def is_project_dir(path: str) -> bool:
            """检查给定路径是否是项目根目录"""
            # 基础标记（normal模式）
            normal_markers = [
                'pyproject.toml',
                'setup.py',
                'setup.cfg',
                'MANIFEST.in',
                '.git',
                '.hg',
                'LICENSE',
                'Pipfile',
                'poetry.lock',
                '.projectroot',
                'README.md',
                '.gitignore',
                'requirements.txt'
            ]

            # 高敏感标记（high模式）
            high_markers = [
                '.idea',  # PyCharm项目
                '.vscode',  # VS Code项目
                '.venv',  # 虚拟环境目录
                'venv',
                'env'
            ]

            # 根据模式选择标记组合
            if auto == Auto_Mode.normal or auto == 1:
                markers = normal_markers
            elif auto == Auto_Mode.high or auto == 2:
                markers = high_markers
            elif auto == Auto_Mode.highest or auto == 3:  # Auto_Mode.highest
                markers = normal_markers + high_markers
            else:
                raise Exception("This Mode is Not Exist!")

            # 检查标记存在性（特殊处理目录类标记）
            for marker in markers:
                target = os.path.join(path, marker)
                if not os.path.exists(target):
                    continue

                # 特殊验证（避免误判子目录中的.idea/.venv等）
                if marker.startswith('.') and marker not in ('.git', '.hg'):
                    if marker in ('.idea', '.vscode'):
                        if not os.path.isdir(target):
                            continue
                    # 确保是顶层目录（父目录不存在相同标记）
                    parent_marker = os.path.join(os.path.dirname(path), marker)
                    if os.path.exists(parent_marker):
                        continue

                return True
            return False

        # 从当前路径向上查找项目根目录
        project_path = current_path
        while True:
            if is_project_dir(project_path):
                break
            parent = os.path.dirname(project_path)
            if parent == project_path:  # 到达根目录
                break
            project_path = parent

    # 无论什么模式，都根据layer参数向上返回父目录
    if layer > 0:
        for _ in range(layer):
            parent = os.path.dirname(project_path)
            if parent == project_path:  # 已经到达根目录
                break
            project_path = parent

    return project_path

def is_executable() -> bool:
    return not sys.executable.endswith('python.exe')

def is_dir_exists(path: str) -> bool:
    return os.path.isdir(path)

def is_file_exists(path: str) -> bool:
    return os.path.isfile(path)
