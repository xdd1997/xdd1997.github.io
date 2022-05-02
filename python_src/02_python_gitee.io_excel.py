#!/usr/bin/env python
# coding: utf-8

import os
import math

try:
    import pandas as pd
except:
    str00 = 'pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple'
    os.system(str00)
    import pandas as pd


# 确定一共几个类别
def get_N_class(col_class):
    kk = 0
    for ii in col_class:
        if not math.isnan(ii):
            kk += 1
    return kk

# 确定某个类别有几个条目
def get_N_url_of_each_class(col_class,col_url,class_id):

    tmp = col_class.to_list()
    index_id = tmp.index(class_id)
    count = 0
    for ii in range(index_id+1,len(col_class)):
        if not math.isnan(col_class[ii]) :  # 如果是数字，终止循环
            break

        if type(col_url[ii])==float and math.isnan(col_url[ii]):  # 如果是空，终止循环
            break

        else:
            count += 1
    return count

# 获取某个类别的字符串
def get_html_src_each_class(content,class_id):
    col_class = content.iloc[:,0]
    col_url = content.iloc[:,4]
    N_url_each_class = get_N_url_of_each_class(col_class,col_url,class_id)
    # 找到class_id所在行
    tmp = col_class.to_list()
    index_id = tmp.index(class_id)
    TITLE = content.iloc[index_id,1]
    ICON = content.iloc[index_id,3]
    str00 = '<ul class="mylist row">\n'
    str00 += '<li class="title"><svg class="icon" aria-hidden="true"><use xlink:href="{0}">             </use></svg> {1} </li>\n'.format(ICON,TITLE)

    for ii in range(index_id+1,index_id+1+N_url_each_class):
        title = content.iloc[ii,2]
        if type(title) == float and float and math.isnan(title):
            title = ''
        icon = content.iloc[ii,3]
        url = content.iloc[ii,4]
        str01 = '<li class="col-3 col-sm-3 col-md-3 col-lg-1">                 <a rel="nofollow" href="{0}" target="_blank"><svg class="icon" aria-hidden="true">                 <use xlink:href="{1}"></use></svg><span>{2}</span></a></li>\n'.format(url,icon,title)
        str00 += str01
        
    str00 += '</ul>\n'
    return str00

excelPath = r"url_collectd_2.xls"
content = pd.read_excel(excelPath,sheet_name=0,header=0)

# 获取两列内容
col_class = content.iloc[:,0]
col_url = content.iloc[:,4]


N_class = get_N_class(col_class)
str_All = '<!--搜索结束--> \n\n'
for ii in range(N_class):
    class_id = ii + 1
    str_All += get_html_src_each_class(content,class_id)
    
str_All += '\n\n<!-- 版权信息 -->'
with open("ddx.html","w",encoding="utf-8") as fw:
    fw.write(str_All)



html_path = r"..\index.html"
with open(html_path,'r',encoding="utf-8") as fr:
    contentOfHtml = fr.read()

# 替换文本
import re

pattern = re.compile(r'<!--搜索结束-->.*<!-- 版权信息 -->',re.DOTALL)
str_to_html = pattern.sub(str_All,contentOfHtml)

icon_js = content.iloc[0,4]
pattern = re.compile(r'//at.alicdn.com/t/font_2561558.*\.js')
str_to_html = pattern.sub(icon_js,str_to_html)

# 写出到html
html_path = r"..\index.html"
with open(html_path,'w',encoding="utf-8") as fw:
    fw.write(str_to_html)


print(str_All)
print("\n\n* * * * * OK，请打开Git上传 * * * * *\n\n")

 



