import re

with open("bookmarks_2022_5_2.html", encoding='utf-8', mode='r') as fr:
    content = fr.read()
str00 = '<DT><H3 ADD_DATE=\"1650468185\"'
N_folder = content.count(str00)
folder = re.findall(r'<DT><H3 ADD_DATE=\"1650468185\".*?</DL><p>',content, re.DOTALL)

URL_LIST = []
for ii in range(N_folder):

    str_ii = folder[ii]
    print(str_ii)

    folderName = re.findall(r'<DT><H3 ADD_DATE="1650468185" LAST_MODIFIED=\".*\">(.*)</H3>', str_ii)
    tmp = []
    tmp.append("Folder")
    tmp.append(folderName[0])
    URL_LIST.append(tmp)

    urlList = re.findall(r'<A HREF=\".*(http.*)\" ADD_DATE=\".*>(.*)</A>', str_ii)
    print(urlList)
    print(len(urlList))

    for ii in urlList:
        tmp = []
        tmp.append(ii[0])
        tmp.append(ii[1][0:6])
        print(tmp)
        URL_LIST.append(tmp)

print('*'*50)
print(len(URL_LIST))


#with open("xdd_20220502.txt", encoding='utf-8', mode='w') as fw:
#    for ii in URL_LIST:
#        fw.writelines(ii[0] +'\t' + ii[1] + '\n')

# =========================================================================================


sum = 0
index = []
for ii in URL_LIST:
    sum += 1
    if ii[0] == "Folder":
        index.append(sum)
print(len(index))

import xlwt
xls = xlwt.Workbook()
sht1 = xls.add_sheet('sheet1')
sht1.write(0, 0, '级别')
sht1.write(0, 1, '分类')
sht1.write(0, 2, '网址名称')
sht1.write(0, 3, '网址图标')
sht1.write(0, 4, '网址链接')
sht1.write(1, 4, '//at.alicdn.com/t/font_2561558_tda670w6d2t.js')

count = 1
Folder_ii = 1
for ii in URL_LIST:
    if ii[0] == "Folder":
        count += 1
        sht1.write(count, 0, Folder_ii)
        sht1.write(count, 1, ii[1])
        sht1.write(count, 3, "#icon-daohang_huaban1")
        Folder_ii += 1
        count += 1
    else:
        sht1.write(count, 2, ii[1])
        sht1.write(count, 3, "#icon-shuqian")
        sht1.write(count, 4, ii[0])
        count += 1

xls.save('url_collectd_2.xls')
