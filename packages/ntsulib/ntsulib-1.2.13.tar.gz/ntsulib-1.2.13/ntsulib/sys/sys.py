import inspect
import os
import platform
import sys
from enum import Enum, unique

import chardet

__all__ = [
    "get_file_bom","get_file_content","get_file_encoding","isEntryPoint",
    "getPlatForm","n_PlatForm","n_PlatForm_Bit"
           ]

@unique  # 确保枚举值唯一
class n_PlatForm(Enum):
    """操作系统平台枚举（涵盖主流系统和常见版本）"""
    # Windows 系列
    win_xp: int = 0         # Windows XP
    win_vista: int = 1      # Windows Vista
    win7: int = 2           # Windows 7
    win8: int = 3           # Windows 8
    win8_1: int = 4         # Windows 8.1
    win10: int = 5          # Windows 10
    win11: int = 6          # Windows 11
    win_server: int = 7      # Windows Server 系列（通用）
    # Linux 系列（常见发行版）
    linux_ubuntu: int = 8    # Ubuntu
    linux_debian: int = 9    # Debian
    linux_centos: int = 10   # CentOS
    linux_fedora: int = 11   # Fedora
    linux_arch: int = 12     # Arch Linux
    linux_gentoo: int = 13   # Gentoo
    linux_other: int = 14    # 其他 Linux 发行版
    # macOS 系列
    mac: int = 15            # macOS（通用）
    mac_catalina: int = 16   # macOS 10.15 (Catalina)
    mac_big_sur: int = 17    # macOS 11 (Big Sur)
    mac_monterey: int = 18   # macOS 12 (Monterey)
    mac_ventura: int = 19    # macOS 13 (Ventura)
    # 其他系统
    android: int = 20        # Android
    ios: int = 21            # iOS
    unix: int = 22           # 其他 Unix 系统（如 FreeBSD）
    unknown: int = 23        # 未知系统
@unique
class n_PlatForm_Bit(Enum):
    """CPU 架构和位数枚举（涵盖主流架构）"""
    x86: int = 0            # 32 位（x86）
    x64: int = 1            # 64 位（x86_64/AMD64）
    arm32: int = 2          # ARM 32 位（如 ARMv7）
    arm64: int = 3          # ARM 64 位（如 ARMv8/AArch64）
    ia64: int = 4           # Intel Itanium（安腾）
    mips: int = 5           # MIPS 架构
    riscv: int = 6          # RISC-V 架构
    ppc: int = 7            # PowerPC
    unknown: int = 8        # 未知架构

