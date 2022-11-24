# -*- coding:utf-8 -*-
import urllib.request
import urllib
import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin
import streamlit as st


class text3:
    @st.cache
    def crawl_content(self, url, i):
        """将指定URL的HTML网页文本内容下载保存到本地"""
        # 1、指定URL
        # url = 'http://tieba.baidu.com/p/2460150866'
        # url = "https://tieba.baidu.com/p/6612379644"
        # url = "https://www.hippopx.com/"
        # 2、发送请求
        # get（）方法会返回一个响应对象

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50"}
        response = requests.get(url=url, headers=headers)

        # 3、获取去响应数据，在响应对象中获取
        # .text返回的是字符串形式的响应数据
        response.encoding = 'utf-8'
        tieba_text = response.text

        # 4、将获取的数据写入本地文件中
        cur_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(os.path.dirname(cur_path), '实验三txt\\Ifo\\')
        str = file_path + i
        if not os.path.exists(str):
            os.mkdir(file_path + i)

        f = open(str + "\\HTML" + ".txt", 'w', encoding='utf-8')
        f.write(tieba_text)
        f.close()

        print("盘完了")
        return tieba_text
    @st.cache
    def extract_title(self, content, i):
        """提取网页标题"""
        # 1、创建BeautifulSoup对象，html.parser对页面进行解析
        soup = BeautifulSoup(content, "html.parser")

        # 2、提取标题
        title = soup.find('title').text

        # 3、将标题写入本地文件
        cur_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(os.path.dirname(cur_path), '实验三txt\\Ifo\\')
        str = file_path + i
        if not os.path.exists(str):
            os.mkdir(file_path + i)

        f = open(str + "\\title" + ".txt", 'w', encoding='utf-8')
        f.write(title)
        f.close()

        print("标题写完了")

    # _____________________________________________________________

    def remove_empty_line(self, content):
        """获取正文"""
        # 匹配全是字符的行
        r = re.compile(r'''^\s+$''', re.M | re.S)  # re.M(多行模式)||re.S(匹配所有字符)
        s = r.sub('', content)
        # 匹配一个空行
        r = re.compile(r'''\n+''', re.M | re.S)
        s = r.sub('\n', s)
        return s

    def remove_js_css(self, content):
        """移除script/style/meta/注释等脚本"""
        r = re.compile(r'''<script.*?</script>''', re.I | re.M | re.S)
        s = r.sub('', content)
        r = re.compile(r'''<style.*?</style>''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<!--.*?-->''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<meta.*?>''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<ins.*?</ins>''', re.I | re.M | re.S)
        s = r.sub('', s)
        return s

    def remove_any_tag(self, s):
        """移除js/css等脚本"""
        s = re.sub(r'''<[^>]+>''', '', s)
        return s.strip()

    def extract_text(self,content, i):
        s = self.remove_empty_line(self.remove_js_css(content))
        s = self.remove_any_tag(s)
        s = self.remove_empty_line(s)
        cur_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(os.path.dirname(cur_path), '实验三txt\\Ifo\\')
        str = file_path + i
        if not os.path.exists(str):
            os.mkdir(file_path + i)

        f = open(str + "\\正文" + ".txt", 'w', encoding='utf-8')
        f.write(s)
        f.close()

        print("正文写完了")

    # ————————————————————————————————————————————————————————

    def extract_a_label(self, content, i):
        """爬取子链接"""
        soup = BeautifulSoup(content, "html.parser")
        alink = soup.find_all('a')
        cur_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(os.path.dirname(cur_path), '实验三txt\\Ifo\\')
        str = file_path + i
        if not os.path.exists(str):
            os.mkdir(file_path + i)

        fp = open(str + "\\子链接" + ".txt", 'w', encoding='utf-8')
        for link in alink:
            a = link.get('href')
            key = link.string
            if key is not None and a is not None:
                fp.write(key)
                fp.write(a)
                fp.write('\n')
        fp.close()

        print("子链接写完了")
        return alink

    # ——————————————————————————————————————————————————————————————————

    def getImg(self, content, i):
        reg = r'src="(.+?\.jpg)" pic_ext'
        imgre = re.compile(reg)
        imglist = imgre.findall(content)
        x = 0
        # path = "D:\\桌面\\python基础知识\\搜索引擎\\实验三爬虫\\img"
        cur_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(os.path.dirname(cur_path), '实验三txt\\Ifo\\')
        path = file_path + i
        if not os.path.exists(path):
            os.mkdir(file_path + i)

        paths = path + '\\'
        for imgurl in imglist:
            urllib.request.urlretrieve(imgurl, '{}{}.jpg'.format(paths, x))
            x = x + 1
        print(imglist)
        return imglist

    def test1(self, url, i):
        """获取指定网页内容"""
        content = self.crawl_content(url, i)  # 获取HTML文件内容
        self.extract_title(content, i)  # 获取标题
        self.extract_text(content, i)  # 获取正文
        alink = self.extract_a_label(content, i)  # 获取子链接
        self.getImg(content.encode('utf-8').decode('utf-8'), i)  # 获取图片
        return alink

    def test2(self, url):
        """广度优先遍历"""
        n = 1  # 文件记录
        N = 10  # 爬取网页的个数
        unvisited = [url, ]
        visited = []
        while True:
            if len(unvisited) == 0 or len(visited) == N:
                break
            num = str(n)
            alink = self.test1(unvisited[0], num)
            visited.append(unvisited[0])
            del unvisited[0]
            for link in alink:
                a = link.get('href')
                key = link.string
                if key is not None and a is not None:
                    if str(a) in visited or str(a) in unvisited:
                        continue
                    if re.match(r'^https?:/{2}\w.+$', str(a)):
                        unvisited.append(str(a))
            n += 1

    def test3(self, url):
        """深度优先遍历"""
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50"}
        resp_shou = requests.get(url=url, headers=headers)
        if resp_shou:
            print(resp_shou.url)
            next_page = re.findall(r"<a href='(.+)'>ÏÂÒ»Ò³", str(resp_shou.text))
            if next_page:
                # 为了不把一个深度全部爬取完，所以只爬取前5页
                if re.findall(r'.+_(\d+)\.html', str(next_page))[0] == '6':
                    return
                next_page_url = urljoin(resp_shou.url, next_page[0])
                return self.test3(next_page_url)


