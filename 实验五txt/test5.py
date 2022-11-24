# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:36:10 2020
@author: Administrator
"""
import os
from PIL import Image
from pygraph.classes.digraph import digraph
import numpy as np
import jieba
import jieba.posseg as pseg
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
from builtins import str
import streamlit as st


class PRIterator:
    __doc__ = '''计算一张图中的PR值'''

    def __init__(self, dg):
        self.damping_factor = 0.5  # 阻尼系数,即α
        self.max_iterations = 100  # 最大迭代次数
        self.min_delta = 0.00001  # 确定迭代是否结束的参数,即ϵ
        self.graph = dg

    def page_rank(self):
        #  先将图中没有出链的节点改为对所有节点都有出链
        for node in self.graph.nodes():
            if len(self.graph.neighbors(node)) == 0:
                for node2 in self.graph.nodes():
                    digraph.add_edge(self.graph, (node, node2))

        nodes = self.graph.nodes()
        graph_size = len(nodes)

        if graph_size == 0:
            return {}
        page_rank = dict.fromkeys(nodes, 1.0 / graph_size)  # 给每个节点赋予初始的PR值
        damping_value = (1.0 - self.damping_factor) / graph_size  # 公式中的(1−α)/N部分

        flag = False
        for i in range(self.max_iterations):
            change = 0
            for node in nodes:
                rank = 0
                for incident_page in self.graph.incidents(node):  # 遍历所有“入射”的页面
                    rank += self.damping_factor * (page_rank[incident_page] / len(self.graph.neighbors(incident_page)))
                rank += damping_value
                change += abs(page_rank[node] - rank)  # 绝对值
                page_rank[node] = rank

            print("第%s次迭代" % (i + 1))
            print(page_rank)

            if change < self.min_delta:
                flag = True
                break
        if flag:
            print("符合终止条件，迭代结束!")
        else:
            print("已经完成了100次迭代!")
        return page_rank


"""2、对一千个网页进行排序"""


def sort_(pr, urls):  # 排序
    for i in range(len(pr) - 1):
        for j in range(len(pr) - 1 - i):
            if pr[j] < pr[j + 1]:
                t = pr[j]
                pr[j] = pr[j + 1]
                pr[j + 1] = t
                t = urls[j]
                urls[j] = urls[j + 1]
                urls[j + 1] = t
    return pr, urls


def get_Matrix(linksavepath):
    matrix = []
    with open(linksavepath, 'r') as fp:
        i = 0
        for line in fp:
            matrix.append([])
            l = line.split(',')
            for num in l:
                num = float(num)
                matrix[i].append(num)
            i = i + 1
    return matrix


def M(m):
    num = m.sum(axis=0)  # 统计每一列的总数，也就是网页的链接数
    return m / num  # 返回建立的转移矩阵


def V(c):
    pr = np.ones((c.shape[0], 1), dtype=float) / len(c)  # 初始化PR值矩阵
    return pr


def PR(n, p, m, v):
    for i in range(n):
        v1 = p * np.dot(m, v) + (1 - p) * v
        if np.abs((v - v1).all()) < 0.001:
            v = v1
            break
        else:
            v = v1
    return v


def get_Url(URLsavepath):
    print(2)
    url = []
    with open(URLsavepath, 'r') as fp:
        for line in fp:
            url.append(line)
    return url


def isvalidurl(url1):  # 判断网页能否访问
    if (len(url1) < 2 or url1.find('.php') != -1 or url1.find('javascript') != -1
            or url1.find('#') != -1 or url1.find('.jpg') != -1 or url1.find('.mp3') != -1):
        return 0
    else:
        return 1


def refinestr(str):  # 剔除无法访问的网页及非网页
    global startpage
    if isvalidurl(str) == 0:
        print("不合法" + str)
        return '0'
    if str.find('http:') != -1 or str.find('https:') != -1:
        pass
    else:
        if (str.find(startpage) != -1):
            pass
        else:
            return startpage + str
    return str


def inlinkmap(url, myurl):  # URL是外链的URL，myurl是本页的url
    global linkmap
    global startpage
    global viewed
    # print(url)
    if isvalidurl(url) == 0:
        # print("不合法"+url)
        return 0
    else:
        try:
            myindex = viewed.index(myurl)
            index = viewed.index(url)
            linkmap[myindex, index] = 1
            # if myindex>=0 and index>=0:
            return 1
        except:
            return 0


def viewappend(stri):
    global viewed
    if isvalidurl(stri) == 0:
        print("不合法" + stri)
    else:
        viewed.append(stri)


def getalllink(url, lenth, linksavepath):  # 获取某个连接下的外链
    global linklen
    global viewed
    global linkmap
    global startpage
    url1 = refinestr(url)
    if len(url1) >= len(startpage):
        try:
            print("访问" + url1)
            htm = requests.get(url1).content
            oup = BeautifulSoup(htm, "html.parser", from_encoding="utf-8")
            linkss = oup.find_all('a', limit=500)  # 找所有外链
            # print(linkss)
            valid = 0
            for link in linkss:  # 遍历该页面外链
                if link != None:
                    if link.get('href') != None:  # 添加外链
                        if len(viewed) < linklen:
                            if viewed.count(link['href']) > 0:  # 有重复
                                # linklen-=1;
                                pass
                            else:
                                viewappend(link['href'])
                                # print(link['href'])
                        tem = inlinkmap(link['href'], url)  # 在linkmap矩阵中建立联系
                        if tem == 1:
                            valid += 1

            print("解析完成:" + url1 + "外链数：" + str(valid))
        except:  # 遇到失败的网页先保存一下现有的链接图
            print("解析失败" + url1)
            df = pd.DataFrame(linkmap)
            df.to_csv(linksavepath, index=False, header=False)


"""3、提取句子的关键字"""


class TextRank(object):

    def __init__(self, sentence, window, alpha, iternum):
        self.sentence = sentence
        self.window = window
        self.alpha = alpha
        self.edge_dict = {}  # 记录节点的边连接字典
        self.iternum = iternum  # 迭代次数

    # 对句子进行分词
    def cutSentence(self):
        cur_path = os.path.dirname(os.path.realpath(__file__))
        jieba.load_userdict(cur_path + '\\user_dict.txt')
        tag_filter = ['a', 'd', 'n', 'v']
        seg_result = pseg.cut(self.sentence)
        self.word_list = [s.word for s in seg_result if s.flag in tag_filter]
        # print(self.word_list)

    # 根据窗口，构建每个节点的相邻节点,返回边的集合
    def createNodes(self):
        tmp_list = []
        word_list_len = len(self.word_list)
        for index, word in enumerate(self.word_list):
            if word not in self.edge_dict.keys():
                tmp_list.append(word)
                tmp_set = set()
                left = index - self.window + 1  # 窗口左边界
                right = index + self.window  # 窗口右边界
                if left < 0: left = 0
                if right >= word_list_len: right = word_list_len
                for i in range(left, right):
                    if i == index:
                        continue
                    tmp_set.add(self.word_list[i])
                self.edge_dict[word] = tmp_set

    # 根据边的相连关系，构建矩阵
    def createMatrix(self):
        self.matrix = np.zeros([len(set(self.word_list)), len(set(self.word_list))])
        self.word_index = {}  # 记录词的index
        self.index_dict = {}  # 记录节点index对应的词

        for i, v in enumerate(set(self.word_list)):
            self.word_index[v] = i
            self.index_dict[i] = v
        for key in self.edge_dict.keys():
            for w in self.edge_dict[key]:
                self.matrix[self.word_index[key]][self.word_index[w]] = 1
                self.matrix[self.word_index[w]][self.word_index[key]] = 1
        # 归一化
        for j in range(self.matrix.shape[1]):
            sum = 0
            for i in range(self.matrix.shape[0]):
                sum += self.matrix[i][j]
            for i in range(self.matrix.shape[0]):
                self.matrix[i][j] /= sum

    # 根据textrank公式计算权重
    def calPR(self):
        self.PR = np.ones([len(set(self.word_list)), 1])
        for i in range(self.iternum):
            self.PR = (1 - self.alpha) + self.alpha * np.dot(self.matrix, self.PR)

    # 输出词和相应的权重
    def printResult(self):
        word_pr = {}
        for i in range(len(self.PR)):
            word_pr[self.index_dict[i]] = self.PR[i][0]
        res = sorted(word_pr.items(), key=lambda x: x[1], reverse=True)
        # print(res)
        for i in res:
            st.write(i)


"""4、网络布局分布图"""


def show_graph4(graph, layout='spring_layout'):
    # 使用 Spring Layout 布局，类似中心放射状
    if layout == 'circular_layout':
        positions = nx.circular_layout(graph)
    else:
        positions = nx.spring_layout(graph)
    # 设置网络图中的节点大小，大小与pagerank值相关，因为pagerank值很小所以需要 *20000
    nodesize = [x['pagerank'] * 20000 for v, x in graph.nodes(data=True)]
    # 设置网络图中的边长度
    # edgesize = [np.sqrt(e[2]['weight']) for e in graph.edges(data=True)]
    # 绘制节点
    nx.draw_networkx_nodes(graph, positions, node_size=nodesize, alpha=0.4)
    # 绘制边
    nx.draw_networkx_edges(graph, positions, alpha=0.2)
    # 绘制节点的 label
    nx.draw_networkx_labels(graph, positions, font_size=10)
    # 输出希拉里邮件中的所有人物关系图
    # plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(plt.show(), showPyplotGlobalUse=False)


"""5、希拉里人物关系图"""


# 针对别名进行转换
def unify_name(name):
    # 读取别名文件 生成对应字典
    cur_path = os.path.dirname(os.path.realpath(__file__))
    aliases_file = pd.read_csv(cur_path + '\\input\\Aliases.csv', encoding='utf-8')
    aliases = {}
    for index, row in aliases_file.iterrows():
        aliases[row['Alias']] = row['PersonId']
    # 读取人名文件 生成对应字典
    persons_file = pd.read_csv(cur_path + '\\input\\Persons.csv', encoding='utf-8')
    persons = {}
    for index, row in persons_file.iterrows():
        persons[row['Id']] = row['Name']

    # 姓名统一小写
    name = str(name).lower()
    # 去掉, 和 @后面的内容
    name = name.replace(",", "").split("@")[0]
    # 别名转换
    if name in aliases.keys():
        return persons[aliases[name]]
    return name


# 画网络图
def show_graph(graph, layout='spring_layout'):
    # 使用 Spring Layout 布局，类似中心放射状
    if layout == 'circular_layout':
        positions = nx.circular_layout(graph)
    else:
        positions = nx.spring_layout(graph)
    # 设置网络图中的节点大小，大小与pagerank值相关，因为pagerank值很小所以需要 *20000
    nodesize = [x['pagerank'] * 20000 for v, x in graph.nodes(data=True)]
    # 设置网络图中的边长度
    edgesize = [np.sqrt(e[2]['weight']) for e in graph.edges(data=True)]
    # 绘制节点
    nx.draw_networkx_nodes(graph, positions, node_size=nodesize, alpha=0.4)
    # 绘制边
    nx.draw_networkx_edges(graph, positions, alpha=0.2)
    # 绘制节点的 label
    nx.draw_networkx_labels(graph, positions, font_size=10)
    # 输出希拉里邮件中的所有人物关系图
    # plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(plt.show(), showPyplotGlobalUse=False)


def t5_run1():
    dg = digraph()
    dg.add_nodes(["A", "B", "C"])

    dg.add_edge(("A", "B"))
    dg.add_edge(("A", "C"))
    dg.add_edge(("B", "C"))
    dg.add_edge(("C", "A"))
    dg.add_edge(("C", "B"))
    pr = PRIterator(dg)
    page_ranks = pr.page_rank()
    st.write("最终的PR值：")
    # print("最终的PR值是:")
    for i in page_ranks:
        # print("%s:%.5f" % (i, page_ranks[i]))
        st.write(i + str(page_ranks[i]))


def t5_run2():
    # startpage = "http://www.hit.edu.cn/"  # 爬虫开始爬的页面
    # mainpage = 'http://www.hit.edu.cn/'  # 被爬取的网站域名
    # viewed = []  # 访问过的URL
    linklen = 1000  # 爬取的页面个数限制
    linkmap = np.zeros([linklen, linklen])  # 网页链接关系矩阵
    cur_path = os.path.dirname(os.path.realpath(__file__))
    linksavepath = '/app/se/实验五txt/na.txt'  # 链接图保存路径
    URLsavepath = '/app/se/实验五txt/url2.txt'  # 访问的页面的保存路径
    matrix = get_Matrix(linksavepath)
    urls = get_Url(URLsavepath)
    m = np.array(matrix, dtype=float)
    m = M(m)
    pr = V(m)
    a = 0.85
    pr = PR(18, a, m, pr)
    pr, urls = sort_(pr, urls)
    st.success("最终网页排名：")
    for url in urls:
        st.write(url)


def t5_run3():
    """提取关键字"""
    s = '程序员(英文Programmer)是从事程序开发、维护的专业人员。一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。'
    tr = TextRank(s, 3, 0.85, 700)
    tr.cutSentence()
    tr.createNodes()
    tr.createMatrix()
    tr.calPR()
    tr.printResult()


def t5_run4():
    G = nx.DiGraph()
    # 有向图之间边的关系
    edges = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "A"), ("B", "D"), ("C", "A"), ("D", "B"), ("D", "C")]
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    pagerank_list = nx.pagerank(G, alpha=1)  # alpha为阻尼因子，alpha=0.85表示跳转率为15%
    # print("pagerank 值是：", pagerank_list)
    nx.set_node_attributes(G, values=pagerank_list, name='pagerank')

    edges_weights_temp = defaultdict(list)
    # 绘制圆环图像
    positions = nx.circular_layout(G)
    # 绘制反射图像
    # positions=nx.spring_layout(G)
    # 绘制节点
    nx.draw_networkx_nodes(G, positions, alpha=0.4)
    # 绘制边
    nx.draw_networkx_edges(G, positions, alpha=0.2)
    # 绘制节点的 label
    nx.draw_networkx_labels(G, positions, font_size=10)
    pagerank_threshold = 0.005
    # 复制一份计算好的网络图
    small_graph = G.copy()
    # 剪掉 PR 值小于 pagerank_threshold 的节点
    for n, p_rank in G.nodes(data=True):
        if p_rank['pagerank'] < pagerank_threshold:
            small_graph.remove_node(n)
    show_graph4(G, 'circular_layout')


def t5_run5():
    cur_path = os.path.dirname(os.path.realpath(__file__))
    img = Image.open(cur_path + "\\Figure_1.png")
    # st.image(img)
    st.image(img, caption="希拉里文物关系图 Image")
    img = Image.open(cur_path + "\\Figure_2.png")
    # st.image(img)
    st.image(img, caption="希拉里文物剪枝关系图 Image")

# if st.button("get"):
#     t5_run1()
# if st.button("get2"):
#     t5_run2()
# if st.button("get"):
#     t5_run5()
# if __name__ == '__main__':
#     while True:
#         choice = input("1、给定网页关系的PR值\n"
#                        "2、对1000个网页进行排序\n"
#                        "3、提取给定句子中的关键字\n"
#                        "4、网络分布图\n"
#                        "5、希拉里人物关系\n"
#                        "请选择：")
#
#         if choice == '1':
#             dg = digraph()
#
#             dg.add_nodes(["A", "B", "C"])
#
#             dg.add_edge(("A", "B"))
#             dg.add_edge(("A", "C"))
#             dg.add_edge(("B", "C"))
#             dg.add_edge(("C", "A"))
#             dg.add_edge(("C", "B"))
#
#             pr = PRIterator(dg)
#             page_ranks = pr.page_rank()
#
#             print("最终的PR值是:")
#             for i in page_ranks:
#                 print("%s:%.5f" % (i, page_ranks[i]))
#
#         elif choice == '2':
#             # startpage = "http://www.hit.edu.cn/"  # 爬虫开始爬的页面
#             # mainpage = 'http://www.hit.edu.cn/'  # 被爬取的网站域名
#             # viewed = []  # 访问过的URL
#             linklen = 1000  # 爬取的页面个数限制
#             linkmap = np.zeros([linklen, linklen])  # 网页链接关系矩阵
#             linksavepath = 'D:\\桌面\\python基础知识\\网络安全前沿技术\\实验4\\na.txt'  # 链接图保存路径
#             URLsavepath = 'D:\\桌面\\python基础知识\\网络安全前沿技术\\实验4\\url2.txt'  # 访问的页面的保存路径
#             matrix = get_Matrix()
#             urls = get_Url()
#             m = np.array(matrix, dtype=float)
#             m = M(m)
#             pr = V(m)
#             a = 0.85
#             pr = PR(18, a, m, pr)
#             pr, urls = sort_(pr, urls)
#             print("最终网页排名为：")
#             for url in urls:
#                 print(url)
#
#         elif choice == '3':
#             """提取关键字"""
#             s = '程序员(英文Programmer)是从事程序开发、维护的专业人员。一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。'
#             tr = TextRank(s, 3, 0.85, 700)
#             tr.cutSentence()
#             tr.createNodes()
#             tr.createMatrix()
#             tr.calPR()
#             tr.printResult()
#
#         elif choice == '4':
#             G = nx.DiGraph()
#             # 有向图之间边的关系
#             edges = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "A"), ("B", "D"), ("C", "A"), ("D", "B"), ("D", "C")]
#             for edge in edges:
#                 G.add_edge(edge[0], edge[1])
#             pagerank_list = nx.pagerank(G, alpha=1)  # alpha为阻尼因子，alpha=0.85表示跳转率为15%
#             print("pagerank 值是：", pagerank_list)
#             nx.set_node_attributes(G, values=pagerank_list, name='pagerank')
#             edges_weights_temp = defaultdict(list)
#
#             # 绘制圆环图像
#             positions = nx.circular_layout(G)
#             # 绘制反射图像
#             # positions=nx.spring_layout(G)
#             # 绘制节点
#             nx.draw_networkx_nodes(G, positions, alpha=0.4)
#             # 绘制边
#             nx.draw_networkx_edges(G, positions, alpha=0.2)
#             # 绘制节点的 label
#             nx.draw_networkx_labels(G, positions, font_size=10)
#             pagerank_threshold = 0.005
#             # 复制一份计算好的网络图
#             small_graph = G.copy()
#             # 剪掉 PR 值小于 pagerank_threshold 的节点
#             for n, p_rank in G.nodes(data=True):
#                 if p_rank['pagerank'] < pagerank_threshold:
#                     small_graph.remove_node(n)
#             show_graph4(G, 'circular_layout')
#
#         elif choice == '5':
#             # 数据加载
#             # 加载邮件数据文件
#             emails = pd.read_csv('./input/Emails.csv', encoding='utf-8')
#             # print(emails.head(5))
#             # print(emails.info())
#             # 删除'MetadataTo'或者 'MetadataFrom'为空的数据
#             emails = emails.dropna(subset=['MetadataTo', 'MetadataFrom'], how='any')
#             # print(emails.info())
#
#             # 读取别名文件 生成对应字典
#             aliases_file = pd.read_csv('./input/Aliases.csv', encoding='utf-8')
#             aliases = {}
#             for index, row in aliases_file.iterrows():
#                 aliases[row['Alias']] = row['PersonId']
#             # 读取人名文件 生成对应字典
#             persons_file = pd.read_csv('./input/Persons.csv', encoding='utf-8')
#             persons = {}
#             for index, row in persons_file.iterrows():
#                 persons[row['Id']] = row['Name']
#
#             # 将寄件人和收件人的姓名进行规范化
#             emails.MetadataFrom = emails.MetadataFrom.apply(unify_name)
#             # -*- coding: utf-8 -*-
#             emails.MetadataTo = emails.MetadataTo.apply(unify_name)
#             # 设置遍的权重等于发邮件的次数
#             edges_weights_temp = defaultdict(list)
#             for row in zip(emails.MetadataFrom, emails.MetadataTo, emails.RawText):
#                 temp = (row[0], row[1])
#                 if temp not in edges_weights_temp:
#                     edges_weights_temp[temp] = 1
#                 else:
#                     edges_weights_temp[temp] = edges_weights_temp[temp] + 1
#             # 转化格式 (from, to), weight => from, to, weight
#             edges_weights = [(key[0], key[1], val) for key, val in edges_weights_temp.items()]
#             # 创建一个有向图
#             graph = nx.DiGraph()
#             # 设置有向图中的路径及权重 (from, to, weight)
#             graph.add_weighted_edges_from(edges_weights)
#             # 计算每个节点（人）的 PR 值，并作为节点的 pagerank 属性
#             pagerank = nx.pagerank(graph)
#             # 将 pagerank 数值作为节点的属性
#             nx.set_node_attributes(graph, name='pagerank', values=pagerank)
#             # 画网络图
#             show_graph(graph)
#             # 将完整的图谱进行精简
#             # 设置 PR 值的阈值，筛选大于阈值的重要核心节点
#             pagerank_threshold = 0.005
#             # 复制一份计算好的网络图
#             small_graph = graph.copy()
#             # 剪掉 PR 值小于 pagerank_threshold 的节点
#             for n, p_rank in graph.nodes(data=True):
#                 if p_rank['pagerank'] < pagerank_threshold:
#                     small_graph.remove_node(n)
#             # 画网络图, 采用 circular_layout 布局让筛选出来的点组成一个圆
#             show_graph(small_graph, 'circular_layout')
#
#         else:
#             print("结束")
#             break
