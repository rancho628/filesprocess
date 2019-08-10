# coding:utf8

"""
DESC:自定义提前特征词：人名、地名、机构名等

"""

import jieba.posseg as ps
import jieba

# 不同业务场景:评论情感判断，可以自定义特征抽取规则.
def extract_feature_words(content,flag):
    featWord ={}
    #stwlist = get_stop_words()
    user_pos_list = [ 'ns']#, 'nr','nt','nz']  # 用户自定义特征词性列表
    for i in range(content.__len__())[:]:
        # 过滤掉停用词
        #if word not in stwlist and pos in user_pos_list:
        if flag[i] in user_pos_list:
            #追加
            if content[i] not in featWord:
                featWord[content[i]]=flag[i]
    return featWord



if __name__=='__main__':
  pass