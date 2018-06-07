# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 17:59:30 2018

@author: steven
"""
from teacher_spider import url_manager
from teacher_spider import html_downloader
from teacher_spider import html_parser
from teacher_spider import html_outputer


class SpiderMain(object):
    def __init__(self):
        self.urls=url_manager.UrlManager()
        self.downloader=html_downloader.HtmlDownloader()
        self.parser=html_parser.HtmlParser()
        self.outputer=html_outputer.HtmlOutputer()
        
    def craw(self,root_url):
        count=0
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url=self.urls.get_new_url()
                # print('craw %d : %s'%(count,new_url))
                print('%d'%count)
                html_cont=self.downloader.download(new_url)
                new_urls,new_data=self.parser.parse(new_url,html_cont)
                self.urls.add_new_urls(new_urls)
                print(new_data['name'])
                print(new_data['paper1'])
                print(new_data['paper2'])
                print(new_data['paper3'])
                self.outputer.collect_data(new_data)
                if count==1000:
                    break
            
                count=count+1
            except:
                print('craw failed')
            
        self.outputer.output_html()
            
        
if __name__=="__main__":
    root_url="http://www.cs.tsinghua.edu.cn/publish/cs/4797/index.html"
    obj_spider=SpiderMain()
    obj_spider.craw(root_url)