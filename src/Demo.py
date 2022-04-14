from IPython.external.qt_for_kernel import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton


def print_signal(msg):
    """
    在命令行打印 SomeThing Changed ！
    :return: None
    """
    print(f"{msg} Changed ！")


class Demo(QWidget):
    """
    Demo类，用于展示信号 & 槽
    """

    # 自定义信号
    my_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # 设置外观
        self.resize(300, 300)
        self.setWindowTitle('~~ My Demo ~~')

        # 设置点按动作
        self.button = QPushButton('OFF!', self)
        self.button.pressed.connect(self.button.released)
        self.button.released.connect(self.change_text)

        # 自定义信号
        self.my_signal.connect(self.change_text)

    def change_text(self):
        """
        槽函数，根据信号改变文本
        :return: None
        """
        print_signal("文本内容")

        if self.button.text() == 'OFF!':
            self.button.setText('ON!')
        else:
            self.button.setText('OFF!')
        # self.button.clicked.connect(self.change_text)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.my_signal.emit()

