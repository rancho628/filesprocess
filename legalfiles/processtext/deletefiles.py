import os
from config2 import data_file_path
from config2 import data_txtfile_path

#循环删除文件功能
def deletefiles():
    for f in os.listdir(data_file_path):
        if os.path.exists(os.path.join(data_file_path, f) ):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(os.path.join(data_file_path, f))
            # os.unlink(path)
        else:
            print('no such file:%s' % os.path.join(data_file_path, f))  # 则返回文件不存在

def deletefiles2txt():
    for f in os.listdir(data_txtfile_path):
        if os.path.exists(os.path.join(data_txtfile_path, f)):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(os.path.join(data_txtfile_path, f))
            # os.unlink(path)
        else:
            print('no such file:%s' % os.path.join(data_txtfile_path, f))  # 则返回文件不存在

if __name__=='__main__':
  deletefiles2txt()
