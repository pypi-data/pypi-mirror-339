import re

__all__ = ["InputValidator"]

class InputValidator:
    """
    输入验证正则表达式集合
    适用于PyQt5和网页表单的输入验证
    """

    @staticmethod
    def getEmailRegular():
        """
        获取电子邮件正则表达式
        规则:
        - 允许字母、数字、点(.)、下划线(_)、百分号(%)、加号(+)、减号(-)
        - @符号前至少1个字符
        - @符号后至少1个点(.)
        - 域名部分至少2个字符
        - 支持国际化域名
        """
        return r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    @staticmethod
    def getUsernameRegular():
        """
        获取用户名正则表达式
        规则:
        - 允许4-20个字符
        - 允许字母、数字、下划线
        - 必须以字母开头
        """
        return r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$'

    @staticmethod
    def getPasswordRegular():
        """
        获取密码正则表达式
        规则:
        - 至少8个字符
        - 包含至少1个大写字母
        - 包含至少1个小写字母
        - 包含至少1个数字
        - 可以包含特殊字符 @$!%*?&
        """
        return r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$'

    @staticmethod
    def getPhoneRegular():
        """
        获取手机号正则表达式
        规则:
        - 支持国际号码格式
        - 支持带+或不带+
        - 支持带空格或分隔符
        """
        return r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'

    @staticmethod
    def validate(input_str, pattern):
        """
        通用验证方法
        :param input_str: 要验证的字符串
        :param pattern: 正则表达式模式
        :return: 匹配返回True，否则False
        """
        return bool(re.fullmatch(pattern, input_str))