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
from legalfiles.processtext.deletefiles import deletefiles,deletefiles2txt

class Batchdealtext():
    #类变量，可供外部直接调用
    featwords =[]
    frewords=[]
    files = None

    def processfile(self):
        # 转换文件为txt
        rootDir = data_file_path
        tra = legalfiles.extracttext.batchconv.TraversalFun(rootDir, ET.Files2Txt)  # 默认方法参数打印所有文件路径
        tra.ReadyTraversal()  # 遍历文件并进行相关操作

        #读取txt
        Batchdealtext.files = legalfiles.extracttext.batchreadfiles.loadFiles(os.path.abspath(data_txtfile_path))


        #对txt遍历分词
        for cont in self.files:
            #按段切原文本，切完是个列表
            sent_list = cont.split('\n')
            # print('=' * 3, '原文本按段切割后', '=' * 3)
            # print(sent_list)

            #分词，content是分词完毕的结果，是个列表
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
            # print('=' * 3, '打印词频在2~15的词', '=' * 3)
            # print(wordlist)
            Batchdealtext.frewords.append(wordlist)


            #提取特征词
            featword=legalfiles.processtext.featureword.extract_feature_words(content,flag)
            print('=' * 3, '提取人名地方名等', '=' * 3)
            print(featword)
            Batchdealtext.featwords.append(featword)


    def clear(self):
        #清空类变量
        Batchdealtext.featwords=[]
        Batchdealtext.frewords=[]
        files = None









if __name__=='__main__':
    pass








