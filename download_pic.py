import urllib.request
import os
import time

def url_open(url):
    '''爬取网页信息'''
    #req = urllib.request.Request(url)
    #req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36')#添加一个文件头
    #response = urllib.request.urlopen(url)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    req = urllib.request.Request(url=url,headers=headers)
    
    response = urllib.request.urlopen(req)#注意，这里要用req，不然就被添加useragent
    html = response.read()
    return html

def get_page(url):    
    '''这里是获取要下载图片缩在网页的url'''
    html = url_open(url).decode('utf-8')
    #html = response.read().decode('utf-8')#打开图片所处网页和html文件
    #找到第一个页面的初始页码
    a = html.find('page now-page')+len('page now-page')+2#find找到字符串首字母位置加上23刚好到达页码位置
    b = html.find('</',a)#从a起始，返回第一个右】

    print(html[a:b])#字符串切片，返回页码
    return html[a:b]

    

def find_imgs(url):
    '''    这里使用的url是已经找到并确定了页码的url    '''
    html = url_open(url).decode('utf-8')
    #print(url)
    img_addrs = []#列表用来存放所有找到的图片的地址
    img_addrs2 = []
    img_addrs_in=[]
    #html2=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    html2=[]
    a = html.find('img src=')
   
      
    while a!=-1 :
        #print(a)
        b = html.find('.jpg',a,a+255)#限定开始和结束的范围为a到a+255，避免找到其他地方去
        c = html.find('a href',a-255,a)
        d = html.find('.html',a-255,a)
        if b!=-1 and c!=-1:#就是找到了
            img_addrs.append(html[a+9:b+4])
            img_addrs2.append(html[c+8:d+5])
        else:
            b=a+9
        
        a = html.find('img src="',b)
    
    #print(img_addrs2)
    i=0
    if i<len(img_addrs2):
        for each in img_addrs2:
            in_addrs = str('http://www.yeji2018.com'+each)
            #print(in_addrs)
            #html2[i] = url_open(in_addrs).decode('utf-8')  
            html2.append(url_open(in_addrs).decode('utf-8'))
            #print(html2[i])
            a_1 = html2[i].find('img src=')
            while a_1!=-1 :
                b_1 = html2[i].find('.jpg',a_1,a_1+255)#限定开始和结束的范围为a到a+255，避免找到其他地方去
                #print(a_1,b_1)
                if b_1!=-1 :#就是找到了
                    #print(html2[i][a_1 + 9:b_1+4])
                    img_addrs_in.append(html2[i][a_1 + 9:b_1+4])
                else:
                    b_1=a_1+9        
                a_1 = html2[i].find('img src="',b_1)
            #print(img_addrs_in)
            #print(len(img_addrs2))
            i+=1
            #print(i)
   # for each in img_addrs :
    #    print(each)

    return img_addrs ,img_addrs_in


def save_imgs(folder,img_addrs):
    i=0
    for each in img_addrs:
        a= time.strftime("%Y%m%d_%H%M%S",time.localtime(time.time()))
        filename = a[0:] + each.split('/')[-1] #分割的最后一项作为图片的名字#
        #这里有个优化的地方，文件保存可以采用源文件+时间，避免文件覆盖
        with open(filename,'wb') as f:
            img = url_open(each)
            f.write(img)
        i+=1
        print('Saving ',each,'......  please wait','下载内容为第',str(i),'项','共计有',str(len(img_addrs)),'项')




def download_pic(folder= 'ooxx',pages = 5,need_pages=3):#下次该从第8也开始
    '''http://www.yeji2018.com/picture/zipai/index_2.html'''
    if os.path.exists('ooxx'):
        pass
    else:
        os.mkdir(folder)#创建一个文件夹
    os.chdir(folder)#修改所处路径

    url = 'http://www.yeji2018.com/picture/zipai/'
    page_num = int(get_page(url))#为了模块化设计，定义一个函数，用来获取路径,在这里，用来获取图片页的第一页，找到第一页的图片页码

    for i in range(pages,pages+need_pages):
        page_addr = page_num + i #d得到爬取的页面的计数
        if page_addr == 1 :
            page_url = url+ 'index' '.html' #得到爬取的链接
        else:
            page_url = url+ 'index_' +str(page_addr) + '.html' #得到爬取的链接
        
        print(page_url)
        #找到打开页面里面图片的地址，保存，返回一个列表
        img_addrs,img_addrs2 = find_imgs(page_url)
        #将页面保存下来
        
        print('将开始下载主页图片')
        #save_imgs(folder,img_addrs)
        print('download successful')

        time.sleep(5)
        #dir1 = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))  #获取上一级目录
        #print(dir1)
        #os.chdir(dir1)
            
        print('将开始下载内图')
        save_imgs(folder,img_addrs2)
        print('download successful')



if __name__ == '__main__':
    download_pic()