t3 = text3()
# t3.test2("https://www.csdn.net/")
# cur_path = os.path.dirname(os.path.realpath(__file__))
# file_path = os.path.join(os.path.dirname(cur_path), '实验三txt\\Ifo\\')
# for i in range(1, 11):
#     s = file_path + str(i)
#     folder = os.walk(s)
#     files = list(folder)[0]
#     print(files[2])


# print(t3.test1("http://tieba.baidu.com/p/2460150866", "0"))

# def run1(gl_url):
#     t3 = text3()
#     t3.test2(gl_url)
#     print("爬取成果")

# run1('http://tieba.baidu.com/p/2460150866')
# cur_path = os.path.dirname(os.path.realpath(__file__))
# file_path = os.path.join(os.path.dirname(cur_path), '实验三txt\\Ifo\\')
# print(file_path)
# f = open(file_path + '1\\正文.txt', 'r', encoding='utf-8')

# if __name__ == '__main__':
    # gl_url = 'http://tieba.baidu.com/p/2460150866'
    # gl_url = "https://www.csdn.net/"


"""获取网页的编码格式"""
# from urllib import request
# import chardet


# if __name__ == "__main__":
#     response = request.urlopen("https://tieba.baidu.com/p/6612379644")
#     html = response.read()
#     charset = chardet.detect(html)#对该html进行编码的获取
#     print(charset) #打印编码格式
