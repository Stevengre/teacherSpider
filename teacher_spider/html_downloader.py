# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 18:00:21 2018

@author: steven
"""
import urllib.request
class HtmlDownloader(object):
    def download(self,url):
        if url is None:
            return None
        response=urllib.request.urlopen(url)
        if response.getcode()!=200:
            return None
        return response.read()
        
