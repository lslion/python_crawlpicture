# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from python_crawlpicture.items import python_crawlpicture


class Pic169bbSpider(scrapy.Spider):
    name = 'pic_169bb'
    allowed_domains = ['169bb.com']
    start_urls = ['http://169bb.com/']
    next_page = '下一页'
    page_nume = 0

    def parse(self, response):
        title_list = response.xpath(
            "/html/body/div[@class='header']/div[@class='hd_nav']/div[@class='w1000']//a/text()").extract()
        urldata = response.xpath(
            "/html/body/div[@class='header']/div[@class='hd_nav']/div[@class='w1000']//a/@href").extract()
        xiyang_title = title_list[5] # 获取西洋美女标签的文本内容
        xiyang_urldata = urldata[5]  # 获取西洋美女首页网址
        print('Download addr: ' + xiyang_urldata)
        yield Request(url=xiyang_urldata, callback=self.enter_theme, dont_filter=True)

    def enter_theme(self, response):
        self.page_nume = self.page_nume +1
        page_title_list = response.xpath("/html/body//div[@class='w1000 box03']/ul[@class='product01']//li/a/@alt").extract()
        page_url_list = response.xpath("/html/body//div[@class='w1000 box03']/ul[@class='product01']//li/a/@href").extract()
        nextpage_str = response.xpath("/html/body/div[@class='w1000 box03']/div[@class='page']/ul//a/text()").extract()[-2]
        nextpage_url = response.xpath("/html/body/div[@class='w1000 box03']/div[@class='page']/ul//a/@href").extract()[-2]

        for i in range(0, len(page_url_list)):
            gril_page_url = page_url_list[i] # 得到西洋美女页面里面每一个美女的网页网址
            print(gril_page_url)
            yield Request(url=gril_page_url, callback=self.enter_article, dont_filter=True)

        if self.page_nume > 2:
            return

        page_url = self.isnextpage(response.url, str(nextpage_str), nextpage_url)
        if page_url != None:
            print('Main next page URL is: ' + page_url)
            yield Request(url=page_url, callback=self.enter_theme, dont_filter=True)
        pass

    def isnextpage(self, pageurl, nexttext, nexturl):
        if nexttext == self.next_page and 'html' in nexturl:
            next_page_url = pageurl[0:pageurl.rfind('/', 1) + 1]
            next_page_url = next_page_url + nexturl
            return next_page_url
        return


    def enter_article(self, response):
        yield Request(url=response.url, callback=self.getPic, dont_filter=True)

        pages_list = response.xpath("//div[@class='dede_pages']/ul//li/a/text()").extract()
        if len(pages_list) == 0:
            print('only one page')
            return

        next_pages_str = response.xpath("//div[@class='dede_pages']/ul//li/a/text()").extract()[-1]
        next_page_url = response.xpath("//div[@class='dede_pages']/ul//li/a/@href").extract()[-1]
        page_url = self.isnextpage(response.url, str(next_pages_str), next_page_url)
        if page_url != None:
            print('Sub next page URL is: ' + page_url)
            yield Request(url=page_url, callback=self.enter_article, dont_filter=True)
        pass

    def getPic(self, response):
        print(response.url)
        item = python_crawlpicture()
        item['referer_url'] = response.url
        item['image_urls'] = response.xpath("//div[@class='big-pic']/div[@class='big_img']//p/img/@src").extract()

        #head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
        #request.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24')
        #request.urlretrieve('http://724.169pp.net/169mm/201801/049/3.jpg', filename=file)
        #print('Final Download :', file)
        # pass
        yield item