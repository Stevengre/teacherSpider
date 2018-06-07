# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 18:01:21 2018

@author: steven
"""
#import csv
import codecs

class HtmlOutputer(object):
    def __init__(self):
        self.datas=[]
    def collect_data(self,data):
        if data is None:
            return
        self.datas.append(data)
        
    def output_html(self):
        fout=codecs.open("data.xls",'w','utf-8')
        fout.write('id\tname\tpaper1\tpaper2\tpaper3\n')
        count=1
        for data in self.datas:
            fout.write("%d\t"%count)
            fout.write("%s\t"%data['name'])
            fout.write("%s\t"%data['paper1'])
            fout.write("%s\t"%data['paper2'])
            fout.write("%s\n"%data['paper3'])
            count=count+1;

        