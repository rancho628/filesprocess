# coding:utf-8

"""
DESC:   在文本预处理中，实现高效的读取文本文件
Prompt: code in Python3 env
"""

import os,time


class loadFolders(object): # 迭代器
    def __init__(self, par_path):
        self.par_path = par_path
    def __iter__(self):
        for file in os.listdir(self.par_path):
            file_abspath = os.path.join(self.par_path, file)
            #print(file_abspath)
            if os.path.isdir(file_abspath): # if file is a folder
                #若是文件夹则return
                yield file_abspath

class loadFiles(object):
    def __init__(self, par_path):
        self.par_path = par_path
    def __iter__(self):
        #调用函数，把一级目录下载下来
        #folders = loadFolders(self.par_path)
        #遍历每一个一级目录
        #for folder in folders:              # level directory
            #catg = folder.split(os.sep)[-1]
            #遍历每一个二级目录
            #print('这儿',self.par_path)
            for file in os.listdir(self.par_path):     # secondary directory
                file_path = os.path.join(self.par_path, file)
                #print(file_path)
                if os.path.isfile(file_path):
                    this_file = open(file_path, 'rb')  # rb读取方式更快
                    content = this_file.read().decode('gbk')
                    yield content
                    this_file.close()



if __name__=='__main__':
    #弄出一个绝对路径
    filepath = os.path.abspath('C:\\Users\\rancho\\PycharmProjects\\filesprocess\\legalfiles\\files2txt')
    files = loadFiles(filepath)
    for msg in files:
        print(msg)


