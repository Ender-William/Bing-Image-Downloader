#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time#引入time，计算下载时间


# In[2]:


print("___    __    _________          ")
print("| |   / /    |  ____  \         ")
print("| |  / /     | |    \  \        ")
print("| | / /      | |     \  \       ")
print("| |/ /       | |     |  |       ")
print("| |_ \       | |     |  |       ")
print("| | \ \      | |     |  |       ")
print("| |  \ \     | |     /  /       ")
print("| |   \ \    | |____/  /        ")
print("|_|    \_|   |________/         ")
print("----------------------------------")
#程序声明
time.sleep(0.1)
print("本程序从必应图片下载大图")
time.sleep(0.1)
print("最多搜索20页的内容")
time.sleep(0.1)
print("作者：KDKDKD！")
time.sleep(0.1)
print("部分代码来自于开源社区")
time.sleep(0.1)
print("版本 Alpha 0.3.1")
time.sleep(0.1)
print("时间：2020-11-02")
time.sleep(0.1)
print("本软件切勿用于非法用途！")
time.sleep(0.1)
print("程序正在加载，请稍等")
time.sleep(0.5)
print("----------------------------------")


# In[3]:


print("import PySimpleGUI as sg")
import PySimpleGUI as sg
print("import urllib.request")
import urllib.request
print("import urllib.parse")
import urllib.parse
print("from bs4 import BeautifulSoup")
from bs4 import BeautifulSoup
print("from urllib.request import urlopen")
from urllib.request import urlopen
print("import os")
import os
print("from lxml import etree")
from lxml import etree
print("import re")
import re
print("import socket")
import socket
print("import sys")
import sys
print("from tqdm import tqdm")
from tqdm import tqdm
print("import requests")
import requests#引入requests库
print("import io  ")
import io  
print("from PIL import Image, ImageTk ")
from PIL import Image, ImageTk 
print("import threading")
import threading
print("from tkinter import Tk, Checkbutton, Label")
from tkinter import Tk, Checkbutton, Label
print("from tkinter import StringVar, IntVar")
from tkinter import StringVar, IntVar
print("import cv2")
import cv2
print("import inspect")
import inspect
print("import ctypes")
import ctypes
print("import itertools")
import itertools
print("import _thread")
import _thread

time.sleep(0.5)
print("----------------------------------")
print("Python库加载完毕")
print("----------------------------------")


# In[4]:


