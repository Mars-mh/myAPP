"""
处理 jieba 外部资源依赖问题
即解决静态资源打包问题
"""

import os
import sys

abspath_of_dict = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dict.txt'))
