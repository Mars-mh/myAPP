"""
读取停用词并返回列表
"""


class ReadWords:
    def __init__(self, path):
        self.path = path

    def get_words_list(self):
        """
        获取词列表
        :return: list
        """
        return [line.strip() for line in open(self.path, encoding='UTF-8').readlines()]