def getPlatForm() -> tuple[n_PlatForm, n_PlatForm_Bit]:
    """检测当前操作系统平台和CPU架构

    Returns:
        tuple[n_PlatForm, n_PlatForm_Bit]: (操作系统枚举, CPU架构枚举)
    """
    # 检测操作系统
    system = platform.system().lower()
    version = platform.version().lower()
    release = platform.release().lower()

    plat = n_PlatForm.unknown
    bit = n_PlatForm_Bit.unknown

    # 操作系统判断
    if system == "windows":
        if "xp" in version:
            plat = n_PlatForm.win_xp
        elif "vista" in version:
            plat = n_PlatForm.win_vista
        elif "7" in version:
            plat = n_PlatForm.win7
        elif "8.1" in version:
            plat = n_PlatForm.win8_1
        elif "8" in version:
            plat = n_PlatForm.win8
        elif "10" in version:
            plat = n_PlatForm.win10
        elif "11" in version or "10.0.22" in version:  # Win11可能报告为10.0.22xxx
            plat = n_PlatForm.win11
        else:
            plat = n_PlatForm.win_server

    elif system == "linux":
        # 尝试获取发行版信息
        try:
            import distro
            distro_id = distro.id().lower()
            if "ubuntu" in distro_id:
                plat = n_PlatForm.linux_ubuntu
            elif "debian" in distro_id:
                plat = n_PlatForm.linux_debian
            elif "centos" in distro_id:
                plat = n_PlatForm.linux_centos
            elif "fedora" in distro_id:
                plat = n_PlatForm.linux_fedora
            elif "arch" in distro_id:
                plat = n_PlatForm.linux_arch
            elif "gentoo" in distro_id:
                plat = n_PlatForm.linux_gentoo
            else:
                plat = n_PlatForm.linux_other
        except ImportError:
            plat = n_PlatForm.linux_other

    elif system == "darwin":
        plat = n_PlatForm.mac
        # 更精确的macOS版本检测
        mac_ver = platform.mac_ver()[0]
        if mac_ver.startswith("10.15"):
            plat = n_PlatForm.mac_catalina
        elif mac_ver.startswith("11."):
            plat = n_PlatForm.mac_big_sur
        elif mac_ver.startswith("12."):
            plat = n_PlatForm.mac_monterey
        elif mac_ver.startswith("13."):
            plat = n_PlatForm.mac_ventura

    elif system == "android":
        plat = n_PlatForm.android
    elif "ios" in system:
        plat = n_PlatForm.ios
    elif system in ("freebsd", "openbsd", "netbsd"):
        plat = n_PlatForm.unix

    # CPU架构判断
    machine = platform.machine().lower()
    if machine in ("x86_64", "amd64"):
        bit = n_PlatForm_Bit.x64
    elif machine == "x86" or machine == "i386" or machine == "i686":
        bit = n_PlatForm_Bit.x86
    elif machine.startswith("armv7") or machine == "arm":
        bit = n_PlatForm_Bit.arm32
    elif machine.startswith("armv8") or machine.startswith("aarch64"):
        bit = n_PlatForm_Bit.arm64
    elif machine == "ia64":
        bit = n_PlatForm_Bit.ia64
    elif "mips" in machine:
        bit = n_PlatForm_Bit.mips
    elif "riscv" in machine:
        bit = n_PlatForm_Bit.riscv
    elif "ppc" in machine or "powerpc" in machine:
        bit = n_PlatForm_Bit.ppc

    return (plat, bit)
def get_file_bom(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(4)
    if raw_data.startswith(b'\xff\xfe\x00\x00') or raw_data.startswith(b'\x00\x00\xfe\xff'):
        return 'UTF-32'
    elif raw_data.startswith(b'\xff\xfe') or raw_data.startswith(b'\xfe\xff'):
        return 'UTF-16'
    elif raw_data.startswith(b'\xef\xbb\xbf'):
        return 'UTF-8'
    else:
        return None
def get_file_encoding(file_path, candidate_encodings=['utf-8', 'gbk', 'iso-8859-9']):
    # 先尝试检测 BOM
    bom_encoding = get_file_bom(file_path)
    if bom_encoding:
        return bom_encoding
    # 如果 BOM 不存在，尝试手动检测
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    # 优先尝试候选编码
    for encoding in candidate_encodings:
        try:
            raw_data.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    # 如果候选编码都失败，再使用 chardet
    result = chardet.detect(raw_data)
    if result['confidence'] > 0.9:  # 只有当可信度较高时才返回
        return result['encoding']
    else:
        return None
# 自动解析编码并获取文件的内容
def get_file_content(file_path, candidate_encodings=['utf-8', 'gbk', 'iso-8859-9']):
    # 检测文件编码
    encoding = get_file_encoding(file_path, candidate_encodings)
    if encoding is None:
        # print("无法确定文件的编码格式。")
        return None
    # 打开文件并读取内容
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        # print(f"文件内容（编码: {encoding}）:")
        #print(content)
        return content
    except UnicodeDecodeError:
        # print(f"无法使用编码 {encoding} 解码文件。")
        return None
def isEntryPoint():
    # 获取主脚本的真实路径（处理符号链接等情况）
    main_script = os.path.realpath(sys.argv[0])

    # 获取当前模块的 __file__（如果是被导入的模块）
    caller_frame = inspect.currentframe().f_back
    caller_globals = caller_frame.f_globals

    # 检查当前模块是否是 __main__ 并且文件路径匹配
    if caller_globals.get('__name__') == '__main__':
        if '__file__' in caller_globals:
            caller_file = os.path.realpath(caller_globals['__file__'])
            if caller_file == main_script:
                return True

    # 如果不是 __main__ 或者文件不匹配，则不是入口点
    return False