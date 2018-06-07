# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 16:16:51 2018

@author: steven
"""
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
#import codecs
import xlwt

#class ProssessMaim(object):
#    pass

if __name__=="__main__":
    #在组内对各位老师进行影响力计算
    #中间结果：分组id，作者id，论文id，影响因子，引用，组内人数
    #最终结果：分组id，作者id，影响力指标，组内排名
    df0=pd.read_csv('all_data_fourth_version.csv')
    df1=pd.read_csv('Group.csv')
    df2=pd.DataFrame(columns={'number_of_members','reference_times','impact_factor','paper_id','author_id','team_id'})
    
    
#    number_of_papers=3
    t=0
    temp=0
    
    while t<61:
        t1=0
        while t1<183:
            if(df1['author_id'][t]==df0['author_id'][t1]):
                df2.loc[temp]={'number_of_members':list(df1['team_id']).count(df1['team_id'][t]),'reference_times':df0['reference_times'][t1],'impact_factor':df0['impact_factor'][t1],'paper_id':df0['paper_id'][t1],'author_id':df0['author_id'][t1],'team_id':df1['team_id'][t]}
                temp=temp+1
            t1=t1+1
        t=t+1
    
    #按组对引用和影响力因子进行排序，并且给予重新的分值
    #1.剔除引用和影响力因子中的nan值
#    #############df2是按照作者id排好顺序的
#    t=0
#    dft=df2
#    while t<182:
#        if(dft['author_id'][t]>dft['author_id'][t+1]):
#            print('False')
#            break
#        t=t+1
#    print('True')
    
    dft=df2.fillna(value=-1)
    i=0
    j=0
    tr=0#temp reference_time
    trn=0
    ti=0#temp impact_factor
    tin=0
    while i<=dft.shape[0]:
        if(j<3):
            if(dft['reference_times'][i] != -1):
                tr=tr+dft['reference_times'][i]
                trn=trn+1
            if(dft['impact_factor'][i] != -1):
                ti=ti+dft['impact_factor'][i]
                tin=tin+1
            j=j+1
            i=i+1
        else:
            if(trn==0):
                j=1
                while j<=3:
                    dft['reference_times'][i-j]=tr
                    j=j+1
            elif(trn<3):
                tr=tr/trn
                j=1
                while j<=3:
                    if(dft['reference_times'][i-j] == -1):
                        dft['reference_times'][i-j]=tr
                    j=j+1                
            if(tin==0):
                j=1
                while j<=3:
                    dft['impact_factor'][i-j]=ti
                    j=j+1
            elif(tin<3):
                j=1
                ti=ti/tin
                while j<=3:
                    if(dft['impact_factor'][i-j] == -1):
                        dft['impact_factor'][i-j]=ti
                    j=j+1
            j=0
            tr=0
            trn=0
            ti=0
            tin=0
            if(i==dft.shape[0]):
                break
        
    #2.按照分组号进行排序，将相同的分组放在一起
    i=1
    dfs=[]
    while(not df2.query('team_id == ['+str(i)+']').empty):
        dfs.append(dft.query('team_id == ['+str(i)+']'))
        i=i+1
    #3.在组内按照影响力因子进行排序，重新得到归一化的影响力因子
    i=0
    len_dfs=len(dfs)
    while i<len_dfs:
        dfs[i]=dfs[i].sort_values(by=['impact_factor'])
        dfs[i]=dfs[i].reset_index(drop = True)
        i=i+1
    i=0
    while i<len_dfs:
        j=0
        k=0
        last=-1
        while j<len(dfs[i]):
            if(dfs[i]['impact_factor'][j]!=last):
                last=dfs[i]['impact_factor'][j]
                k=k+1
            dfs[i]['impact_factor'][j]=k
            j=j+1
        i=i+1
    #4.在组内按照引用进行排序，获得引用的归一化的值
    i=0
    while i<len_dfs:
        dfs[i]=dfs[i].sort_values(by=['reference_times'])
        dfs[i]=dfs[i].reset_index(drop = True)
        i=i+1
    i=0
    while i<len_dfs:
        j=0
        k=0
        last=-1
        while j<len(dfs[i]):
            if(dfs[i]['reference_times'][j]!=last):
                last=dfs[i]['reference_times'][j]
                k=k+1
            dfs[i]['reference_times'][j]=k
            j=j+1
        i=i+1
    #5.将每个作者的三篇论文的引用和影响力因子相称然后相加，作为dff的影响力指标，初始组内排名均为-1
    i=0
    while i<len_dfs:
        dfs[i]['author_impact_factor_one']=None
        i=i+1
    i=0
    while i<len_dfs:
        j=0
        while j<len(dfs[i]):
            dfs[i]['author_impact_factor_one'][j]=dfs[i]['reference_times'][j]*dfs[i]['impact_factor'][j]
            j=j+1
        i=i+1
    i=0
    while i<len_dfs:
        dfs[i]=dfs[i].sort_values(by=['author_id'])
        dfs[i]=dfs[i].reset_index(drop = True)
        i=i+1
    #6.对dff中的影响力指标，在组内进行排序，排序后获得排名
    i=0
    resualt=[]
    while i<len_dfs:
        j=1
        k=0
        dff=pd.DataFrame(columns={'rank','author_impact_factor','author_id','team_id'})
        last=dfs[i]['author_id'][0]
        while j<len(dfs[i]):
            if(last==dfs[i]['author_id'][j]):
                dfs[i]['author_impact_factor_one'][j]=dfs[i]['author_impact_factor_one'][j]+dfs[i]['author_impact_factor_one'][j-1]
            else:
                last=dfs[i]['author_id'][j]
                dff.loc[k]={'rank':0,'author_impact_factor':dfs[i]['author_impact_factor_one'][j-1],'author_id':dfs[i]['author_id'][j-1],'team_id':dfs[i]['team_id'][j-1]}
                k=k+1
            j=j+1
        dff.loc[k]={'rank':0,'author_impact_factor':dfs[i]['author_impact_factor_one'][j-1],'author_id':dfs[i]['author_id'][j-1],'team_id':dfs[i]['team_id'][j-1]}
        resualt.append(dff)
#        if(dfs[i]['number_of_members'][0]==k+1):
#            print('ok\n\n')
#        else:
#            print('NOOOOOOOOOOOOOOOOOOOO\n\n')
        i=i+1
    i=0
    while i<len(resualt):
        resualt[i]=resualt[i].sort_values(by=['author_impact_factor'],ascending=False)
        resualt[i]=resualt[i].reset_index(drop = True)
        j=0
        while j<len(resualt[i]):
            resualt[i]['rank'][j]=j+1
            j=j+1
        i=i+1    
    #7.写成xlsx表格
    tables = xlwt.Workbook(encoding='utf-8', style_compression=0)
    i=0
    while i<len(resualt):
        sheet=tables.add_sheet('team_'+str(resualt[i]['team_id'][0]),cell_overwrite_ok=True)
        sheet.write(0,0,'rank')
        sheet.write(0,1,'author_id')
        sheet.write(0,2,'author_impact_factor')
        j=0
        while j<len(resualt[i]):
            sheet.write(j+1,0,resualt[i]['rank'][j])
            sheet.write(j+1,1,resualt[i]['author_id'][j])
            sheet.write(j+1,2,resualt[i]['author_impact_factor'][j])
            j=j+1
        i=i+1
    tables.save(r'result.xls')
    
    
    
 
    
#######################################################################
#    #进行分组，记录老师id和分组号和相关值，若是相关值更高则分相关值高的分组
#    df=pd.DataFrame(columns={'author_id','team_id','similarity_degree'})
#    ai=1
#    ti=1
#    sd=0
#    #初始化df
#    while ai<=61:
#        df.loc[ai-1]={'author_id':ai,'team_id':0,'similarity_degree':-1}
#        ai=ai+1
#    #进行分组
#    dataset=pd.read_csv('Similarity.csv')
#    ai=1
#    while ai<=61:
#        ai2=1
#        if(df['team_id'][ai-1]==0):
#            df['team_id'][ai-1]=ti
#            while ai2<=61:
#                if((ai2!=ai) & (dataset[str(ai2-1)][ai-1]!=0)):
#                    if(dataset[str(ai2-1)][ai-1]>df['similarity_degree'][ai2-1]):
#                        df['team_id'][ai2-1]=ti
#                        df['similarity_degree'][ai2-1]=dataset[str(ai2-1)][ai-1]
#                ai2=ai2+1
#            ti=ti+1
#        else:
#            while ai2<=61:
#                if((ai2!=ai) & (dataset[str(ai2-1)][ai-1]>df['similarity_degree'][ai-1])):
#                    if(df['team_id'][ai2-1]!=0):
#                        df['team_id'][ai-1]=df['team_id'][ai2-1]
#                        df['similarity_degree'][ai-1]=dataset[str(ai2-1)][ai-1]
#                    else:
#                        df['team_id'][ai-1]=ti
#                        df['team_id'][ai2-1]=ti
#                        df['similarity_degree'][ai-1]=dataset[str(ai2-1)][ai-1]
#                        df['similarity_degree'][ai2-1]=dataset[str(ai2-1)][ai-1]
#                ai2=ai2+1
#        ai=ai+1
#    df.to_csv('Group.csv',index=0)
    




    
    
######################################################################    
#    #计算相似度，并且生成一个老师和所有其他老师相似度的表
#    dataset=pd.read_csv('all_data_fourth_version.csv')
#    a=np.eye(61)
#    a=a*4
#    
#    a1=1
#    while a1<=61:#61个作者
#        print(a1)
#        a2=a1+1#和除了自己意外的作者进行相似度比较
#        while a2<=61:
#            t=0
#            p1=0
#            while p1<3:
#                k1=0
#                flag1=False
#                #一个作者三个文章的所有关键词
#                while k1<6:
#                    flag2=False
#                    if(dataset['key'+str(k1)][a1-1+p1*61] is not np.nan):
#                        p2=0
#                        while p2<3:
#                            k2=0
#                            #另一个作者三篇文章的所有关键词
#                            while k2<6:
#                                if(dataset['key'+str(k1)][a1-1+p1*61]==dataset['key'+str(k2)][a2-1+p2*61]):
#                                    flag2=True
#                                    flag1=True
#                                    t=t+1
#                                    break
#                                k2=k2+1
#                            p2=p2+1
#                    if(flag2):
#                        break
#                    k1=k1+1
#                if(flag1):
#                    break
#                p1=p1+1
#            a[a1-1][a2-1]=t
#            a[a2-1][a1-1]=a[a1-1][a2-1]
#            print(a2)
#            a2=a2+1
#        a1=a1+1
#    pd_data = pd.DataFrame(a)
#    print(pd_data)
#    pd_data.to_csv('Similarity.csv')
    
#    #文件预处理，去除前面的空格
#    dataset=pd.read_csv('all_data_second_version.csv')
#    i=0
#    while i<dataset.shape[0]:
#        j=0
#        while j<6:
#            if(dataset['key'+str(j)][i] is not np.nan):
#                print(dataset['key'+str(j)][i],'=>',end=' ')
#                dataset['key'+str(j)][i]=str.lstrip(dataset['key'+str(j)][i])
#                print(dataset['key'+str(j)][i])
#            j=j+1
#        i=i+1
#    dataset.to_csv('all_data_third_version.csv')       
        
        
 

#########################################################################      
    #输出所有的key给老师查看
#    dataset=pd.read_csv('all_data_third_version.csv')
#    #建立一个集合，里面存储所有不相同的key
#    new_set=set()
#    i=0
#    while i<dataset.shape[0]:
#        j=0
#        while j<6:
#            if(dataset['key'+str(j)][i] is not np.nan):
#                if(dataset['key'+str(j)][i] not in new_set):
#                    new_set.add(dataset['key'+str(j)][i])
#                print(dataset['key'+str(j)][i])
#            j=j+1
#        i=i+1
#    fout=codecs.open("data.csv",'w','utf-8')
#    fout.write('kinds_of_work\n')
#    for new_data in new_set:
#        fout.write('%s\n'%new_data)        



        
        
#########################################################################
#    #文件预处理，将所有的都转化为小写字符,
#    dataset=pd.read_csv('all_data_first_version.csv')
#    i=0
#    while i<dataset.shape[0]:
#        j=0
#        while j<6:
#            if(dataset['key'+str(j)][i] is not np.nan):
#                print(dataset['key'+str(j)][i],'=>',end=' ')
#                dataset['key'+str(j)][i]=str.lower(dataset['key'+str(j)][i])
#                print(dataset['key'+str(j)][i])
#            j=j+1
#        i=i+1
#    dataset.to_csv('all_data_second_version.csv')