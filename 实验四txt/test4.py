# -*- coding:utf-8 -*-

import os
import jieba
import jieba.analyse
import numpy as np
import streamlit as st

text = " "


def getSingle(s, k):
    """
    将字符串分为长度为k的子串，统计子串出现的次数
    :param s: 字符串
    :param k: 子串的长度
    :return: 返回字典
    """
    dic = dict()  # 定义一个字典
    for i in range(len(s) - k + 1):
        s1 = s[i:i + k]  # 对句子进行切分
        j = dic.get(s1)
        if j is not None:
            # 如果长度为k的子串在字典中统计
            # value += 1
            dic[s1] += 1
        else:
            # 如果没有出现过就是None
            # value = 1
            dic[s1] = 1
    return dic


def getSimilarity(s1, s2, k):
    """
    查询两段文本的相似度
    :param s1: 文本1
    :param s2: 文本2
    :param k: 切分的字串长度
    :return: 返回两个文本的相似度
    """
    if s1 == s2:
        return 1
    set1 = set()  # 定义一个集合
    profile1 = getSingle(s1, k)
    profile2 = getSingle(s2, k)
    for i in profile1.keys():  # 将子串添加到集合中，因为集合不会重复出现
        set1.add(i)
    set2 = set()
    for i in profile2.keys():
        set2.add(i)
    # print(set1)
    # print(set2)
    # print(set1 & set2)
    return 1.0 * len(set1 & set2) / len(set1 | set2)


def get_sameStr(s1, s2):
    # text.delete(1.0, tkinter.END)
    """
    获得文本中重复的字符串
    :param s1: 文档1
    :param s2: 文档2
    """
    global text
    text = " "
    res1 = []
    for x in s1:
        if x in s2:
            res1.append(x)
            # text.insert('end', x + "", "tag_1")
            text += '''<font color=red>''' + x + '''</font>'''
        else:
            # self.text.insert('insert', x + "")
            text += x
    # text.insert('insert', "\n")
    # self.text += '\n'
    for x in s2:
        if x in s1:
            res1.append(x)
            # text.insert('end', x + "", "tag_1")
            text += '''<font color=red>''' + x + '''</font>'''
        else:
            # text.insert('insert', x + "")
            text += x
    # text.insert('insert', "\n")

    # print("重复字符串为：", end="")
    # print(res1)


