"""
使用TF_IDF, jieba-TF_IDF, TextRank 获取关键词
"""
import os
import math
import pandas as pd
import jieba.analyse


class GetKeyWords:
    def __init__(self, doc_path):
        # 基本路径
        self.doc_path = doc_path  # 文件根目录
        self.doc_list = os.listdir(doc_path)  # 文件列表

        # 创建保存内容地址
        self.res_path_root = doc_path.replace('词频结果/', '') + '关键词统计结果/'

        try:
            os.mkdir(self.res_path_root)
        except FileExistsError:
            pass

        self.data = []  # 各个文本词频表
        self.jieba_data = []  # jieba分词语料表

    def helper(self, target):
        """
        计算IDF所需数值
        :param target:
        :return: INT count_of_doc_num
        """
        tmp = 0
        dict_list = [x[1] for x in self.data]

        for x in dict_list:
            if target in x:
                tmp += 1

        return tmp

    def get_tf_idf(self):

        # 读取文件
        for item in self.doc_list:
            f = open(self.doc_path + item, 'r')

            word_pair = []

            for line in f:
                word_pair.append(line.replace('\n', '').split(','))

            # 计算词频并写入字典
            tmp_fre_sum = sum([int(x[1]) for x in word_pair])
            word_fre_dict = {}

            content = []  # JIEBA 分析的原料

            for word in word_pair:
                word_fre_dict[word[0]] = int(word[1]) / tmp_fre_sum
                content.append(word[0])

            self.data.append([item.replace('.csv', ''), word_fre_dict])
            self.jieba_data.append([item.replace('.csv', ''), " ".join(content)])

        total_dco_num = len(self.data)

        # 计算TF-IDF 并保存
        res_root = []
        res_root_name = []
        for item in self.data:
            file_name = item[0]
            file_data = item[1]

            res = {}

            for k, v in file_data.items():
                i = self.helper(k)
                res[k] = v * math.log(total_dco_num / i)

            res_root.append([(k, v) for k, v in res.items()])
            res_root_name.append(file_name)

        frame = pd.DataFrame(res_root, index=res_root_name).T
        frame.to_csv(self.res_path_root + '默认TF_IDF关键词结果.csv', index=False, encoding='utf-8')

        # 使用结巴计算相关结果
        res_jieba = []
        res_text_rank = []
        res_name = []
        for item in self.jieba_data:
            file_name = item[0]
            file_data = item[1]

            # 计算 tf_idf 与 text_rank
            extract_tags = jieba.analyse.extract_tags(file_data, topK=100, withWeight=True)
            textrank = jieba.analyse.textrank(file_data, topK=100, withWeight=True)

            res_jieba.append(extract_tags)
            res_text_rank.append(textrank)
            res_name.append(file_name)

        frame_jieba = pd.DataFrame(res_jieba, index=res_name).T
        frame_text_rank = pd.DataFrame(res_text_rank, index=res_name).T

        # 文件保存
        frame_jieba.to_csv(self.res_path_root + 'JIEBA_TF_IDF关键词结果.csv', index=False, encoding='utf-8')
        frame_text_rank.to_csv(self.res_path_root + 'JIEBA_TEXT_RANK关键词结果.csv', index=False, encoding='utf-8')

