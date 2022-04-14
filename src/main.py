import sys
from PyQt5.QtWidgets import QApplication
# from MessageBox import MessageBox
from WelcomeBox import WelcomeBox
# from Demo import Demo

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # demo = Demo()
    # demo.show()

    my_box = WelcomeBox()
    my_box.show()

    # message_box = MessageBox()
    # message_box.show()

    sys.exit(app.exec_())
