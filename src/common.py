from PyQt5.QtWidgets import QWidget, QPushButton


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        # 设置外观
        self.resize(300, 300)
        self.setWindowTitle('~~ My Demo ~~')

        # 设置动作
        self.button = QPushButton('OFF!', self)
        self.button.pressed.connect(self.button.released)
        self.button.released.connect(self.change_text)

    def change_text(self):
        print('change text')

        if self.button.text() == 'OFF!':
            self.button.setText('ON!')
        else:
            self.button.setText('OFF!')

        # self.button.clicked.connect(self.change_text)
