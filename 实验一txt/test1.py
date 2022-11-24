# -*- coding:utf-8 -*-
import time
import streamlit as st
import jieba


class text1:
    def __init__(self, text):
        self.text = text

    # ————————————————————————————————————————————————————————————————————————
    def BF(self, s_str, p_str):
        """
        BM算法进行匹配
        :param s_str: 主串
        :param p_str: 模式串
        :return: 返回主串中出现的模式串的首元位置
        """
        i = 0
        j = 0
        while i < len(s_str) and j < len(p_str):
            if s_str[i] == p_str[j]:
                i += 1
                j += 1
            else:
                i = i - j + 1  # 主串返回到模式串的移动一位后的首位置
                j = 0
            if j == len(p_str):
                return i - j
        return -1

    def kmp(self, m_str, s_str):
        # m_str表示主串，s_str表示模式串

        # 求next数组
        next_ls = [-1] * len(s_str)
        m = 1  # 从1开始匹配
        s = 0
        next_ls[1] = 0
        while m < len(s_str) - 1:
            if s_str[m] == s_str[s] or s == -1:
                m += 1
                s += 1
                next_ls[m] = s
            else:
                s = next_ls[s]
        #  print(next_ls)  检查next数组
        # KMP
        i = j = 0  # i,j位置指针初始值为0
        while i < len(m_str) and j < len(s_str):
            # 模式串遍历结束匹配成功，主串遍历结束匹配失败
            # 匹配成功或失败后退出
            if m_str[i] == s_str[j] or j == -1:
                # 把j==-1时纳入到条件判断中，实现i+1，j归零
                i += 1
                j += 1
            else:
                j = next_ls[j]

        if j == len(s_str):
            return i - j  # 匹配成功
        return -1  # 匹配失败

    # 测试
    # dex = BF()
    # print(S[dex:len(P)+dex])
    # 对“sanguo.txt”文本进行查找
    def search_bf(self, mode_str):
        self.text = " "
        with open('sanguo.txt', 'r+', encoding='utf-8') as f:
            for line in f:
                length = len(line)  # 模式串的长度
                dex = 0  # 记录主串下标
                while dex <= length:
                    """BM算法进行查找
                    ——如果找到，就返回模式串对应的主串的首元位置，对行进行切片，截取该行剩余的内容，下标变换
                    ——如果没有找到就读取下一行"""
                    result = self.BF(line, mode_str)
                    if not result == -1:
                        dex = result
                        # print(line[:dex - 1], end="")
                        self.text += line[:dex - 1]
                        # 将文本中的内容加入到界面文本框中
                        # self.text.insert('insert', line[:dex - 1] + "")
                        """两种高亮的方式
                        前者使用于运行框输出
                        后者适用于文本中"""
                        # print("\033[1;30;43m" + line[dex:len(mode_str) + dex] + "\033[0m", end="")
                        # \colorbox{yellow}{hello}
                        # self.text.insert('end', line[dex:len(mode_str) + dex] + "", "tag_1")
                        # self.text += ":+1:" + line[dex:len(mode_str) + dex] + ":+1:"
                        self.text += '''<font color=red>''' + line[dex:len(mode_str) + dex] + '''</font>'''
                        line = line[dex + len(mode_str):]
                        dex = dex + len(mode_str)
                    else:
                        # print(line)
                        # self.text.insert('insert', line)
                        self.text += line
                        break

    def search_kmp(self, mode_str):
        self.text = " "
        with open('sanguo.txt', 'r+', encoding='utf-8') as f:
            for line in f:
                length = len(line)  # 模式串的长度
                dex = 0  # 记录主串下标
                # stat_time = time.perf_counter()
                while dex <= length:
                    """BM算法进行查找
                    ——如果找到，就返回模式串对应的主串的首元位置，对行进行切片，截取该行剩余的内容，下标变换
                    ——如果没有找到就读取下一行"""

                    result = self.kmp(line, mode_str)
                    if not result == -1:
                        dex = result
                        # print(line[:dex - 1], end="")
                        self.text += line[:dex - 1]
                        # 将文本中的内容加入到界面文本框中
                        # self.text.insert('insert', line[:dex - 1] + "")
                        """两种高亮的方式
                        前者使用于运行框输出
                        后者适用于文本中"""
                        # print("\033[1;30;43m" + line[dex:len(mode_str) + dex] + "\033[0m", end="")
                        self.text += '''<font color=red>''' + line[dex:len(mode_str) + dex] + '''</font>'''
                        # self.text.insert('end', line[dex:len(mode_str) + dex] + "", "tag_1")
                        line = line[dex + len(mode_str):]
                        dex = dex + len(mode_str)
                    else:
                        # print(line)
                        # self.text.insert('insert', line)
                        self.text += line
                        break

    # —————————————————————————————————————————————————————————————————————————#
    # ***********1、书目查找*********
    # ———————————————————————————#

    def split_words(self, article):
        """
        将字典的值进行分割放入列表中
        :param article:数目字典
        :return:书名列表
        """
        words = []
        for i in article.values():
            cut = i.split()
            words.extend(cut)

        # 去掉开头字母示是小写的值
        for num in words:
            if num[0].islower():
                words.remove(num)
        # 去掉重复的值
        set_words = set(words)
        return set_words

    def insert_index(self, article, set_all_word):
        """
        建立索引
        :param article: 数目
        :param set_all_word: 去重的set
        """
        invert_index = {}  # 索引字典
        for b in set_all_word:  # 循环书名的单词
            temp = []
            for j in article.keys():  # 循环书号
                filed = article[j]  # 获得书名
                split_filed = filed.split()

                if b in split_filed:
                    temp.append(j)
            invert_index[b] = temp

        return invert_index

    # ————————————————————————————————————————————————————————
    # *******2、单词索引查找***********
    # ————————————————
    @st.cache
    def read_file(self, file_name):
        """
        将英文文本的单词放到列表中存储
        :param file_name: 文件名
        :return: 返回单词列表
        """
        words = []
        with open(file_name, 'r', encoding='utf-8') as fp:

            for line in fp:
                word = ''
                line = line.strip()
                word.strip()
                for char in line:
                    if char.isalpha():
                        word += char
                    else:
                        word.strip()
                        words.append(word)
                        word = ''
        # 删除多余的空字符
        for i in words:
            if i == '':
                words.remove(i)
        return words

    def index_table(self, words):
        """
        建立做索引表
        :param words: 单词列表
        :return: 索引表
        """
        # 将单词放入字典中{单词：位置}
        article = {}
        dex = 0
        """注意字典中的键不能有重复的元素"""
        set_words = set(words)
        for i in set_words:
            article[i] = dex
            dex += 1
        # print(article)
        # 建立索引表
        table = {}  # 索引表
        for i in article.keys():
            temp = []
            for j in range(len(words)):
                if i == words[j]:
                    temp.append(j)
            table[i] = temp
        return table

    def write_file(self, file_name, table):
        """
        将索引表写进文件中
        :rtype: object
        """
        with open(file_name, 'w+', encoding='utf-8') as fp:
            for i in table:
                fp.write("%-15s" % i)
                for j in table[i]:
                    fp.write("%-5s" % j)
                fp.write("\n")

    # ——————————————————————————————————————————————————————————————————————
    # ***********3、三国人物查找
    # ——————————————————————————
    def read_sanguo(self, file_name):
        """
        从文件中读取文章进行分词
        :param file_name: 文件名称
        :return: 返回所有词语组成的列表
        """
        f = open(file_name, 'r', encoding='utf-8')
        sanguo = f.read()
        words = jieba.lcut(sanguo)  # 精准模式语法，切分后词语总词数与文章总词数相同
        f.close()
        return words

    def sanguo_table(self, words, find_words):
        """
        建立三国文章的索引表
        :param words: 所有词语列表
        :param find_words: 待查找的词语
        :return: 返回索引表
        """
        table = {}
        # 暂时定对为曹操和刘备建立索引表
        for word in find_words:
            dex = 0  # 循环词语下标
            temp = []  # 存放查找词语的下标
            for k in words:
                if word == k:
                    temp.append(dex)
                dex += 1
            table[word] = temp
        return table

    # ————————————————————————————————————————————————————————————————————————————————————————————#
    # ************运行函数****************
    # ——————————————————————————————————————————————————————————

    # BF算法查找三国
    def show1(self, find_what):
        start_time = time.perf_counter()
        self.search_bf(find_what)
        end_time = time.perf_counter()
        sum_time = end_time - start_time
        # print("BF：%f" % sum_time)

    # KMP算法查找三国
    def show2(self, find_what):
        start_time = time.perf_counter()
        self.search_kmp(find_what)
        end_time = time.perf_counter()
        sum_time = end_time - start_time
        # print("KMP：%f" % sum_time)

    # 书目查找
    def fun1(self):
        self.text = " "
        gl_article = {}
        # 将文件中的内容读取到字典中
        with open("实验2.1 建立词汇索引表_用例.txt", 'r', encoding='utf-8') as fp:
            for line in fp:
                line = line.replace("\n", "")
                gl_article[line[0:3]] = line[3:]

        # 进行拆分去重
        all_words = self.split_words(gl_article)
        # 建立索引
        invert = self.insert_index(gl_article, all_words)

        with open("书目索引表", 'w+', encoding='utf-8') as fp:
            for i in invert:
                fp.write("%-12s" % i)
                for j in invert[i]:
                    fp.write("%-5s" % j)
                fp.write("\n")

        with open("书目索引表", 'r', encoding='utf-8') as fp:
            for line in fp:
                self.text += line

    # 单词索引查找
    def fun2(self):
        self.text = " "
        file_name = "实验2.2_单文档查找用例.txt"
        gl_words = self.read_file(file_name)
        table = self.index_table(gl_words)
        show_filename = "单词索引表"
        self.write_file(show_filename, table)
        with open("单词索引表", 'r', encoding='utf-8') as fp:
            for line in fp:
                self.text += line

    # 三国人物查找
    @st.cache
    def fun3(self, mode_str):
        self.text = " "
        file = "sanguo.txt"
        article = self.read_sanguo(file)  # 返回的是一个列表
        find_what = ['曹操', '诸葛亮', '刘备']
        gl_table = self.sanguo_table(article, find_what)
        dex = -1  # 搜索哪一个单词
        for i in range(len(find_what)):
            if find_what[i] == mode_str:
                dex = i
                break

        index = gl_table[find_what[dex]]  # 获得所有需要高亮的词的下标

        # print("索引查找时间：%f" % sum_time)
        for i in range(len(article)):
            if i in index:
                self.text += '''<font color=red>''' + article[i] + '''</font>'''
            else:
                self.text += article[i]

        # 测试
        # for k in gl_table:
        #     print("%s:%s\n" % (k, gl_table[k]))

    def fun3_show(self, find_what):
        self.fun3(find_what)

    def run1(self, find_what):
        """
        BF算法
        :param find_what: 用户想要搜索的内容
        :return: 返回搜索结果
        """
        self.show1(find_what)
        st.markdown(self.text, unsafe_allow_html=True)

    def run2(self, find_what):
        """kmp算法"""
        self.show2(find_what)
        st.markdown(self.text, unsafe_allow_html=True)

    def run3(self):
        self.fun1()
        st.write(self.text)
        # print(self.text)

    def run4(self):
        self.fun2()
        # print(self.text)
        st.write(self.text)

    def run5(self, find_what):
        self.fun3_show(find_what)
        st.markdown(self.text, unsafe_allow_html=True)
        print(self.text)

    #     # 设置按钮的名称，宽度，事件，行，列，方位（NSWE），坐标
    #     Button(self.root, text="BF算法", width=10, command=self.show1).grid(row=3, column=0, sticky=W)
    #     Button(self.root, text="KMP算法", width=10, command=self.show2).grid(row=3, column=0)
    #     Button(self.root, text="退出", width=10, command=quit).grid(row=3, column=0, sticky=E)
    #     Button(self.root, text="书目查找", width=10, command=self.fun1).grid(row=4, column=0, sticky=W)
    #     Button(self.root, text="单词查找", width=10, command=self.fun2).grid(row=4, column=0)
    #     Button(self.root, text="三国人物查找", width=10, command=self.fun3_show).grid(row=4, column=0, sticky=E)
    #     self.root.mainloop()


t1 = text1(" ")
# t1.run5("曹操")
