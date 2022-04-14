import random
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QHBoxLayout


class MessageBox(QWidget):
    """
    消息框对象
    """
    def __init__(self):
        super(MessageBox, self).__init__()
        self.button = QPushButton('获取一个随机数～', self)
        self.button.clicked.connect(self.do_something)

        # 设置布局
        self.all_h_layout = QHBoxLayout()
        self.all_h_layout.addWidget(self.button)
        self.setLayout(self.all_h_layout)

    def do_something(self):
        """
        槽函数，使用MessageBox输出内容
        :return: None
        """
        question_choice = QMessageBox.question(self, "Change Num ?", "获取一个新的随机数？", QMessageBox.No | QMessageBox.Yes)

        if question_choice == QMessageBox.Yes:
            self.button.setText(str(random.randint(0, 100)))
        else:
            pass

