# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 18:00:57 2018

@author: steven
"""
from bs4 import BeautifulSoup
import re
from urllib import parse

class HtmlParser(object):
    def _get_new_urls(self,page_url,soup):
        new_urls=set()
        #href="/publish/cs/4616/2010/20101224144625833818684/20101224144625833818684_.html
        #这里的正则表达式需要进一步细化
        links=soup.find_all('a',href=re.compile(r"/publish/cs/4616/.+_.html"))
        for link in links:
            new_url=link['href']
            new_full_url=parse.urljoin(page_url,new_url)#把new_url以page_url的格式拼接成完整的url
            new_urls.add(new_full_url)
        return new_urls
    
    
    def _get_new_data(self,page_url,soup):
        res_data={}
        #url
        res_data['url']=page_url
        #提取老师姓名
        name_node=soup.find('p',text=re.compile(r'姓名.+'))
        if name_node is not None:
            res_data['name']=name_node.get_text()
            res_data['name']=res_data['name'].replace("姓名：",'')
            res_data['name']=res_data['name'].replace("\n",'')
            res_data['name']=res_data['name'].replace(" ",'')
        #提取老师放在个人主页前三的论文
        paper_node1=soup.find('p',text=re.compile('\[1\].+'))
        paper_node2=soup.find('p',text=re.compile('\[2\].+'))
        paper_node3=soup.find('p',text=re.compile('\[3\].+'))
        if paper_node1 is not None:
            res_data['paper1']=paper_node1.get_text()
#            res_data['paper1']=paper_node1['paper1'].replace("[1]",'')
        if paper_node2 is not None:
            res_data['paper2']=paper_node2.get_text()
#            res_data['paper2']=paper_node2['paper2'].replace("[2]",'')
        if paper_node3 is not None:
            res_data['paper3']=paper_node3.get_text()
#            res_data['paper3']=paper_node3['paper3'].replace("[3]",'')
        return res_data
    
    def parse(self,page_url,html_cont):
        if page_url is None or html_cont is None:
            print('page_url or html_cont is None')
            return
        soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls=self._get_new_urls(page_url,soup)
        new_data=self._get_new_data(page_url,soup)
        return new_urls,new_data
