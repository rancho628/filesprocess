import os,re,time,jieba
import legalfiles.extracttext.batchconv
import legalfiles.extracttext.batchreadfiles
import legalfiles.extracttext.conv2txt as ET
import legalfiles.processtext.cutandremove
import legalfiles.processtext.freqword
import legalfiles.processtext.featureword
from config2 import data_txtfile_path
from operator import itemgetter
from config2 import data_file_path
import legalfiles.saveobject.savetxt

def processFile():
    # 转换文件为txt
    rootDir = data_file_path
    #print(rootDir)
    tra = legalfiles.extracttext.batchconv.TraversalFun(rootDir, ET.Files2Txt)  # 默认方法参数打印所有文件路径
    tra.ReadyTraversal()  # 遍历文件并进行相关操作

    #读取txt
    filepath = os.path.abspath(data_txtfile_path)
    files = legalfiles.extracttext.batchreadfiles.loadFiles(filepath)

    #把txt弄成一个个对象保存到数据库
    legalfiles.saveobject.savetxt.save_txt(data_txtfile_path,files);


    #要返回给view的变量
    featWords = {}
    wordlists = {}

    #对txt遍历分词
    for cont in files:
        #按段切原文本
        sent_list = cont.split('\n')
        # print('=' * 3, '原文本按段切割后', '=' * 3)
        # print(sent_list)

        #分词，content是分词完毕的结果
        content,flag = legalfiles.processtext.cutandremove.seg_doc(sent_list)
        # print('=' * 3, '分词完毕文本', '=' * 3)
        # print(content)

        # 词频统计,word是一个counter,我主要是获取他对应词语的频率，fdist是给下面用的
        words,fdist = legalfiles.processtext.freqword.nltk_wf_feature(content)
        #获取所有的不重复的词
        content_nocov = list(set(content))
        word_fre={}
        for cv in content_nocov:
            word_fre[cv]=words[cv]
        #按照词频降序排序
        sorted_word_fre=sorted(word_fre.items(),key=itemgetter(1),reverse=True)
        # print('=' * 3, '统计词频', '=' * 3)
        # print(sorted_word_fre)
        #切出10个最高频率词
        # print('=' * 3, '10个最高频率词', '=' * 3)
        # print(sorted_word_fre[0:10])

        #打印指定词频范围的词
        wordlist = legalfiles.processtext.freqword.freqword(fdist)
        # print('=' * 3, '打印词频在5~15的词', '=' * 3)
        # print(wordlist)
        wordlists.update(wordlist)

        #提取特征词
        featWord=legalfiles.processtext.featureword.extract_feature_words(content,flag)
        # print('=' * 3, '提取人名地方名等', '=' * 3)
        # print(featWord)
        featWords.update(featWord)

    # 视图要什么就返回什么到视图
    return wordlists,featWords


if __name__=='__main__':
    processFile()








