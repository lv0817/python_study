import urllib.request
import re

def open_url(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','ozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36')
    page = urllib.request.urlopen(req)
    html = page.read().decode('utf-8')

    return html

def get_img(html):
    '''从给定的网页中利用正则表达式匹配对象'''
    p = r'<img class="BDE_Image" src="([^"]+\.jpg)'
    imglist = re.findall(p,html)
    '''
    for each in imglist:
        print(each)
    '''
    for each in imglist :
        filename = each.split('/')[-1]
        urllib.request.urlretrieve(each,filename,None)
        

if __name__ == '__main__':
    url = 'https://tieba.baidu.com/p/5393582905'
    get_img(open_url(url))