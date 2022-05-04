"""
创建文档相似度矩阵
"""
import os
import pandas as pd


class GetAdjMatrix:
    def __init__(self, doc_path):
        # 基本路径
        self.doc_path = doc_path  # 文件根目录
        self.doc_list = os.listdir(doc_path)  # 文件列表

        # 创建保存内容地址
        self.res_path_root = doc_path.replace('词频结果/', '') + '项目共现词统计结果/'
        try:
            os.mkdir(self.res_path_root)
        except FileExistsError:
            pass

        self.data = []  # 各个文本词频表

    def get_adj_matrix(self):
        # 读取文件
        for item in self.doc_list:
            f = open(self.doc_path + item, 'r')

            word_pair = []

            for line in f:
                word_pair.append(line.replace('\n', '').split(','))

            # 获取各个文章关键词
            self.data.append([item.replace('.csv', ''), [word[0] for word in word_pair]])

        # 遍历全部文件获取共现关键词
        res_count = []
        res_content = []

        for i in self.data:
            tmp_count = []
            tmp_content = []

            for j in self.data:
                if i == j:
                    tmp_count.append(0)
                    tmp_content.append('null')
                    pass
                else:
                    intersection_list = list(set(i[1]).intersection(set(j[1])))
                    tmp_content.append(intersection_list)
                    tmp_count.append(len(intersection_list))

            res_count.append(tmp_count)
            res_content.append(tmp_content)

        # 保存文件
        name_file = [x[0] for x in self.data]
        count_frame = pd.DataFrame(res_count, index=name_file, columns=name_file)
        content_frame = pd.DataFrame(res_content, index=name_file, columns=name_file)

        content_frame.to_csv(self.res_path_root + '文章间关键词共现内容.csv', index=True, header=True, encoding='gb2312')
        count_frame.to_csv(self.res_path_root + '文章间关键词共现数量.csv', index=True, header=True, encoding='gb2312')

