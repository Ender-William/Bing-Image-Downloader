#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PySimpleGUI as sg  
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import time
import requests
from lxml import etree
import re
import socket
import sys
from tqdm import tqdm
import requests#引入requests库
import time#引入time，计算下载时间
import tkinter as tk
import io  
from PIL import Image, ImageTk 
import threading
from tkinter import Tk, Checkbutton, Label
from tkinter import StringVar, IntVar
import cv2
from PIL import Image, ImageTk


# In[2]:


'''
通过继承threading.Thread类来避免
创建的窗口在搜索并下载数据的时候出现
卡死的情况，不过使用这种方法可能导致
程序同时执行多个搜索和下载任务，这点
必须在0.2.9版本之后完成更新来避免此
类情况。原因是因为程序需要实时显示保
存情况和保存完的图片的预览。
'''
class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


# In[3]:


def SaveImage(link,InputData,count,overtime):
    try: 
        print("正在检测网址，请稍后")
        content = "正在检测网址，请稍后"
        window.Element('_Multiline_').Update(content)
        socket.setdefaulttimeout(overtime)
        time.sleep(0.1)
        print("正在下载图片，请稍后")
        content = "正在下载图片，请稍后"
        window.Element('_Multiline_').Update(content)
        urllib.request.urlretrieve(link,'./'+InputData+'/'+str(count)+'.jpg')
        urllib.request.urlretrieve(link,'./'+"Preview"+'/'+str(count)+'.png')
    except socket.timeout:
        time.sleep(0.1)
        print("链接超时")
        content ="链接超时"
        
        window.Element('_Multiline_').Update(content)
    except urllib.error.HTTPError as reason:
        print(reason)
        content =reason
        window.Element('_Multiline_').Update(content)
    except Exception:
        time.sleep(0.1)
        print("无效链接")
        content ="无效链接"
        window.Element('_Multiline_').Update(content)
    else:
        print("已有" + str(count) + "张图")
        content = str(count)
        window.Element('Picture_Num').Update(content)
        time.sleep(0.1)
        try:
            Path ='./'+"Preview"+'/'+str(count)+'.png'
            picture_type = 'png'
            newpath = 'Preview'
            if not os.path.exists(newpath):
                os.mkdir(newpath)

            #portion = os.path.splitext(Path)
            #print('convert  ' + newpath +'  to '+portion[0]+'.'+picture_type)
            img = cv2.imread(Path)
            cv2.imwrite("./"+newpath+"/"+str(count)+'.'+picture_type,img)
            #photo = ImageTk.PhotoImage(file=Path)
            NPATH = "./"+newpath+"/"+str(count)+'.'+picture_type
            window.Element('Image').Update(NPATH,size=(1100, 1100),visible=True)
        except:
            content = 'CV2 模组错误，无法预览图片'
            window.Element('_Multiline_').Update(content)
            time.sleep(0.1)


# In[4]:


# 主函数
def main(PageNum,InputData,word,overtime):
    for i in range(PageNum):
        print("正在检索的页数：",i+1)
        NUM =i+1
        content = "正在检索的页数："+ str(NUM)
        window.Element('_Multiline_').Update(content)
        #try:
        url = 'http://cn.bing.com/images/async?q={0}&first={1}&count=35&relp=35&lostate=r&mmasync=1&dgState=x*175_y*848_h*199_c*1_i*106_r*0'
        #定义请求头
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        page1 = urllib.request.Request(url.format(InputData, i*35+1), headers=headers)
        page = urllib.request.urlopen(page1)
        #使用beautifulSoup进行解析网页
        soup = BeautifulSoup(page.read(), 'html.parser')
        #print(soup)
        #创建文件夹
        if not os.path.exists("./" + word):
            os.mkdir('./' + word)
        if not os.path.exists("./" + "Preview"):
            os.mkdir('./' + "Preview")
        for StepOne in soup.select('.iusc'):
            
            link=StepOne.attrs['href']
            url=link
            time.sleep(0.2)
            time1=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("图片开始保存时间：",time1)
            content ="图片开始保存时间："+ time1
            window.Element('_Multiline_').Update(content)
            time1s=time.mktime(time.strptime(time1,"%Y-%m-%d %H:%M:%S"))
            #print("原始访问链接：",url)
            
            #通过正则表达式检索照片格式
            mainURL=url.split("%3a%2f%2f",1)
            mainURL=mainURL[1]
            #print(mainURL)
            otherURL=mainURL.split(".jpg",1)
            otherURL=otherURL[0].replace("%2f","/")
            #print("list",otherURL)
            imageURL="http://"+otherURL+".jpg"
            print("图像链接：",imageURL)
            content = "图像链接："+ imageURL
            window.Element('_Multiline_').Update(content)
            link=imageURL
            time.sleep(1)
            count = len(os.listdir('./' + word)) + 1
            overtime=overtime
            SaveImage(link,word,count,overtime)
            time2=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("图片结束保存时间：",time2)
            content = "图片结束保存时间：" + time2
            window.Element('_Multiline_').Update(content)
            time2s=time.mktime(time.strptime(time2,"%Y-%m-%d %H:%M:%S"))
            delta=time2s-time1s
            print("保存耗时：",delta)
            content = "保存耗时：" + str(delta)
            window.Element('_Multiline_').Update(content)
            print("-----------------------------------")
        #except:
            #print('URL OPENING ERROR !')
    content = "完成下载"
    window.Element('_Multiline_').Update(content)


# In[5]:


def Start_Search ():
    PageNum = value['_PageNum_']
    PageNum = int(PageNum)
    overtime = value['_OverTime_']
    overtime = float(overtime)
    word = value['_KeyWords_']
    InputData=urllib.parse.quote(word)
    main(PageNum,InputData,word,overtime)


# In[6]:


import PySimpleGUI as sg


# 创建布局
layout = [
    [sg.Text('请输入页数',font=(30), justification='center'), sg.Input(key='_PageNum_',size = (50,1))],
    [sg.Text('请输入时长',font=(30), justification='center'), sg.Input(key='_OverTime_',size = (50,1))],
    [sg.Text('输入关键字',font=(30), justification='center'), sg.Input(key='_KeyWords_',size = (50,1))],
    [sg.Btn('开始检索', key='_START_',font=(30)),sg.Btn('终止检索', key='_END_',font=(30))],
    [sg.Text('已有图片张数：',font=(30), justification='center'),
     sg.Text('0',key ='Picture_Num',size = (5,1),font=(30), justification='center')],
    [sg.Multiline('还未开始检索', key = '_Multiline_',size = (40,10),autoscroll = True ,font=(30)),
     sg.Image(size=(1100,1100),filename=r"logo.jpg",key = 'Image',visible=True)],
    #[sg.Image(size=(1100,1100),
           #   filename=r"logo.jpg",key = 'Image')]
]


# 创建窗口，引入布局，并进行初始化
# 创建时，必须要有一个名称，这个名称会显示在窗口上
window = sg.Window('Picture search and downloader Alpha 0.2.9', layout=layout, finalize=True)

while True:  # 创建一个事件循环，否则窗口运行一次就会被关闭
    event, value = window.Read()  # event, value 的值分别是 _LOGIN_ {'_USER_': 'admin', '_PWD_': '123'}
    # print(event, value)  # 可以打印一下看看变量的内容
    if event is None:   # 如果事件的值为 None，表示点击了右上角的关闭按钮
        break
    if event == '_END_':   # 
        break
    if event == '_START_':  # 当获取到事件时，处理逻辑
        #print(InputData)
        MyThread(Start_Search)
        


window.close()


# In[ ]:




