import pandas as pd
import os
import math
import jieba.analyse

doc_path = '/Users/mahao/PycharmProjects/myApp/obj_text/词频结果/'
doc_list = os.listdir(doc_path)

data = []
jieba_data = []

# 读取文件
for item in doc_list:
    f = open(doc_path + item, 'r')

    word_pair = []

    for line in f:
        word_pair.append(line.replace('\n', '').split(','))

    # 获取各个文章关键词
    data.append([item.replace('.csv', ''), [word[0] for word in word_pair]])

# 遍历全部文件获取共现关键词
res_count = []
res_content = []

for i in data:
    tmp_count = []
    tmp_content = []
    for j in data:
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

name_file = [x[0] for x in data]
count_frame = pd.DataFrame(res_count, index=name_file, columns=name_file)
content_frame = pd.DataFrame(res_count, index=name_file, columns=name_file)

# for item in doc_list:
#     f = open(doc_path + item, 'r')
#     word_pair = []
#
#     for line in f:
#         word_pair.append(line.replace('\n', '').split(','))
#
#     # 计算词频并写入字典
#     tmp_fre_sum = sum([int(x[1]) for x in word_pair])
#     word_fre_dict = {}
#     content = []
#     for word in word_pair:
#         word_fre_dict[word[0]] = int(word[1]) / tmp_fre_sum
#         content.append(word[0])
#
#     data.append([item.replace('.csv', ''), word_fre_dict])
#     jieba_data.append([item.replace('.csv', ''), ",".join(content)])

#
# def helper(target_key):
#     tmp = 0
#     dict_list = [x[1] for x in data]
#
#     for x in dict_list:
#         if target_key in x:
#             tmp += 1
#
#     return tmp
#
#
# total_dco_num = len(data)
#
#
# # 计算TF-IDF 并保存
# res_root = []
# res_root_name = []
# for item in data:
#     file_name = item[0]
#     file_data = item[1]
#
#     res = {}
#
#     for k, v in file_data.items():
#         i = helper(target_key=k)
#         res[k] = v * math.log(total_dco_num / i)
#
#     res_root.append([(k, v) for k, v in res.items()])
#     res_root_name.append(file_name)
#
# frame = pd.DataFrame(res_root, index=res_root_name).T
#
# # 使用结巴计算相关结果
# res_jieba = []
# res_name = []
# for my_file in jieba_data:
#     file_name = my_file[0]
#     file_data = my_file[1]
#
#     # 计算 tf_idf 与 text_rank
#     extract_tags = jieba.analyse.textrank(file_data, topK=100, withWeight=True)
#     print(file_name)
#
#     res_jieba.append(extract_tags)
#     res_name.append(file_name)
#
# data_frame = pd.DataFrame(res_jieba, index=res_name)
#
#
#


