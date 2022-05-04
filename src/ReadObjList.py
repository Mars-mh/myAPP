"""
获取项目列表
"""
import os


class ReadObjList:
    def __init__(self, path):
        self.listdir = os.listdir(path)

    def get_obj_list(self):
        return filter(lambda x: '.txt' in x, self.listdir)

