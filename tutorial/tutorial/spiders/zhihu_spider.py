import scrapy

from tutorial.items import ZhihuItem

class ZhihuSpider(scrapy.Spider):#必须是继承于子类的
    name = 'zhihu'#确定网页名字
    allowed_domain = ['nuc,edu.cn']#爬取范围，就算网页上有其他链接，爬虫也不会爬到其他网页
    start_urls =[
        'http://lxy.nuc.edu.cn/info/1026/3240.htm',
        'http://lxy.nuc.edu.cn/info/1026/3245.htm'
    ]  #爬取的范围
    '''这里在爬的时候遇到403和500两个问题，这是由于反爬的存在，所以先用两个不会反爬的网址测试'''
    def parse(self,response):
        '''downloader 接受response交给spider并给item'''
        '''
        filename = response.url.split('/')[-1]
        with open(filename,'wb') as f :
            f.write(response.body)
        '''
        sel =scrapy.selector.Selector(response)#这里要把response参数穿进去，不然不知道筛选哪一个
        sites = sel.xpath('//ul[@class = "directory-url"]/li')    
        items=[]
        for site in sites:
            item = ZhihuItem
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').extract()
            print(title,link,desc)
            items.append(item)

        return items