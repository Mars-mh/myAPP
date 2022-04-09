import sys
from PyQt5.QtWidgets import QApplication
from common import Demo

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = Demo()
    demo.show()

    sys.exit(app.exec_())
