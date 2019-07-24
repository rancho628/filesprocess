import os,re,time,jieba
import legalfiles.extracttext.batchconv
import legalfiles.extracttext.batchreadfiles
import legalfiles.extracttext.conv2txt as ET
import legalfiles.processtext.cutandremove
import legalfiles.processtext.freqword
import legalfiles.processtext.featureword

def processFile():
    # 转换文件为txt
    rootDir = "C:\\Users\\rancho\\PycharmProjects\\filesprocess\\legalfiles\\files"
    tra = legalfiles.extracttext.batchconv.TraversalFun(rootDir, ET.Files2Txt)  # 默认方法参数打印所有文件路径
    tra.ReadyTraversal()  # 遍历文件并进行相关操作

    #读取txt
    filepath = os.path.abspath('C:\\Users\\rancho\\PycharmProjects\\filesprocess\\legalfiles\\files2txt')
    files = legalfiles.extracttext.batchreadfiles.loadFiles(filepath)

    #对txt遍历分词
    for i,content in enumerate(files):
        #分词
        content,flag = legalfiles.processtext.cutandremove.seg_doc(content)
        print('=' * 3, '分词完毕文本', '=' * 3)
        print(content)

        # 词频统计
        fdist,words = legalfiles.processtext.freqword.nltk_wf_feature(content)
        print('=' * 3, '统计词频', '=' * 3)
        print(words.keys())
        print(words.values())
        print('=' * 3, '10个最高频率词', '=' * 3)
        print(fdist.tabulate(10))  # 频率分布表

        #去重复
        content_nocov=list(set(content))
        print('=' * 3, '去重复后文本', '=' * 3)
        print(content_nocov)

        # # 去重复后词频统计
        # processtext.FreqWord.nltk_wf_feature(content_nocov)

        #打印指定词频范围的词
        wordlist = legalfiles.processtext.freqword.freqword(fdist)
        print('=' * 3, '打印词频在2~15的词', '=' * 3)
        print(wordlist)

        #提取特征词
        featWord=legalfiles.processtext.featureword.extract_feature_words(content,flag)
        print('=' * 3, '提取人名地方名等', '=' * 3)
        print(featWord)


if __name__=='__main__':
    processFile()








