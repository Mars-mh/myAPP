import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox

FILE_PATH = "../data/user_inf.csv"


class WelcomeBox(QWidget):
    """
    欢迎洁面：
        用户名
        密码
    """

    def __init__(self):
        super(WelcomeBox, self).__init__()
        self.resize(300, 100)

        # 初始化两个label，及其对应文本输入框
        self.user_label = QLabel('Username:', self)
        self.user_line = QLineEdit(self)

        self.pwd_label = QLabel('Password:', self)
        self.pwd_line = QLineEdit(self)

        # 初始化登陆按钮
        self.login_button = QPushButton('Log in', self)
        self.signin_button = QPushButton('Sign in', self)

        # 布局分区
        self.grid_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        # 初始化各个分区内容
        self.layout_init()

    def layout_init(self):
        """
        为各个分区添加元素
        :return: None
        """
        self.grid_layout.addWidget(self.user_label, 0, 0)
        self.grid_layout.addWidget(self.user_line, 0, 1)
        self.grid_layout.addWidget(self.pwd_label, 1, 0)
        self.grid_layout.addWidget(self.pwd_line, 1, 1)

        self.h_layout.addWidget(self.login_button)
        self.h_layout.addWidget(self.signin_button)

        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    def lineedit_init(self):
        """
        初始化lineedit中的提示文本
        :return: None
        """
        self.user_line.setPlaceholderText('Please enter ur name')
        self.pwd_line.setPlaceholderText('Please enter ur password')

