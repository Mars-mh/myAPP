import time
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QFileDialog, QTextBrowser, QCheckBox
from PyQt5.QtGui import QIcon

from ReadWords import ReadWords
from ReadObjList import ReadObjList
from ReadData import ReadData
from GetKeyWords import GetKeyWords
from GetAdjMatrix import GetAdjMatrix

import os
import sys

# 防止打包出错，指定加载路径
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    the_path = sys._MEIPASS + '/'
else:
    the_path = os.path.dirname(__file__) + '/'

the_path = the_path.replace('\\', '/')


class ProfessionalMode(QWidget):
    """
    主页面
    """
    def __init__(self):
        super(ProfessionalMode, self).__init__()

        # 设置数据存储区
        self._stop_list = None
        self._my_dict_list = None
        self._doc_list = None

        # 初始化显示label
        self.stopwords_label = QLabel('停用词未更新 (*.txt with utf-8) ...', self)
        self.my_dict_label = QLabel('用户词典未更新 (*.txt with utf-8) ...', self)
        self.obj_label = QLabel('项目文件夹为空 (contain *.txt with utf-8) ...', self)

        # 设置参数区域
        self._cut_all = False
        self._hmm = False
        self._word_style_red = "<b><font color='red'>"
        self._word_style_green = "<b><font color='green'>"

        # 设置结果区域
        self._fre_dir = None

        self._time = lambda x: x.strftime("%Y-%m-%d %H:%M:%S", x.localtime())

        # 设置页面标题，固定页面大小
        self.setWindowTitle('专业模式')
        self.setWindowIcon(QIcon(the_path + 'my_icon/mc_icon.ico'))
        self.resize(800, 600)
        self.setFixedSize(800, 600)

        # 初始化日志打印text browser
        self.my_log = QTextBrowser(self)
        self.my_log.setStyleSheet(f"border-image:url({the_path}my_icon/mc_p.png)")

        # 初始化功能按钮
        self.stopwords_button = QPushButton('更新停用词', self)
        self.stopwords_button.clicked.connect(lambda: self.get_words_path(1))

        self.my_dict_button = QPushButton('更新用户词典', self)
        self.my_dict_button.clicked.connect(lambda: self.get_words_path(2))

        self.obj_button = QPushButton('读取项目文件夹', self)
        self.obj_button.clicked.connect(self.get_obj_path)

        self.stopwords_print_button = QPushButton('打印', self)
        self.stopwords_print_button.clicked.connect(lambda: self.print_words(1))

        self.dict_print_button = QPushButton('打印', self)
        self.dict_print_button.clicked.connect(lambda: self.print_words(2))

        self.obj_print_button = QPushButton('打印', self)
        self.obj_print_button.clicked.connect(self.print_doc_list)

        self.hmm_check = QCheckBox('是否使用HMM模型')
        self.hmm_check.stateChanged.connect(lambda: self.switch_check_box(1))
        self.cut_all_check = QCheckBox('是否启用全模式')
        self.cut_all_check.stateChanged.connect(lambda: self.switch_check_box(2))

        self.cut_button = QPushButton('开始分词', self)
        self.cut_button.clicked.connect(self.get_words_cut)

        self.key_button = QPushButton('提取关键词', self)
        self.key_button.clicked.connect(self.get_key_words)

        self.adj_button = QPushButton('词共现矩阵', self)
        self.adj_button.clicked.connect(self.get_adj_matrix)

        self.clear_button = QPushButton('清空日志', self)
        self.clear_button.clicked.connect(self.clear_log)
        self.clear_all_button = QPushButton('重新启动', self)
        self.clear_all_button.clicked.connect(self.kill_all)

        # 布局分区
        self.grid_layout = QGridLayout()

        # 初始化各个布局分区内容
        self.layout_init()

    def layout_init(self):
        """
        为各个分区添加元素
        :return: None
        """
        self.grid_layout.addWidget(self.stopwords_button, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.stopwords_print_button, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.stopwords_label, 0, 2, 1, 3)

        self.grid_layout.addWidget(self.my_dict_button, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.dict_print_button, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.my_dict_label, 1, 2, 1, 3)

        self.grid_layout.addWidget(self.obj_button, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.obj_print_button, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.obj_label, 2, 2, 1, 3)

        self.grid_layout.addWidget(self.my_log, 3, 1, 8, 4)

        self.grid_layout.addWidget(self.cut_all_check, 3, 0, 1, 1)
        self.grid_layout.addWidget(self.hmm_check, 4, 0, 1, 1)

        self.grid_layout.addWidget(self.cut_button, 5, 0, 1, 1)
        self.grid_layout.addWidget(self.key_button, 6, 0, 1, 1)
        self.grid_layout.addWidget(self.adj_button, 7, 0, 1, 1)

        self.grid_layout.addWidget(self.clear_button, 8, 0)
        self.grid_layout.addWidget(self.clear_all_button, 9, 0)

        self.setLayout(self.grid_layout)

        # 写日志
        self.my_log.append(f'<b>{self._time(time)}: 初始化界面完成 ...')

    def get_words_path(self, target_type):
        """
        获取词列表
        :param target_type: 1表示停用词，2表示用户词典
        :return: None
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "选取文件", './')

        if target_type == 1:
            type_name = '停用词'
        else:
            type_name = '用户自定义词典'

        if file_name:
            if target_type == 1:
                self.stopwords_label.setText(file_name)

            elif target_type == 2:
                self.my_dict_label.setText(file_name)

            self.my_log.append(f'<b>{self._time(time)}: 读取停用词位置完成 ...')
        else:
            self.my_log.append(f"{self._word_style_red}{self._time(time)}: {type_name}读取失败，未选择文件  ！！！")
            return

        try:
            if target_type == 1:
                self._stop_list = ReadWords(self.stopwords_label.text()).get_words_list()
            elif target_type == 2:
                self._my_dict_list = ReadWords(self.my_dict_label.text()).get_words_list()

            self.my_log.append(f'<b>{self._time(time)}: {type_name}解析完成 ...')

        except UnicodeDecodeError:
            self.my_log.append(f"{self._word_style_red}{self._time(time)}: {type_name}读取失败，请检查文本编码是否为UTF-8  ！！！")
        except FileNotFoundError:
            self.my_log.append(f"{self._word_style_red}{self._time(time)}: {type_name}读取失败，未选择文件  ！！！")

    def get_obj_path(self):
        dir_name = QFileDialog.getExistingDirectory(self, "选取文件夹", './')

        if dir_name:
            self.obj_label.setText(dir_name)
            self.my_log.append(f'<b>{self._time(time)}: 读取待分析文件夹完成...')
        else:
            self.my_log.append(f"{self._word_style_red}{self._time(time)}: {dir_name}读取失败，未选择文件夹  ！！！")
            return

        # 开始读取项目列表
        try:
            self._doc_list = list(ReadObjList(dir_name).get_obj_list())
        except FileNotFoundError:
            self._doc_list = None

    def print_words(self, print_type):
        """
        打印停用词及用户自定义词典
        :param print_type: 1表示停用词，2表示用户词典，其余数值直接退出
        :return: None
        """
        if print_type == 1:
            type_name = '停用词'
            target = self._stop_list
        elif print_type == 2:
            type_name = '用户自定义辞典'
            target = self._my_dict_list
        else:
            return

        # 若为空时点击打印，则输出警告
        if not target:
            self.my_log.append(f"{self._word_style_red}{self._time(time)}: {type_name}为空，无法打印 ！！！")
            return

        self.my_log.append(f'<b>{self._time(time)}: 打印最近添加的前100个{type_name}：')
        self.my_log.append('<b>' + '-' * 65)

        # 只打印前100，若小于则全部输出
        n = 100 if len(target) >= 100 else len(target)
        tmp = ['<table><tr>']

        for i in range(1, n+1):
            tmp.append('<td>' + str(target[-i]) + '</td><td></td>')
            if i % 8 == 0:
                tmp.append('</tr><tr>')

        tmp.append('</tr></table>')

        self.my_log.append("".join(tmp))

    def print_doc_list(self):
        if not self._doc_list:
            self.my_log.append(f"{self._word_style_red}{self._time(time)}: 项目文件夹为空，无法打印 ！！！")
            return

        self.my_log.append(f'<b>{self._time(time)}: 打印最近添加的项目文件名：')
        self.my_log.append('<b>' + '-' * 65)

        for item in self._doc_list:
            self.my_log.append(item)

    def switch_check_box(self, box_type):
        """

        :param box_type: 1表示hmm 2表示cut_all
        :return:
        """
        if box_type == 1:
            if self.hmm_check.isChecked():
                self._hmm = True
                self.my_log.append(f'<b>{self._time(time)}: 选择使用 <HMM> 模型 ...')
            else:
                self._hmm = False
                self.my_log.append(f'<b>{self._time(time)}: 不选择使用 <HMM> 模型 ...')
        elif box_type == 2:
            if self.cut_all_check.isChecked():
                self._cut_all = True
                self.my_log.append(f'<b>{self._time(time)}: 选择使用 <全模式> ...')
            else:
                self._cut_all = False
                self.my_log.append(f'<b>{self._time(time)}: 选择使用 <精确模式> ...')
        else:
            pass

    def get_words_cut(self):
        if not self._stop_list or not self._my_dict_list or not self._doc_list:
            self.my_log.append(f"{self._word_style_red}{self._time(time)}: 请完成基本配置，再进行分词 ！！！")
            return

        self.my_log.append("<b>" + "-" * 65 + "</font>")
        self.my_log.append(f"{self._word_style_green}{self._time(time)}:" + "开始分词...")
        self.my_log.append(f"{self._word_style_green}----分词模型配置为: 使用HMM({self._hmm}) and 使用全模式({self._cut_all})")
        self.my_log.append(f"{self._word_style_green}----项目文档个数为: {len(self._doc_list)}" + "</font>")

        obj_path = self.obj_label.text() + '/'

        read_data = ReadData(obj_path, self._stop_list, self._my_dict_list, self._cut_all, self._hmm)

        # 遍历存入词频结果
        for item in self._doc_list:

            try:
                read_data.my_cut(obj_path, item)
            except UnicodeDecodeError:
                self.my_log.append("<b>" + "-" * 65 + "</font>")
                self.my_log.append(f"{self._word_style_red}{self._time(time)}:" + f"项目文件夹中'{item}'编码错误...")
                return

        self._fre_dir = obj_path + '词频结果/'
        self.my_log.append(f"{self._word_style_green}{self._time(time)}: 分词结束...")
        self.my_log.append(f"{self._word_style_green}----结果保存在文件夹: {self._fre_dir}")

    def get_key_words(self):
        if not self._fre_dir:
            self.my_log.append(f"{self._word_style_red}{self._time(time)}: 请完成分词操作，再进行关键词抽取 ！！！")
            return

        self.my_log.append("<b>" + "-" * 65 + "</font>")
        self.my_log.append(f"{self._word_style_green}{self._time(time)}: 开始提取关键词(TF_IDF)...")
        self.my_log.append(f"{self._word_style_green}{self._time(time)}: 开始提取关键词(JIEBA_TF_IDF)...")
        self.my_log.append(f"{self._word_style_green}{self._time(time)}: 开始提取关键词(JIEBA_TEXT_RANK)...")

        key_words = GetKeyWords(self._fre_dir)
        key_words.get_tf_idf()
        self.my_log.append(f"{self._word_style_green}{self._time(time)}: 关键词抽取结束...")
        self.my_log.append(f"{self._word_style_green}----结果保存在文件夹: {self._fre_dir.replace('词频结果/', '') + 'TFIDF统计结果/'}")

    def get_adj_matrix(self):
        if not self._fre_dir:
            self.my_log.append(f"{self._word_style_red}{self._time(time)}: 请完成分词及关键词抽取 ！！！")
            return

        adj_matrix = GetAdjMatrix(self._fre_dir)
        self.my_log.append("<b>" + "-" * 65 + "</font>")
        self.my_log.append(f"{self._word_style_green}{self._time(time)}: 开始统计文章间关键词共现结果...")
        adj_matrix.get_adj_matrix()
        self.my_log.append(f"{self._word_style_green}{self._time(time)}: 文章间关键词共现结果统计结束...")
        self.my_log.append(f"{self._word_style_green}----结果保存在文件夹: {self._fre_dir.replace('词频结果/', '') + '项目共现词统计结果/'}")

    def clear_log(self):
        if self.my_log.toPlainText():
            self.my_log.clear()
        else:
            pass

    def kill_all(self):
        self.my_log.clear()

        # 设置数据存储区
        self._stop_list = None
        self._my_dict_list = None
        self._doc_list = None

        # 设置参数区域
        self._cut_all = False
        self._hmm = False

        # 设置结果区域
        self._fre_dir = None

        # 初始化显示label
        self.stopwords_label.setText('停用词未更新 (*.txt with utf-8) ...')
        self.my_dict_label.setText('用户词典未更新 (*.txt with utf-8) ...')
        self.obj_label.setText('项目文件夹为空 (contain *.txt with utf-8) ...')


