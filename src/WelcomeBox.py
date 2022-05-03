"""
选择界面
选择：简单模式或专业模式进行关键词分析
"""
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon
from SimpleModeBox import SimpleMode
from ProfessionalModeBox import ProfessionalMode


class WelcomeBox(QWidget):
    def __init__(self):

        super(WelcomeBox, self).__init__()

        self.setWindowTitle('鹏珍的分词工具箱')
        self.setWindowIcon(QIcon('my_icon/mc_icon.ico'))

        # 初始化包含的页面对象
        self.simple_widget = SimpleMode()
        self.professional_widget = ProfessionalMode()

        # 固定页面大小
        self.resize(200, 100)

        # 初始化按钮
        self.simple_button = QPushButton('简单模式', self)
        self.professional_button = QPushButton('专业模式', self)

        # 初始化label
        self.prompt_label = QLabel('选择模式:')

        # 初始化布局
        self.grid_layout = QGridLayout()

        # 初始化各个布局分区内容
        self.layout_init()

        # 绑定按键功能
        self.simple_button.clicked.connect(self.open_simple_mode)
        self.professional_button.clicked.connect(self.open_professional_mode)

    def layout_init(self):
        """
        初始化布局
        :return:None
        """
        self.grid_layout.addWidget(self.prompt_label, 0, 0)
        self.grid_layout.addWidget(self.simple_button, 1, 0)
        self.grid_layout.addWidget(self.professional_button, 2, 0)

        self.setLayout(self.grid_layout)

    def open_simple_mode(self):
        self.simple_widget.show()

    def open_professional_mode(self):
        self.professional_widget.show()
