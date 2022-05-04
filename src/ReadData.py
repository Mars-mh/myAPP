"""
读取项目文本数据
"""
import re
import os
import sys
import pandas as pd
import jieba
from collections import Counter

# 防止打包出错，指定加载路径
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    the_path = sys._MEIPASS + '\\'
else:
    the_path = os.path.dirname(__file__) + '\\'


class ReadData:

    def __init__(self, obj_path, stop_list, dict_list, cut_all, hmm):
        self.path = obj_path
        self.s_l = stop_list
        self.d_l = dict_list
        self.cut_all = cut_all
        self.hmm = hmm
        self.file_pattern = re.compile(r'[^\u4e00-\u9fa5]')

        # 创建结果保存路径
        self.res_path = self.path + '词频结果/'

        try:
            os.mkdir(self.res_path)
        except FileExistsError:
            pass

        jieba.load_userdict(self.d_l)

    def my_cut(self, target_path, file_name):
        """
        分词主函数
        :return:None
        """

        file = open(target_path + file_name, "r", encoding='utf-8')

        content = Counter()

        for item in file:
            item = re.sub(self.file_pattern, '', item)
            if len(item):
                cut_res = jieba.cut(item, HMM=self.hmm, cut_all=self.cut_all)

                # 去除停用词
                for word in cut_res:
                    if len(word) >= 2 and word not in self.s_l:
                        content[word] += 1

        frame = pd.DataFrame(content.items())
        sort_values = frame.sort_values(by=1, ascending=False)
        sort_values.to_csv(self.res_path + file_name.replace(".txt", '.csv'), header=None, index=None, encoding='gb2312')

