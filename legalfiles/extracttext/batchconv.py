# coding=utf-8

"""
Description: 批量文档格式自动转化为txt
"""

import legalfiles.extracttext.conv2txt as ET

import os,time


'''
功能描述：遍历目录，对子文件单独处理
参数描述：1 rootDir 根目录  2 func：方法参数  3 saveDir: 保存路径
'''
class TraversalFun():
    # 1 初始化
    def __init__(self,rootDir,func=None,saveDir=""):
        self.rootDir = rootDir # 目录路径
        self.func = func   # 参数方法
        self.saveDir = saveDir # 保存路径

    # 2 遍历目录准备工作
    def ReadyTraversal(self):
        # 切分路径：目录+文件名
        dirs,latername = os.path.split(self.rootDir)
        #print('传进来的根目录：',self.rootDir,' 前面：',dirs,' 后面：',latername)

        # 保存目录
        save_dir = ""
        if self.saveDir=="":
            #这里把它变成绝对路径,下面根据绝对路径才能创建
            save_dir = os.path.abspath(os.path.join(dirs,latername+'2Txt'))
        else:
            save_dir = self.saveDir
        # 创建保存目录
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        #print("保存目录："+save_dir)

        # 遍历传进来的路径，递归转化txt文件
        TraversalFun.TraversalDir(self,self.rootDir,save_dir)


    # 3 递归遍历所有文件，并提供具体文件操作功能
    def TraversalDir(self,rootDir,save_dir=''):
        # 返回指定目录包含的文件或文件夹的名字的列表
        for lists in os.listdir(rootDir):
            # 待处理文件夹名字集合
            path = os.path.join(rootDir, lists)

            # 若是文件，对单个文件进行转化为txt格式且，保存在save_dir
            if os.path.isfile(path):
                self.func(os.path.abspath(path),os.path.abspath(save_dir))

            # 若是目录，继续递归遍历
            if os.path.isdir(path):
                #拼成一个新的目录，并且创建该目录
                newpath = os.path.join(save_dir, lists)
                if not os.path.exists(newpath):
                    os.mkdir(newpath)
                TraversalFun.TraversalDir(self,path,newpath)




if __name__ == '__main__':
    # # 打开文件
    # path = "..\\files"
    # dirs = os.listdir(path)
    # # 输出所有文件和文件夹
    # for file in dirs:
    #     print(os.path.abspath(file),'\n')
    #     print(file,'\n')

    #根目录文件路径
    rootDir = "C:\\Users\\rancho\\PycharmProjects\\filesprocess\\legalFfiles\\files"
    tra=TraversalFun(rootDir,ET.Files2Txt)
    tra.ReadyTraversal()
