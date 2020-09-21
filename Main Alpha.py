#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[ ]:


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
print("----------------------------------")


# In[ ]:


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
print("版本 Alpha 0.2.8")
time.sleep(0.1)
print("时间：2020-09-22")
time.sleep(0.1)
print("本软件切勿用于非法用途！")
time.sleep(0.5)
print("----------------------------------")


# In[ ]:


#从得到的图片链接下载图片，并保存
'''
#作废的代码，应用于0.2.7及之前的程序里
def SaveImage(link,InputData,count,overtime):
        
    try: 
        socket.setdefaulttimeout(overtime)
        time.sleep(0.1)
        urllib.request.urlretrieve(link,'./'+InputData+'/'+str(count)+'.jpg')
    except socket.timeout:
        time.sleep(0.1)
        print("链接超时")
    except urllib.error.HTTPError as reason:
        print(reason)
    except Exception:
        time.sleep(0.1)
        print("无效链接")
    else:
        print("已有" + str(count) + "张图")
'''


# In[ ]:


def SaveImage(link,InputData,count,overtime):
    
    try:
        socket.setdefaulttimeout(overtime)
        time.sleep(0.1)
        urllib.request.urlretrieve(link,'./'+InputData+'/'+str(count)+'.jpg')
        print("正在检测网址，请稍后")
        start = time.time()
        size = 0
        path = './'+InputData+'/'+str(count)+'.jpg' #必须是完整路径
        response = requests.get(link,stream = True)#stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载
        chunk_size = 1024#每次块大小为1024
        content_size = int(response.headers['content-length'])#返回的response的headers中获取文件大小信息
        print("文件大小："+str(round(float(content_size/chunk_size/1024),4))+"[MiB]")
        with open(path,'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):#每次只获取一个chunk_size大小
                file.write(data)#每次只写入data大小
                size = len(data)+size
                #'r'每次重新从开始输出，end = ""是不换行
                print('\r'+"【"+str(round(float(size/content_size)*100,2))+"%"+"】"+"已经下载："+int(size/content_size*50)*"█"+" 【"+str(round(size/chunk_size/1024,2))+"MiB】",end="")
        end = time.time()
        print("")
        print("保存图片耗时耗时:"+str(end-start)+"秒")
        #片段的程序来源：https://blog.csdn.net/YiXiao1997/article/details/86721536?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param
        
        print("已有" + str(count) + "张图")
    except socket.timeout:
        time.sleep(0.1)
        print("链接超时")
    except urllib.error.HTTPError as reason:
        print(reason)
    except Exception:
        time.sleep(0.1)
        print("无效链接")
    #else:
        #print("已有" + str(count) + "张图")


# In[ ]:


# 主函数
def main(PageNum,InputData,word,overtime):
    for i in range(PageNum):
        print("-----------------------------------")
        print("-----------------------------------")
        print("-----------------------------------")
        print("-----------------------------------")
        print("正在检索的页数：",i+1)
        print("-----------------------------------")
        print("-----------------------------------")
        print("-----------------------------------")
        print("-----------------------------------")
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
        for StepOne in soup.select('.iusc'):
            link=StepOne.attrs['href']
            url=link
            time.sleep(0.2)
            time1=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("图片开始保存时间：",time1)
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
            link=imageURL
            time.sleep(1)
            count = len(os.listdir('./' + word)) + 1
            overtime=overtime
            SaveImage(link,word,count,overtime)
            time2=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("图片结束保存时间：",time2)
            time2s=time.mktime(time.strptime(time2,"%Y-%m-%d %H:%M:%S"))
            delta=time2s-time1s
            print("保存耗时：",delta)
            print("-----------------------------------")
        #except:
            #print('URL OPENING ERROR !')


# In[ ]:


if __name__=='__main__':
    #输入需要加载的页数，每页35幅图像
    PageNum = int(input("请输入要检索的页数，最大不超过20页:"))
    #输入需要搜索的关键字
    #print("超过该时长放弃保存，若保存大图，建议设置15秒以上")
    overtime=float(input("请设置链接请求超时时长:"))
    word=input("输入需要搜索的关键字:")
    print("-----------------------------------")
    #UTF-8编码
    InputData=urllib.parse.quote(word)
    #print(InputData)
    main(PageNum,InputData,word,overtime)


# In[ ]:


print("-----------------------------------")
input("按下回车键退出程序")


# In[ ]:




