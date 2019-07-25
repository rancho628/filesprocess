import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))  # 获取项目根目录

# print(PROJECT_ROOT)
data_dictfile_path = os.path.join(PROJECT_ROOT, "legalfiles/need/dict.txt.big")  # dict文件路径
# print(data_dictfile_path)
data_stopfile_path = os.path.join(PROJECT_ROOT, "legalfiles/need/stopword.txt")  # stop文件路径
# print(data_stopfile_path)
data_txtfile_path = os.path.join(PROJECT_ROOT, "legalfiles/files2txt")  # txt文件路径
# print(data_txtfile_path)
data_file_path = os.path.join(PROJECT_ROOT, "legalfiles/files")  # file文件路径
# print(data_file_path)