import os

import jieba
import re
import jieba.posseg as pseg
import streamlit as st
import pandas as pd

class Word:
    word = None
    num = 0
    place = None

    def __init__(self, word):
        self.word = word
        self.place = []


def t6_run1():
    """结巴分词统计词频和词语出现的位置"""
    cur_path = os.path.dirname(os.path.realpath(__file__))
    filename1 = "\\结巴.txt"
    fp1 = open(cur_path + filename1, 'r', encoding='utf-8')
    article1 = fp1.read()
    fp1.close()
    list1 = jieba.lcut(article1)  # 列表
    set1 = set(list1)  # 集合
    words = dict()  # 字典
    for s in set1:
        words[s] = Word(s)
    start = 0
    for ar in list1:
        words[ar].num += 1
        words[ar].place.append(start)
        start += len(ar)
    newwords = []
    for w in words.values():
        newwords.append(w)

    fp = open(cur_path + '\\test1.txt', 'w', encoding='utf-8')
    for w in newwords:
        fp.write(w.word + ':')
        fp.write('[' + str(w.num) + '] ')
        fp.write(str(w.place) + '\n')
        # print(w.word)
        # print(w.num)
        # print(w.place)
        st.text(w.word + str(w.num) + " : " + str(w.place))
        # st.text(w.place)
    fp.close()


def forward(sentence, dictionary, max_len):
    """正向匹配
    :param sentence: 文本
    :param dictionary: 词典
    :param max_len: 最大词语长度
    :return: 分词结果
    """
    segments = []
    while len(sentence) > 0:
        length = max_len
        while length > 1:
            if sentence[:length] in dictionary:
                segments.append(sentence[:length])
                sentence = sentence[length:]
                break
            length = length - 1
        if length == 1:
            segments.append(sentence[:1])
            sentence = sentence[1:]
    if segments[-1] == '\n':
        del segments[-1]
    return segments


def backward(sentence, dictionary, max_len):
    """逆向匹配
    :param sentence: 文本
    :param dictionary: 词典
    :param max_len: 最大词语长度
    :return: 分词结果
    """
    segments = []
    while len(sentence) > 0:
        length = max_len
        while length > 1:
            if sentence[-length:] in dictionary:
                segments.append(sentence[-length:])
                sentence = sentence[:-length]
                break
            length = length - 1
        if length == 1:
            segments.append(sentence[-1:])
            sentence = sentence[:-1]
    if segments[0] == '\n':
        del segments[0]
    return segments


def t6_run2():
    """最大匹配法——正向/逆向"""
    cur_path = os.path.dirname(os.path.realpath(__file__))
    filename2 = "\\词典.txt"
    fp2 = open(cur_path + filename2, 'r', encoding='utf-8')
    sentence = fp2.readline()
    dictionary = fp2.readline()
    fp2.close()
    dictionary = dictionary[:len(dictionary) - 1]
    dictionary = dictionary.split(',')
    segments = forward(sentence, dictionary, 5)
    # segments = backward(sentence, dictionary, 5)
    # print(segments)
    # print('/'.join(segments))
    st.write(segments)
    st.write('/'.join(segments))


def t6_tun3():
    """对三国文本结巴分词，统计词频"""
    cur_path = os.path.dirname(os.path.realpath(__file__))
    filename3 = "\\人民日报.txt"
    fp3 = open(cur_path + filename3, 'r', encoding='utf-8')
    article3 = fp3.read()
    fp3.close()
    list3 = jieba.lcut(article3)
    set3 = set(list3)  # 集合
    words = dict()  # 字典
    for s in set3:
        words[s] = Word(s)
    for ar in list3:
        words[ar].num += 1
    newwords = []
    for w in words.values():
        newwords.append(w)
    # for w in newwords:
        # print(w.word + ":", end="")
        # print(w.num)
        # st.write(w.word + ": " + str(w.num))
    scade = pd.read_csv( cur_path+ '\\run3.CSV', encoding='gbk')
    st.dataframe(scade)

def get_diction():
    """利用结巴分词建立词典"""
    cur_path = os.path.dirname(os.path.realpath(__file__))
    filepath1 = '\\人民日报.txt'
    dict = []
    fp = open(cur_path + filepath1, 'r', encoding='utf-8')
    article3 = fp.read()
    # 创建字典
    line1 = article3.replace(' ', '')  # 去掉文本中的空格
    pattern = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 只保留中英文、数字，去掉符号
    line2 = re.sub(pattern, '', line1)  # 把文本中匹配到的字符替换成空字符
    seg = jieba.lcut(line2, cut_all=False)
    for i in range(len(seg)):
        if seg[i] not in dict:
            dict.append(seg[i])
    with open(cur_path + '\\dict人民_txt', 'w', encoding='utf-8') as fp:
        for i in dict:
            fp.write(i + ',')
    # print(dict)
    # st.write(dict)


def t6_run4():
    """最大匹配法"""
    get_diction()
    cur_path = os.path.dirname(os.path.realpath(__file__))
    filename1 = "\\人民日报.txt"
    fp1 = open(cur_path + filename1, 'r', encoding='utf-8')
    sentence = fp1.read()
    fp1.close()

    filename2 = "\\dict人民_txt"
    fp2 = open(cur_path + filename2, 'r', encoding='utf-8')
    dictionary = fp2.read()
    fp2.close()
    dictionary = dictionary.split(',')
    # segments = forward(sentence,dictionary,5)
    segments = backward(sentence, dictionary, 5)
    # print('/'.join(segments))
    set3 = set(segments)  # 集合
    words = dict()  # 字典
    for s in set3:
        words[s] = Word(s)
    for ar in segments:
        words[ar].num += 1
    newwords = []
    for w in words.values():
        newwords.append(w)
    # for w in newwords:
        # print(w.word + ":", end="")
        # print(w.num)
        # st.write(w.word + ": " + str(w.num))
    scade = pd.read_csv( cur_path+ '\\run4.CSV', encoding='gbk')
    st.dataframe(scade)


# if __name__ == "__main__":
#     for i in range(4):
#         chioce = input("1、jieba分词\n"
#                        "2、最大匹配法\n"
#                        "3、对三国进行分词\n"
#                        "4、最大匹配法分词\n")
#         if chioce == '1':
#             fun1()
#         elif chioce == '2':
#             fun2()
#         elif chioce == '3':
#             pro1()
#         else:
#             pro2()
# pro2()

# fun1()
# fun2()
# pro1()
# dict()
