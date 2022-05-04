"""
main文件
命令行打包: pyinstaller
time: 2022/5/4/19/49
"""
# 显示调用各个模块
import pandas as pd
import os
import sys
import math
import time
import re
from collections import Counter

from PyQt5.QtWidgets import QApplication
from WelcomeBox import WelcomeBox

if __name__ == '__main__':
    app = QApplication(sys.argv)

    my_box = WelcomeBox()
    my_box.show()

    sys.exit(app.exec_())
