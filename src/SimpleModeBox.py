"""
简单模式，完成单个文章的分词
并将词频结果输出
"""
import jieba
import jieba.analyse
import re
import pandas as pd
import time
from collections import Counter
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QTextBrowser, QTextEdit, QHBoxLayout, QFileDialog, QGraphicsOpacityEffect

from CommonData import CommonData


def count_words_fun(text_input, my_stop_words):
    """
    统计词频
    :param my_stop_words: list of stop words
    :param text_input: generator object Tokenizer
    :return: dict: 词频统计结果
    """
    c = Counter()

    for item in text_input:
        if len(item) < 2 or item in my_stop_words:
            pass
        else:
            if item in c:
                c[item] += 1
            else:
                c[item] = 1
    return dict(c)


class SimpleMode(QWidget):
    def __init__(self):

        super(SimpleMode, self).__init__()

        # 数据保存
        self._output = {}
        self.file_pattern = re.compile(r'[^\u4e00-\u9fa5]')
        self.stop_words = CommonData().stop_words
        self._time = lambda x: x.strftime("%Y-%m-%d %H:%M:%S", x.localtime())

        # 固定页面大小
        self.resize(800, 600)

        # 初始化功能按钮
        self.clear_button = QPushButton('清除', self)
        self.go_button = QPushButton('开始', self)
        self.save_button = QPushButton('存储', self)

        self.clear_button.setEnabled(False)
        self.go_button.setEnabled(False)
        self.save_button.setEnabled(False)

        # 美化
        self.clear_button.setIcon(QIcon('./src/my_icon/clear.ico'))
        self.go_button.setIcon(QIcon('./src//my_icon/go.ico'))
        self.save_button.setIcon(QIcon('./src/my_icon/save.ico'))

        # 初始化输入输出文本框
        self.input_text_box = QTextEdit()
        self.input_text_box.setPlaceholderText('请输入待分词文本... ...')

        self.output_text_box = QTextBrowser()
        self.output_text_box.setPlaceholderText('结果输出窗口: \n 1-在左侧输入文本\n 2-选择开始进行分词\n 3-分词结果将在本框内显示\n 4-选择存储保存分词结果')

        self.input_text_box.setStyleSheet("border-image:url(./src/my_icon/mc_bg_l.png)")
        self.output_text_box.setStyleSheet("border-image:url(./src/my_icon/mc_bg_r.png)")

        self.input_text_box.textChanged.connect(self.check_input_fun)

        # 初始化布局
        self.grid_layout = QGridLayout()
        self.h_down_box_layout = QHBoxLayout()

        # 初始化各个布局分区内容
        self.layout_init()

        # 绑定各个按钮功能
        self.clear_button.clicked.connect(self.clear_input_fun)
        self.go_button.clicked.connect(self.go_fun)
        self.save_button.clicked.connect(self.save_fun)

    def layout_init(self):

        self.grid_layout.addWidget(self.input_text_box, 0, 0, 5, 1)
        self.grid_layout.addWidget(self.output_text_box, 0, 1, 5, 1)

        self.h_down_box_layout.addWidget(self.clear_button)
        self.h_down_box_layout.addWidget(self.go_button)
        self.h_down_box_layout.addWidget(self.save_button)

        self.grid_layout.addLayout(self.h_down_box_layout, 5, 0, 1, 2)

        self.setLayout(self.grid_layout)

    def check_input_fun(self):
        """
        检查输入文本框是否有内容，如果无则设置按钮不可用
        :return: None
        """
        if self.input_text_box.toPlainText():
            self.clear_button.setEnabled(True)
            self.go_button.setEnabled(True)
            self.save_button.setEnabled(True)
        else:
            self.clear_button.setEnabled(False)
            self.go_button.setEnabled(False)
            self.save_button.setEnabled(False)

    def clear_input_fun(self):
        """
        清除输入框中内容, 清空缓存中上一次的分词结果
        :return: None
        """
        if self.input_text_box.toPlainText():
            self.input_text_box.clear()
            self.output_text_box.clear()
        else:
            pass

        # 清空缓存中上一次的分词结果
        if self._output:
            self._output = {}
        else:
            pass

    def go_fun(self):
        """
        开始分词
        :return:None
        """
        text = self.input_text_box.toPlainText()
        item = re.sub(self.file_pattern, '', text)

        # 若输入为空
        if not item:
            self.output_text_box.append(f"<font color='red'>{self._time(time)}:\t未输入有效中文文本，请检查输入!</font>")
            return

        else:
            cut_res = jieba.cut(item, cut_all=True)

            # 获取 tf-idf / textrank 数值
            extract_tf_idf_tags = jieba.analyse.extract_tags(item, topK=100, withWeight=True)
            extract_textrank_tags = jieba.analyse.textrank(item, topK=100, withWeight=True)

            # 将tf-idf / textrank结果转化为字典
            tf_dict = {}
            trank_dict = {}

            for t in extract_tf_idf_tags:
                tf_dict[t[0]] = t[1]

            for t in extract_textrank_tags:
                trank_dict[t[0]] = t[1]

            # 获取词频
            count_words = count_words_fun(cut_res, self.stop_words)

            final_words = set(trank_dict.keys()) | set(tf_dict.keys())

            # 输出分词结果
            res = {}
            for word in final_words:
                tmp = [0, 0, 1]

                if word in tf_dict:
                    tmp[0] = round(tf_dict.get(word), 3)

                if word in trank_dict:
                    tmp[1] = round(trank_dict.get(word), 3)

                if word in count_words:
                    tmp[2] = round(count_words.get(word), 3)

                res[word] = tmp

            # 将结果写入类属性
            self._output = res

            # 在输出中打印
            self.output_text_box.append(f"<font color='green'>{self._time(time)}:\t 分词结果如下:</font>")
            self.output_text_box.append('-' * 60)
            self.output_text_box.append("{0:20}\t{1:4}\t{2:4}\t{3:4}".format('关键词', 'TF-IDF', 'TextRank', '词频'))
            self.output_text_box.append('-'*60)
            for k, v in self._output.items():
                my_str = "{0:20}\t{1:4}\t{2:4}\t{3:4}".format(k, v[0], v[1], v[2])
                self.output_text_box.append(my_str)
            self.output_text_box.append('-' * 60)

    def save_fun(self):
        """
        存储文件
        :return: None
        """
        # 先判断是否完成分词
        if not self._output:
            self.output_text_box.append(f"<font color='red'>{self._time(time)}:\t未进行中文文本分词，请先分词!</font>")
            return
        else:
            dir_name = QFileDialog.getExistingDirectory(self, "选取文件夹", './')

            # 后判断是否获取到有效存储位置
            if not dir_name:
                self.output_text_box.append(f"<font color='red'>{self._time(time)}:\t未选择保存文件的文件夹，保存失败!</font>")
                return

            tmp_res = []

            for k, v in self._output.items():
                tmp_res.append([k, v[0], v[1], v[2]])

            data_frame = pd.DataFrame(tmp_res, columns=['关键词', 'TF-IDF', 'TEXTRANK', '词频'])
            frame_sort_values = data_frame.sort_values(by='TF-IDF', ascending=False)

            full_file_name = dir_name + f'/简单模式分词结果-{self._time(time)}.csv'
            frame_sort_values.to_csv(full_file_name, index=False)

            self.output_text_box.append(f"<font color='green'>{self._time(time)}:\t 文件保存在:</font>")
            self.output_text_box.append(f"<font color='green'>{full_file_name}</font>")
