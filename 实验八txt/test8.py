import os
import re
import jieba.analyse
import string

import jieba
import math
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import streamlit as st


class MYTfIdf:
    def __init__(self, s):
        self.s = s

    def fenci(self, s):
        """每一行代表一个文档内容，移除不需要的字符"""
        line1 = s.replace(' ', '')  # 去掉文本中的空格
        pattern = re.compile("[^\u4e00-\u9fa5^a-z^A-Z]")  # 只保留中英文、数字，去掉符号
        line2 = re.sub(pattern, '', line1)  # 把文本中匹配到的字符替换成空字符
        seg_list = jieba.cut(line2)

        result = []
        for seg in seg_list:
            seg = ''.join(seg.split())
            if seg != '，' and seg != '？' and seg != '。' and seg != '\n' and seg != '\n\n':
                result.append(seg)
        return result

    def tf(self, cut_s):
        """统计每个文本中国每个单词出现的次数"""
        docv = []  # [{},{}……]：存放各个文档中单词出现的频率
        for i, doc in enumerate(cut_s):  # 同时获得索引和值
            vec = {}
            for j, word in enumerate(doc):
                if word not in vec:
                    vec[word] = 1
                else:
                    vec[word] += 1

            for key, value in vec.items():
                vec[key] = value / len(doc)
            docv.append(vec)
        return docv

    def idf(self, docs):
        """计算idf"""
        word_idf = {}
        for i, doc in enumerate(docs):
            for word in doc:
                if word not in word_idf:
                    word_idf[word] = []
                    word_idf[word].append(i)
                else:
                    word_idf[word].append(i)
        for key in word_idf:
            word_idf[key] = len(set(word_idf[key]))  # 去掉重复的文档，计算每个单词在多少个文档中出现

        idf_word = {}
        docs_count = len(docs)  # 文档个数
        for word in word_idf:
            idf_word[word] = math.log(docs_count / word_idf[word] + 1)
        return idf_word

    def get_tf_idf(self, docs, docv, idf_word):
        tf_idf = {}
        for i in range(0, len(docs)):
            for word in idf_word:
                if word not in docs[i]:
                    tf_idf[word] = 0
                else:
                    tf_idf[word] = (docv[i][word] * idf_word[word])
        return tf_idf

    def getTfIdfValue(self):
        if self.s:
            docs = []
            for v in self.s:
                docs.append(self.fenci(v))
            # print(docs)
            docv = self.tf(docs)
            # print(docv)
            idf_word = self.idf(docs)
            # print(idf_word)
            tf_idf = self.get_tf_idf(docs, docv, idf_word)
            return tf_idf


# 生成构造类
class hhh:
    def __int__(self, data, kv):
        self.data = data[0]
        self.tfidf = MYTfIdf(data)
        self.kv = kv  # 初始化设置窗口大小

    def s_match(self, s, s1):
        """匹配词语出现的位置"""
        loc = list()
        l_s = len(s)
        for k in s1:
            temp = []
            l_s1 = len(k)
            for i in range(l_s - l_s1 + 1):
                index = i
                for j in range(l_s1):
                    if s[index] == k[j]:
                        index += 1
                    else:
                        break
                if index - i == l_s1:
                    temp.append(i)
            loc.extend(temp)
        return sorted(loc)

    def getShingle(self, locList):
        """拆分得窗口信息"""
        textLine = list()
        data = ''.join(self.data)
        for v in locList:
            temp = [data[v:v + self.kv]]
            textLine.append(temp)
        # print("得到的窗口信息", textLine)
        return textLine

    def getScore(self, tfidfV, shingles, keywords):  # tfidf的值，生成的窗口信息,关键词列表
        """给生成的每段窗口打分"""
        score = dict()  # 每一窗口的分数字典
        for i, v in enumerate(shingles):
            if not score.get(i):
                score[i] = 0  # 每一段初始化是0
            for keyw in keywords:  # 对于每个关键词
                if keyw in (''.join(v)):
                    score[i] += ''.join(v).count(keyw) * tfidfV[keyw]  # count是计数
            # print("得分为：", end="")
            # print(score[i])
        # 将字典排序
        sortedDic = sorted(score.items(), key=lambda t: t[1], reverse=True)  # 排序方法
        # print('窗口得分', sortedDic)
        return sortedDic

    def getResult(self, keywords):
        """返回摘要的结果"""
        _keywords = keywords.split(' ')  # 先按空格分开
        tfidfV = self.tfidf.getTfIdfValue()  # 先算tfidf的分数
        # print('tfidf的分数', tfidfV)
        locList = self.s_match(''.join(self.data), _keywords)  # 得到每个查询词的位置
        # print(locList)
        txtLine = self.getShingle(locList)  # 根据位置对文档进行窗口滑动切分
        scores = self.getScore(tfidfV, txtLine, _keywords)  # 得到每个窗口的分数
        maxShinge = txtLine[scores[0][0]]  # 返回得分最大的窗口
        return maxShinge