'''
通过继承threading.Thread类来避免
创建的窗口在搜索并下载数据的时候出现
卡死的情况，不过使用这种方法可能导致
程序同时执行多个搜索和下载任务，这点
必须在0.2.8版本之后完成更新来避免此
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
        


# In[5]:


'''
这段程序是用作终止子线程而使用的，
避免在终止搜索图片之后重新打开一次
程序，减少了时间上的浪费
'''
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


# In[6]:


def SaveImage(link,InputData,count,overtime):
    try: 
        '''
        这段程序向目标网址发出链接请求
        并检测反馈时间和反馈类型
        '''
        print("正在检测网址，请稍后")
        content = "正在检测网址，请稍后"
        window.Element('_Multiline_').Update(content)
        socket.setdefaulttimeout(overtime) #设定访问超时时长
        time.sleep(0.1)
        '''
        假设链接可以访问，则开始下载并保存图片
        '''
        print("正在下载图片，请稍后")
        content = "正在下载图片，请稍后"
        window.Element('_Multiline_').Update(content)
        urllib.request.urlretrieve(link,'./'+InputData+'/'+str(count)+'.jpg')
        urllib.request.urlretrieve(link,'./'+"Preview"+'/'+str(count)+'.png')
    except socket.timeout:
        #链接超时，抛出异常
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
            '''
            使用OpenCV模组读取jpg格式的图片
            并将图片转化为png格式的图片后保存
            至Preview文件夹内。Preview文件
            夹内的图片是为了图形化界面预览使用
            '''
            Path ='./'+"Preview"+'/'+str(count)+'.png'
            picture_type = 'png'
            newpath = 'Preview'
            

            
            img = cv2.imread(Path)
            NPATH = "./"+newpath+"/"+str(count)+'.'+picture_type

            '''
            这段程序将使图片适应软件窗口500x500的大小
            '''
            x, y = img.shape[0:2] # 获取图片的宽与高 x y
 
            if x < y:
                Scale = y // 500
                if y <=1:
                    SC = y/500
                    img = cv2.resize(img,dsize=None,fx=SC,fy=SC, interpolation=cv2.INTER_NEAREST)
                    cv2.imwrite(NPATH,img)
                else:
                    SC = 500/y
                    img = cv2.resize(img,dsize=None,fx=SC,fy=SC,interpolation=cv2.INTER_NEAREST)
                    cv2.imwrite(NPATH,img)

            else:
                Scale = x // 500
                if x <=1:
                    SC = x/500
                    img = cv2.resize(img,dsize=None,fx=SC,fy=SC,interpolation=cv2.INTER_NEAREST)
                    cv2.imwrite(NPATH,img)
                else:
                    SC = 500/x
                    img = cv2.resize(img,dsize=None,fx=SC,fy=SC,interpolation=cv2.INTER_NEAREST)
                    cv2.imwrite(NPATH,img)


            img = cv2.imread(NPATH)
            cv2.imwrite("./"+newpath+"/"+str(count)+'.'+picture_type,img)
            window.Element('Image').Update(NPATH,size=(500, 500),visible=True)

        except:
            content = 'CV2 模组错误，无法预览图片'
            window.Element('_Multiline_').Update(content)
            time.sleep(0.1)


# In[7]:


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
            time.sleep(0.1)
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
    window.Element('_STOP_').Update(disabled = True)
    window.Element('_START_').Update(disabled = False)


# In[8]:


def Start_Search ():
    PageNum = value['_PageNum_']
    PageNum = int(PageNum)
    overtime = value['_OverTime_']
    overtime = float(overtime)
    word = value['_KeyWords_']
    InputData=urllib.parse.quote(word)
    main(PageNum,InputData,word,overtime)


# In[9]:


# 创建布局
layout = [
    [sg.Text('请输入页数',font=(30), justification='center'), sg.Input(key='_PageNum_',size = (50,1))],
    [sg.Text('请输入时长',font=(30), justification='center'), sg.Input(key='_OverTime_',size = (50,1))],
    [sg.Text('输入关键字',font=(30), justification='center'), sg.Input(key='_KeyWords_',size = (50,1))],
    [sg.Btn('开始检索', key='_START_',font=(30),disabled=False),
     sg.Btn('终止检索', key='_STOP_',font=(30),disabled=True)],
    [sg.Text('已有图片张数：',font=(30), justification='center'),
     sg.Text('0',key ='Picture_Num',size = (5,1),font=(30), justification='center')],
    [sg.Multiline('还未开始检索', key = '_Multiline_',size = (40,10),autoscroll = True ,font=(30)),
     sg.Image(size=(500,500),filename=r"logo.png",key = 'Image',visible=True)],
]


# 创建窗口，引入布局，并进行初始化
# 创建时，必须要有一个名称，这个名称会显示在窗口上
window = sg.Window('Picture search and downloader Alpha 0.3.1', layout=layout, finalize=True)


#Start_Search = MyThread
threading = threading
MyThread = threading.Thread(target=Start_Search)
while True:  # 创建一个事件循环，否则窗口运行一次就会被关闭
    
    event, value = window.Read()  # event, value 的值分别是 _LOGIN_ {'_USER_': 'admin', '_PWD_': '123'}
    # print(event, value)  # 可以打印一下看看变量的内容
    if event is None:   # 如果事件的值为 None，表示点击了左上角的关闭按钮
        break
    if event == '_STOP_':   # 
        window.Element('_START_').Update(disabled = False)
        window.Element('_STOP_').Update(disabled = True)
        content = "正在终止检索"
        print(content)
        window.Element('_Multiline_').Update(content)
        time.sleep(1)
        #break
        stop_thread(MyThread)
        #MyThread.pause
        MyThread.join()
        content = "正在回收线程"
        print(content)
        window.Element('_Multiline_').Update(content)
        time.sleep(1)
        #window.Element('_STOP_').Update(disabled = True)
        content = "已经终止检索"
        print(content)
        window.Element('_Multiline_').Update(content)
    if event == '_START_':  # 当获取到事件时，处理逻辑
        MyThread = threading.Thread(target=Start_Search)
        MyThread.start()
        window.Element('_START_').Update(disabled = True)
        window.Element('_STOP_').Update(disabled = False)


window.close()


# In[ ]:




