# coding:utf8

"""
DESC:分词
"""
import os
import re,jieba,sys
import jieba.posseg as ps
from config2 import data_dictfile_path
from config2 import data_stopfile_path

# 加载自定义分词词典
jieba.load_userdict(data_dictfile_path)


#********************1 结巴中文分词***********************************

# 先清洗，然后利用jieba进行分词，再去除停用词，返回切词后的list
def seg_doc(sent_list):

    # map内置高阶函数:一个函数f和list，函数f依次作用在list.
    # 这个函数功能就是：正则处理，去掉一些字符，例如\u3000
    sent_list = map(textParse, sent_list)

    # 2 获取停用词
    stwlist = get_stop_words()

    # 3 一段一段地，先分词+再去除停用词
    #word_2dlist = [rm_tokens(ps.cut(part),stwlist) for part in sent_list]
    word_2dlist=[]
    flag_2dlist=[]
    for part in sent_list:
        #先分词 + 再去除停用词
        word_1dlist,flag_1dlist=rm_tokens(ps.cut(part),stwlist)#jieba.cut(part, cut_all=False)
        word_2dlist.append(word_1dlist)
        flag_2dlist.append(flag_1dlist)

    # 4 把一段一段的分词结果（列表的列表）合并到一个列表里
    word_list = sum(word_2dlist, [])
    flag_list = sum(flag_2dlist, [])
    return word_list,flag_list


# 正则对字符串清洗掉一些字符
def textParse(str_doc):
    # 正则过滤掉特殊符号、标点、英文、数字等。

    #可以去掉中文逗号
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:：;；|<=>?@，—。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    str_doc=re.sub(r1, ' ', str_doc)

    # 去掉字符
    str_doc = re.sub('\u3000', '', str_doc)

    # 去除空格
    #str_doc=re.sub('\s+', ' ', str_doc)

    # 去除换行符
    # str_doc = str_doc.replace('\n',' ')

    return str_doc

# 创建停用词列表
def get_stop_words(path=data_stopfile_path):
    file = open(path, 'r',encoding='utf-8').read().split('\n')
    return set(file)

# 去掉一些停用词和没用字符（很有必要）
def rm_tokens(mywords,stwlist):
    #字典变列表
    mywords = list(mywords)
    stop_words = stwlist

    words = []
    flags = []
    for word, flag in mywords:
        words.append(word)
        flags.append(flag)

    for i in range(words.__len__())[::-1]:
        if words[i] in stop_words: # 去除停用词
            words.pop(i)
            flags.pop(i)
        elif words[i].isdigit(): # 去除数字
            words.pop(i)
            flags.pop(i)
        elif len(words[i]) == 1:  # 去除单个字符
            words.pop(i)
            flags.pop(i)
        elif words[i] == " ":  # 去除空字符
            words.pop(i)
            flags.pop(i)
    return words,flags




if __name__=='__main__':

    print(range(10)[::-1])