def t8_run1():
    result = hhh()
    result.data = [
        "搜索引擎包含了各个学科的概念和知识，这些学科包含了计算机科学、数学、心理学等。特别是数学几乎在搜索引擎的各个系统都大量使用，例如布尔代数、概率论、数理统计等，这些数学知识的应用为搜索引擎解决了一个个的难题，最终使得搜索技术走向成熟。", ]
    result.kv = 40
    st.write(str(result.data))
    keyword = "搜索引擎 数学"
    result.tfidf = MYTfIdf([
        "搜索引擎包含了各个学科的概念和知识，这些学科包含了计算机科学、数学、心理学等。特别是数学几乎在搜索引擎的各个系统都大量使用，例如布尔代数、概率论、数理统计等，这些数学知识的应用为搜索引擎解决了一个个的难题，最终使得搜索技术走向成熟。"])
    # print(result.getResult(keyword))
    st.success("关键句为：" + str(result.getResult(keyword)))


def get_keyword(text):
    fenci_text = jieba.cut(text)
    # print("/ ".join(fenci_text))

    # 第二步：去停用词
    # 这里是有一个文件存放要改的文章，一个文件存放停用表，然后和停用表里的词比较，一样的就删掉，最后把结果存放在一个文件中
    cur_path = os.path.dirname(os.path.realpath(__file__))
    stopwords = {}.fromkeys([line.rstrip() for line in open('/app/se/实验八txt/stopwords.txt', encoding='utf-8')])
    final = ""
    for word in fenci_text:
        if word not in stopwords:
            if word != "。" and word != "，":
                final = final + " " + word
    # print(final)

    # 第三步：提取关键词
    a = jieba.analyse.extract_tags(text, topK=3, withWeight=True, allowPOS=())
    keyword = ""
    flag = 0
    for i in a:
        flag += 1
        if flag != 3:
            keyword += i[0] + " "
        else:
            keyword += i[0]
    return keyword


def t8_run2():
    cur_path = os.path.dirname(os.path.realpath(__file__))
    for i in range(10, 15):
        fp = open("/app/se/实验八txt/体育/" + str(i) + '.txt', 'r',
                  encoding='ansi')
        content = fp.read()
        st.write(content)
        fp.close()
        result = hhh()
        date = [content]
        result.data = date
        result.kv = 70
        keyword = get_keyword(content)
        result.tfidf = MYTfIdf(date)
        st.success("关键句为：" + str(result.getResult(keyword)))


def keysentences_extraction(text):
    tr4s = TextRank4Sentence()
    tr4s.analyze(text, lower=True, source='all_filters')
    # text    -- 文本内容，字符串
    # lower   -- 是否将英文文本转换为小写，默认值为False
    # source  -- 选择使用words_no_filter, words_no_stop_words, words_all_filters中的哪一个来生成句子之间的相似度。
    # 		  -- 默认值为`'all_filters'`，可选值为`'no_filter', 'no_stop_words', 'all_filters'
    # sim_func -- 指定计算句子相似度的函数

    # 获取最重要的num个长度大于等于sentence_min_len的句子用来生成摘要
    keysentences = tr4s.get_key_sentences(num=1, sentence_min_len=6)
    return keysentences


def t8_run3():
    cur_path = os.path.dirname(os.path.realpath(__file__))
    for i in range(10, 15):
        fp = open("/app/se/实验八txt/体育/" + str(i) + '.txt', 'r',
                  encoding='ansi')
        content = fp.read()
        st.write(content)
        fp.close()
        keysentences = keysentences_extraction(content)
        st.success(keysentences)


