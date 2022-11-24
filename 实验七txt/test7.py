import math
import os

import chardet
import jieba
import re
import codecs
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from scipy import spatial
import jieba.analyse
import streamlit as st


def fenci(s):
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


def proceed(texts):
    """统计各个文章中单词"""
    docs = []  # [[ ], [ ],……]
    for text in texts:
        doc = fenci(text)  # 预处理+分词处理
        docs.append(doc)  # 将分词结果放入列表中
    return docs


def tf(docs):
    """统计各个文档中单词在本文档中出现的次数"""
    docv = []  # [{},{}……]：存放各个文档中单词出现的频率
    for i, doc in enumerate(docs):  # 同时获得索引和值
        vec = {}
        for word in doc:
            if word not in vec:
                vec[word] = 1
            else:
                vec[word] += 1
        docv.append(vec)
    return docv


def idf(docs):
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
        idf_word[word] = math.log2(docs_count / word_idf[word])
    return idf_word


def get_tf_idf(docs, docv, idf_word):
    tf_idf = []
    length = len(idf_word)
    for i in range(0, len(docs)):
        temp = []
        for word in idf_word:
            if word not in docs[i]:
                temp.append(0)
            else:
                temp.append(docv[i][word] * idf_word[word])
        tf_idf.append(temp)
    return tf_idf


def t7_run1():
    text = ["我喜欢苹果，你喜欢吗？",
            "每天一个苹果，医生远离你",
            "永远不要拿苹果和橘子比较",
            "相对于橘子而言，我更喜欢苹果"]
    docs = proceed(text)
    # print(docs)
    st.text(docs)
    docv = tf(docs)
    # print(docv)
    st.text(docv)
    idf_word = idf(docs)
    # print(idf_word)
    st.text(idf_word)
    tf_idf = get_tf_idf(docs, docv, idf_word)
    for i in range(len(tf_idf)):
        # print(tf_idf[i])
        st.text(tf_idf[i])


def convert(filename, out_enc='UTF-8'):
    content = codecs.open(filename, 'rb').read()
    source_encoding = chardet.detect(content)['encoding']  # 检测文本的编码
    content = content.decode(source_encoding).encode(out_enc)  # 将文本转换为utf-8格式
    codecs.open(filename, 'wb').write(content)


def fenci2(file, path):
    sFilePath = './segfile1'
    fp = open(file, 'r', encoding='utf-8')


def t7_run2():
    """scikit-learn库来计算TFIDF"""
    corpus = ["我 喜欢 苹果 你 喜欢 吗",
              "每天 一个 苹果 医生 远离 你",
              "永远 不要 拿 苹果 和 橘子 比较",
              "相对 于 橘子 而言 我 更 喜欢 苹果"]
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        st.text("-------这里输出第" + str(i) + "类文本的词语tf-idf权重------")
        temp = " "
        for j in range(len(word)):
            temp += word[j] + str(weight[i][j]) + "/"
        st.write(temp)


def t7_run3():
    """利用tf-idf和余弦相似度计算文本的相似度
    并对文本进行排序"""
    # 1.读取文本内容
    file_list = []
    cur_path = os.path.dirname(os.path.realpath(__file__))
    for i in range(1, 12):
        fp = open(cur_path + '\\20篇文章\\' + str(i) + '.txt', 'r', encoding='utf-8')
        content = fp.read()
        file_list.append(content)

    # 2.利用tf_idf抽取文章中的关键词
    docs = proceed(file_list)
    # print(docs)
    st.text(docs)
    docv = tf(docs)
    # print(docv)
    st.text(docv)
    idf_word = idf(docs)
    sorted(idf_word.items(), key=lambda x: x[1], reverse=True)
    key_word = []
    num = 0
    for word in idf_word:
        num += 1
        key_word.append(word)
        if num == 20:
            break

    # 3.获得文章各自的词频向量
    xiangliang = []
    for i in range(0, len(docs)):
        temp = []
        for word in key_word:
            if word in docs[i]:
                temp.append(docv[i][word])
            else:
                temp.append(0)
        xiangliang.append(temp)

    # 4、利用余弦定理计算文本相似度
    result = []
    text1 = xiangliang[len(docs) - 1]
    for i in range(0, len(docs) - 1):
        res = 1 - spatial.distance.cosine(text1, xiangliang[i])
        result.append(res)

    # 5、打印结果,并对文本进行排序
    # print(result)
    st.write(result)
    b = sorted(enumerate(result), key=lambda r: r[1], reverse=True)
    c = [x[0] for x in b]
    # print(c)
    st.text(c)


class Simhash(object):
    def simhash(self, content):
        keylist = []
        # jieba分词
        seg = jieba.cut(content)
        # 去除停用词
        # jieba.analyse.set_stop_words("stopwords.txt")
        # 得到前20个分词和tf-idf权值
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=20, withWeight=True, allowPOS=())
        # print(keywords)
        for feature, weight in keywords:
            # print(weight)
            weight = int(weight * 20)
            # print(weight)
            # print("k=" + feature)
            feature = self.string_hash(feature)
            # print("v=" + feature)
            temp = []
            for i in feature:
                if i == "1":
                    temp.append(weight)
                else:
                    temp.append(-1 * weight)
            keylist.append(temp)

        list1 = np.sum(np.array(keylist), axis=0)
        if not keylist:
            return "00"
        simhash = ""
        # 降维处理
        for i in list1:
            if i > 0:
                simhash += "1"
            else:
                simhash += "0"
        return simhash

    def string_hash(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
        return str(x)


def hammingDis(s1, s2):
    t1 = "0b" + s1
    t2 = "0b" + s2
    n = int(t1, 2) ^ int(t2, 2)
    i = 0
    while n:
        n &= (n - 1)
        i += 1
    max_hashbit = max(len(bin(int(t1, 2))), len(bin(int(t2, 2))))
    sim = i / max_hashbit
    return sim


def t7_run4():
    text1 = "打南边来了个哑巴，腰里别了个喇叭;"
    text2 = "打南边来了个哑巴"
    text3 = "腰里别了个喇叭; "
    st.write("文本1 : " + text1)
    st.write("文本2 : " + text2)
    st.write("文本3 : " + text3)
    s1 = Simhash()
    t1_hash = s1.simhash(text1)
    t2_hash = s1.simhash(text2)
    t3_hash = s1.simhash(text3)

    sim1 = hammingDis(t1_hash, t2_hash)
    sim2 = hammingDis(t1_hash, t3_hash)
    # print(sim1)
    st.success("文本1和文本2的相似度： " + str(sim1))
    st.success("文本1和文本2的相似度： " + str(sim2))
    # print(sim2)


# if __name__ in '__main__':
#     choice = input("1、计算TF-IDF\n"
#                    "2、scikit-learn库来计算TFIDF\n"
#                    "3、余弦相似度计算文本相似度\n"
#                    "4、simhash算法\n"
#                    "请选择：")
#     if choice == '1':
#         fun1()
#     elif choice == '2':
#         fun2()
#     elif choice == '3':
#         fun3()
#     else:
#         pro1()
#     # text = "信息检索中的模型有向量空间模型"
#     # print(jieba.lcut(text))

