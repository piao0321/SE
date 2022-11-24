# -*- coding: utf-8 -*-
"""
@Time :2022/11/20 0:28
@Author :Lai Xiangyuan
@Email :2936885192@qq.com
@File :try.py
@ID :12003990122
"""

import streamlit as st
from 实验一txt.test1 import *
from 实验三txt.test3 import *
from 实验四txt.test4 import *
from 实验五txt.test5 import *
from 实验六txt.test6 import *
from 实验七txt.test7 import *
from 实验八txt.test8 import *


def main():
    st.image("封面.png")
    # app = MultiPage()
    st.sidebar.warning("请在边栏进行选择")
    activities = ["实验一二", "实验三", "实验四", "实验五",
                  "实验六", "实验七", "实验八"]

    choice = st.sidebar.selectbox("Select task", activities)
    st.success("当前选择：" + choice)

    if choice == "实验一二":
        st.info("1、BF算法进行查找\n")
        st.info("2、KMP算法进行查找\n")
        st.info("3、数目查找\n")
        st.info("4、单词查找\n")
        st.info("5、三国人物查找\n")
        find_what = st.text_area('Enter you message', '如曹操')
        which = st.sidebar.selectbox("请选择你要测试第几题：", ["exe1", "exe2", "exe3", "exe4", "exe5"])
        st.success(which)
        if st.button("submit"):
            if which == "exe1":
                t1.run1(find_what)
            elif which == "exe2":
                t1.run2(find_what)
            elif which == "exe3":
                t1.run3()
            elif which == "exe4":
                t1.run4()
            elif which == "exe5":
                t1.run5(find_what)
            st.balloons()

    elif choice == "实验三":
        st.info("1、爬取指定URL的内容")
        st.info("2、广度优先遍历爬取若干网页（正则表达式获取内容）")
        st.info("3、深度优先遍历")
        find_what = st.text_area('输入你想要爬取的网页', '如https://www.csdn.net/')
        which = st.sidebar.selectbox("请选择你要测试第几题：", ["exe1", "exe2", "exe3"])
        st.success("当前测试：" + which)
        # st.file_uploader("文件上传")
        # st.download_button('Download some text', data='application/octet-stream', file_name=' ', mime='application/octet-stream')
        if st.button("submit"):
            if which == "exe1":
                t3.test1(find_what, "0")
            elif which == "exe2":
                t3.test2(find_what)
            elif which == "exe3":
                t3.test3(find_what)

            # 对实验结果进行显示
        file_num = st.text_input("选择第几个文件夹(1~10)", 'type here..')
        files_name = ['HTML.txt', 'title.txt', '子链接.txt', '正文.txt']
        which_file = st.selectbox("请选择你想要显示的文件", files_name)
        cur_path = os.path.dirname(os.path.realpath(__file__))
        if st.button("display"):
            fp = open(cur_path + "\\实验三txt\\Ifo\\" + str(file_num) + "\\" + which_file, 'r', encoding='utf-8')
            content = fp.read()
            fp.close()
            st.write(content)

    elif choice == "实验四":
        st.info("1、计算两个文本串的k-shingle集合")
        st.info("2、计算两个文本的相似度")
        st.info("3、计算一个文本和和某路径下所有文档的相似度")
        st.info("4、simhash计算两个文本哈希值相似度")
        which = st.sidebar.selectbox("请选择你要测试第几题：", ["exe1", "exe2", "exe3", "exe4"])
        if st.button("display"):
            if which == "exe1":
                t4_run1()
            elif which == 'exe2':
                t4_run2()
            elif which == 'exe3':
                t4_run3()
            elif which == "exe4":
                cur_path = os.path.dirname(os.path.realpath(__file__))
                com_file_data_sim(cur_path + '\\实验四txt\\sanguo.txt').com_data_sim()

    elif choice == "实验五":
        st.info("1、给定网页关系的PR值")
        st.info("2、对1000个网页进行排序")
        st.info("3、提取给定句子中的关键字")
        st.info("4、网络分布图")
        st.info("5、希拉里人物关系")
        which = st.sidebar.selectbox("请选择你要测试第几题：", ["exe1", "exe2", "exe3", "exe4", "exe5"])
        if which == "exe1":
            t5_run1()
        elif which == "exe2":
            t5_run2()
        elif which == "exe3":
            t5_run3()
        elif which == "exe4":
            t5_run4()
        elif which == "exe5":
            t5_run5()

    elif choice == "实验六":
        st.info("1、jieba分词")
        st.info("2、最大匹配法")
        st.info("3、对三国进行分词")
        st.info("4、最大匹配法分词")
        which = st.sidebar.selectbox("请选择你要测试第几题：", ["exe1", "exe2", "exe3", "exe4"])
        if which == "exe1":
            t6_run1()
        elif which == "exe2":
            t6_run2()
        elif which == "exe3":
            t6_tun3()
        elif which == "exe4":
            t6_run4()

    elif choice == "实验七":
        st.info("1、计算TF-IDF")
        st.info("2、scikit-learn库来计算TFIDF")
        st.info("3、余弦相似度计算文本相似度")
        st.info("4、simhash算法")
        which = st.sidebar.selectbox("请选择你要测试第几题：", ["exe1", "exe2", "exe3", "exe4"])
        if which == "exe1":
            t7_run1()
        elif which == "exe2":
            t7_run2()
        elif which == "exe3":
            t7_run3()
        elif which == "exe4":
            t7_run4()

    elif choice == "实验八":
        st.info("1、“滑动窗口的方法”抽取文档摘要")
        st.info("2、选取几篇相关文档抽取其中摘要信息")
        st.info("3、使用TextRank提取给定段落中的中心句")
        which = st.sidebar.selectbox("请选择你要测试第几题：", ["exe1", "exe2", "exe3"])
        if which == "exe1":
            t8_run1()
        elif which == "exe2":
            t8_run2()
        elif which == "exe3":
            t8_run3()


main()