# 获取字符串对应的hash值
class SimhashStr():
    def __init__(self, str):
        self.str = str

    # 得到输入字符串的hash值
    def get_hash(self):
        # 结巴分词
        seg = jieba.cut(self.str)
        # 取前20个关键词
        keyword = jieba.analyse.extract_tags('|'.join(seg), topK=20, withWeight=True, allowPOS=())
        keyList = []
        # 获取每个词的权重
        for feature, weight in keyword:
            # 每个关键词的权重*总单词数
            weight = int(weight * 20)
            # 获取每个关键词的特征
            feature = self.string_hash(feature)
            temp = []
            # 获取每个关键词的权重
            for i in feature:
                if i == '1':
                    temp.append(weight)
                else:
                    temp.append(-weight)
                keyList.append(temp)
        # 将每个关键词的权重变成一维矩阵
        list1 = np.sum(np.array(keyList), axis=0)
        # 获取simhash值
        simhash = ''
        for i in list1:
            # 对特征标准化表示
            if i > 0:
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash

    def string_hash(self, feature):
        if feature == "":
            return 0
        else:
            # 将字符转为二进制，并向左移动7位
            x = ord(feature[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            # 拼接每个关键词中字符的特征
            for c in feature:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(feature)
            if x == -1:
                x = -2
            # 获取关键词的64位表示
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            return str(x)


# 比较两个字符串的相似度
class simliary():
    def __init__(self, sim1, sim2):
        self.sim1 = sim1
        self.sim2 = sim2

    # 比较两个simhash值的相似度
    def com_sim(self):
        # 转为二进制结构
        t1 = '0b' + self.sim1
        t2 = '0b' + self.sim2
        n = int(t1, 2) ^ int(t2, 2)
        # 相当于对每一位进行异或操作
        i = 0
        while n:
            n &= (n - 1)
            i += 1
        return i


# 比较大量文本中数据之间的相似度
class com_file_data_sim:
    def __init__(self, path):
        self.path = path

    # 获取文件中的数据列表
    def get_file_data(self):
        content_txt = []
        with open(self.path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                content = line.strip()
                content_txt.append(content)
        return content_txt

    # 对列表中的数据进行hash值比对
    def com_data_sim(self):
        global text
        text = " "
        content_data = self.get_file_data()
        # print(content_data)
        for i in range(len(content_data) - 1):
            for y in range(i + 1, len(content_data)):
                str1 = content_data[i]
                str2 = content_data[y]
                sim1 = SimhashStr(str1).get_hash()
                sim2 = SimhashStr(str2).get_hash()
                sim = simliary(sim1, sim2).com_sim()
                st.success("文本1")
                st.write(str1)
                st.success("文本2")
                st.write(str2)
                st.info("simhash:" + str(sim))
                # print(str1)
                # print(str2)
                # text.insert('insert', str(sim))
                # print('simhash值为：' + str(sim))


def t4_run1():
    """给定两个文本串，设置不同的K值，计算它们的k-shingle集合，
       并进行相似度计算；
       分析不同的k值对相似度的影响
       r（A,B） = |S(A) and S(B)|  /  |S(A) or S(b)|"""
    text1 = "重庆理工大学在重庆市，是一个美丽的大学。"
    text2 = "重庆市有一个美丽的大学，叫重庆理工大学。"
    # 测试
    k_single1 = getSingle(text1, 2)
    k_single2 = getSingle(text2, 2)
    similarity = getSimilarity(text1, text2, 1)

    st.write("文本串1的k_single:" + str(k_single1))
    st.write("文本串2的k_single:" + str(k_single2))
    st.write("文本相似度" + str(similarity))
    # print(similarity)


def t4_run2():
    """利用K-shingle算法，计算两个给定文档的相似度，
       查找重复字符串，并将重复字符串高亮显示出来"""
    cur_path = os.path.dirname(os.path.realpath(__file__))
    fp = open("/app/se/实验四txt/1.txt", 'r', encoding='utf-8')
    text1 = fp.read()
    st.text("文档1内容为：" + text1)
    fp.close()
    fp = open("/app/se/实验四txt/2.txt", 'r', encoding='utf-8')
    text2 = fp.read()
    st.text("文档2内容为：" + text2)
    fp.close()
    result = getSimilarity(text1, text2, 2)
    st.write("两个文本的像帝都为：" + str(result))
    # get_sameStr(text1, text2)
    # st.write(text)


def t4_run3():
    max_similarity = 0.2  # 指定阈值
    # """一对多文档查重"""
    global text
    text = " "
    cur_path = os.path.dirname(os.path.realpath(__file__))
    fp = open("/app/se/实验四txt/test", 'r', encoding='utf-8')
    des = fp.read()  # 指定文件

    path = cur_path + "\\文件"  # 指定路径
    # dirpath:目录的路径
    # dirnames:目录下所有存在的目录的名称
    # filenames:目录路径下所有文件的名称
    for dirpath, dirnames, filenames in os.walk(path):
        # print(dirpath, dirnames, filenames)
        if filenames is not None:
            if dirnames is not None:
                for i in filenames:
                    # print(dirpath+'\\'+i)
                    fp = open(dirpath + '\\' + i, 'r', encoding='utf-8')
                    s = fp.read()
                    st.success(s)
                    result = getSimilarity(des, s, 2)  # 查重率
                    # if result >= max_similarity:
                    # text.insert('insert', "查重率为：" + str(result) + "\n")
                    # text.insert('insert', "文档路径：" + dirpath + '\\' + i + "\n")
                    text += "查重率为：" + str(result)
                    st.text("文档名称：" + dirpath + "\\" + i)
                    st.text("查重率为：" + str(result))
                    # print(getSimilarity(des, s, 2))
                    # st.markdown(get_sameStr(des, s), unsafe_allow_html=True)
                    fp.close()


# if st.button("get"):
#     run1()
# if st.button("get2"):
#     run2()
# if st.button("get3"):
#     run3()
# if st.button("get"):
#     com_file_data_sim('sanguo.txt').com_data_sim()
    # print(getSimilarity(text1, text2, 2))
    # Button(root, text="一对一文档查重", width=10, command=fun2).grid(row=0, column=0, sticky=W)
    #
    # """扩展实验：对给定的一个文档，计算它和某路径下的所有文档的相似度
    #    将相似度高于某阈值的文档名称和重复内容显示出来"""
    # max_similarity = 0.2
    # Button(root, text="一对多文档查重", width=15, command=fun3).grid(row=0, column=0, sticky=N)
    #
    # """自己编写I-match和simhash方法的代码
    #    并对选定的文档进行相似度计算，对结果进行对比"""
    # Button(root, text="simhash", width=15, command=com_file_data_sim('sanguo.txt').com_data_sim).grid(row=0, column=0,
    #                                                                                                   sticky=E)
    # # com_file_data_sim('sanguo.txt').com_data_sim()
    #
    # mainloop()
