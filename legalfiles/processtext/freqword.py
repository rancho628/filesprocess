# coding:utf8

"""
DESC:NLTK词频统计
"""

from nltk import *
from legalfiles.processtext.cutandremove import seg_doc
from collections import Counter

#解决中文显示
#import matplotlib
# （1）查看当前使用字体格式
# from matplotlib.font_manager import findfont, FontProperties
# print(findfont(FontProperties(family=FontProperties().get_family())))
# （2）在C:\Windows\Fonts查找中文字体SimHei.ttf，并将其复制到../mpl-data/font/ttf文件夹下面
# (3) 设置使用字体
#matplotlib.rcParams['font.sans-serif'] = 'SimHei'


# 利用nltk进行词频特征统计
def nltk_wf_feature(word_list=None):
    # ********统计词频方法1**************
    fdist=FreqDist(word_list)
    words=Counter(word_list)

    return words,fdist

    # print('=' * 3, '统计词频', '=' * 3)
    # print(Words.keys(), '\n', Words.values())

    # print('=' * 3, '10个最高频率词', '=' * 3)
    # fdist.tabulate(10)  # 频率分布表

    # print('='*3,'指定词语词频统计','='*3)
    # w='倪利刚'
    # print(w,'出现频率：',fdist.freq(w)) # 给定样本的频率
    # print(w,'出现次数：',fdist[w]) # 出现次数

    # print('='*3,'可视化词频','='*3)
    # fdist.plot(30) # 频率分布图
    # fdist.plot(30,cumulative=True) # 频率累计图

    # print('='*3,'根据词语长度查找词语','='*3)
    # wlist =[w for w in fdist if len(w)>2]#法1
    # print(wlist)
    # wlist =[w for w in Words if len(w)>2]#法2
    # print(wlist)


def freqword(fdist):
    wordlist ={}
    for key in fdist.keys():
        if fdist.get(key)>=2 :
            wordlist[key]=fdist.get(key)
    return wordlist






if __name__=='__main__':

    pass
