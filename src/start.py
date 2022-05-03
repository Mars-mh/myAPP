"""
main文件
命令行打包: pyinstaller --add-data 'src/dict.txt:.' start.py
Windows 用户应该在上面的行中使用;而不是。:
"""
import sys
from PyQt5.QtWidgets import QApplication
from WelcomeBox import WelcomeBox

if __name__ == '__main__':
    app = QApplication(sys.argv)

    my_box = WelcomeBox()
    my_box.show()

    sys.exit(app.exec_())
