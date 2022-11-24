# -*- coding: utf-8 -*-
"""
@Time :2022/11/19 22:35
@Author :Lai Xiangyuan
@Email :2936885192@qq.com
@File :sreamlit学习.py
@ID :12003990122
"""

import streamlit as st

#### 使用 `<font>` 的标签的修改文字前景色

# <font color="red">红色</font>
# <font color="green">绿色</font>
# <font color="blue">蓝色</font>
#
# <font color="rgb(200, 100, 100)">使用 rgb 颜色值</font>
#
# <font color="#FF00BB">使用十六进制颜色值</font>
st.markdown('''helll<font color=red>''' + '''hongse</font>''', unsafe_allow_html=True)
# st.title("hello world")
#
# st.header("This is a header")
#
# st.subheader('This is a subheader')
#
# st.text("hello streamlit")
#
# st.markdown("### this is a markdown")
#
# st.error("successful")
#
# st.info("information")
#
# st.warning("warning")
#
# st.error("error")
#
# st.exception("NameERROR('name three not define')")
#
# # get help info about python
# st.help(range)
#
# # writing text
# st.write("text write")
# st.write(range(10))
#
# # Image
# from PIL import Image
#
# img = Image.open("39822464_2.jpg")
# # st.image(img)
# st.image(img, width=300, caption="Simple Image")
#
# # videos
# # vib_file = open("0 互联网时代第1集：时代.mp4", "rb")
# # vib_bytes = vib_file.read()
# # st.video(vib_bytes)
#
# # vib_file = open("0 互联网时代第1集：时代.mp4", "rb").read()
# # st.video(vib_file)
#
# # Audio
# # audio_file = open("file_name", "rb").read()
# # st.radio(audio_file, format_func='audio/mp3')
#
# # Widget
# # Checkbox  勾选
# if st.checkbox("show/hide"):
#     st.text("showing or hiding widget")
#
# # radio Buttons 多选一
# status = st.radio("what is your status", ("Active", "Inactive"))
#
# # SelectBox
# occupation = st.selectbox("your occupation", ["doctor", "businessman"])
# st.write("you select this options", occupation)
#
# # MultiSelect
# location = st.multiselect("where are you from?", ("China", "Japan", "London"))
# st.write("you select", len(location), "locations")
#
# # Slider
# level = st.slider("what is you level", 1, 10)
#
# # Button
# if st.button("simple Button"):
#     st.text("Streamlit is cool")
#
# # text input
# first_name = st.text_input("Enter you firstname", "type here..")
#
# if st.button("submit"):
#     result = first_name.title()
#     st.success(result)
#
# # text area
# message = st.text_area("Enter you message", "type here..")
#
# if st.button("submit1"):
#     result = message.title()
#     st.success(result)
#
# # date input
# # import datetime
# #
# # today = st.date_input("today is", datetime.datetime.now())
# #
# # # Time
# # the_Time = st.time_input("this time is ", datetime.time())
#
# # display json
# st.text("display json")
# st.json({'name': "jesse", "gender": "male"})
#
# # display raw code 显示代码
# st.text("display row code")
# st.code("import numpy as np")
# with st.echo():
#     import pandas as pd
#
#     df = pd.DataFrame()
#
# # progress bar
# import time
#
# my_bar = st.progress(0)
# for p in range(10):
#     my_bar.progress(p * 1)
#
# # Spinner  等待转圈
# # with st.spinner("waiting.."):
# #     time.sleep(5)
#
# # st.success("finish wait")
#
# # Balloon 飘气球
# st.balloons()
#
# # SIDEBARS  边栏
# st.sidebar.header("About")
# st.sidebar.text("this is streamlit tut")
#
#
# # Function
#
# # def run_fxn():
# #     return "hello"
# #
# #
# # def app():
# #     st.write(run_fxn())
# # PLOT
