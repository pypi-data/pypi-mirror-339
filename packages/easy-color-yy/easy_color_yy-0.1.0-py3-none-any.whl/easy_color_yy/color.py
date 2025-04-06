import  colorama
from colorama import Fore

class Color:
    """可以设置控制台字体的颜色"""

    def __init__(self):
        """初始化colorama"""
        colorama.init()

    @staticmethod
    def red_print(string: str):
        """红色字体"""
        print(Fore.RED + string)

    @staticmethod
    def blue_print(string: str):
        """蓝色字体"""
        print(Fore.BLUE + string)