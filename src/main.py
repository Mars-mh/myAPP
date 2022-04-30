import sys
from PyQt5.QtWidgets import QApplication
from WelcomeBox import WelcomeBox

if __name__ == '__main__':
    app = QApplication(sys.argv)

    my_box = WelcomeBox()
    my_box.show()

    sys.exit(app.exec_())
