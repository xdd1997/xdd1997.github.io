import re
import math
import time

import pandas as pd
from git import Repo

def read_bookmarks(bookmarks_File):
    with open(bookmarks_File, encoding='utf-8', mode='r') as fr:
        content = fr.read()
    str00 = '<DT><H3 ADD_DATE=\"1650468185\"'
    N_folder = content.count(str00)
    folder = re.findall(r'<DT><H3 ADD_DATE=\"1650468185\".*?</DL><p>', content, re.DOTALL)

    URL_LIST = []
    for ii in range(N_folder):
        str_ii = folder[ii]
        folderName = re.findall(r'<DT><H3 ADD_DATE="1650468185" LAST_MODIFIED=\".*\">(.*)</H3>', str_ii)
        tmp = ["Folder", folderName[0]]
        URL_LIST.append(tmp)
        urlList = re.findall(r'<A HREF=\".*(http.*)\" ADD_DATE=\".*>(.*)</A>', str_ii)

        for jj in urlList:
            tmp = [jj[0], jj[1][0:6]]
            URL_LIST.append(tmp)

    return URL_LIST


def save_content_to_xlsx(URL_LIST, xlsxName):
    sum00 = 0
    index = []
    for ii in URL_LIST:
        sum00 += 1
        if ii[0] == "Folder":
            index.append(sum00)
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
            sht1.write(count, 3, "icon-daohang_huaban1")
            Folder_ii += 1
            count += 1
        else:
            sht1.write(count, 2, ii[1])
            sht1.write(count, 3, "icon-shuqian")
            sht1.write(count, 4, ii[0])
            count += 1

    xls.save(xlsxName)

# 确定一共几个类别
def get_N_class(col_class):
    kk = 0
    for ii in col_class:
        if not math.isnan(ii):
            kk += 1
    return kk


# 确定某个类别有几个条目
def get_N_url_of_each_class(col_class, col_url, class_id):
    tmp = col_class.to_list()
    index_id = tmp.index(class_id)
    count = 0
    for ii in range(index_id + 1, len(col_class)):
        if not math.isnan(col_class[ii]):  # 如果是数字，终止循环
            break

        if type(col_url[ii]) == float and math.isnan(col_url[ii]):  # 如果是空，终止循环
            break

        else:
            count += 1
    return count


# 获取某个类别的字符串
def get_html_src_each_class(content, class_id):
    col_class = content.iloc[:, 0]
    col_url = content.iloc[:, 4]
    N_url_each_class = get_N_url_of_each_class(col_class, col_url, class_id)
    # 找到class_id所在行
    tmp = col_class.to_list()
    index_id = tmp.index(class_id)
    TITLE = content.iloc[index_id, 1]
    ICON = content.iloc[index_id, 3]
    str00 = '<ul class="mylist row">\n'
    str00 += '<li class="title"> <svg class="icon" aria-hidden="true"><use xlink:href="#{0}"></use></svg> {1} </li>\n'.format(
        ICON, TITLE)

    for ii in range(index_id + 1, index_id + 1 + N_url_each_class):
        title = content.iloc[ii, 2]
        if type(title) == float and float and math.isnan(title):
            title = ''
        icon = content.iloc[ii, 3]
        url = content.iloc[ii, 4]
        str01 = '<li class="col-3 col-sm-3 col-md-3 col-lg-1"> <a rel="nofollow" href="{0}" target="_blank"><svg class="icon" aria-hidden="true">                 <use xlink:href="#{1}"></use></svg><span>{2}</span></a></li>\n'.format(
            url, icon, title)
        str00 += str01

    str00 += '</ul>\n'
    return str00


def write_index_From_xlsx(xlsxName):
    content = pd.read_excel(xlsxName, sheet_name=0, header=0)
    # 获取两列内容
    col_class = content.iloc[:, 0]
    col_url = content.iloc[:, 4]

    N_class = get_N_class(col_class)
    str_All = '<!--搜索结束--> \n\n'
    for ii in range(N_class):
        class_id = ii + 1
        str_All += get_html_src_each_class(content, class_id)

    str_All += '\n\n<!-- 版权信息 -->'
    # with open("ddx.html", "w", encoding="utf-8") as fw:
    #     fw.write(str_All)

    # 读取已有的 index.html
    html_path = r"..\index.html"
    with open(html_path, 'r', encoding="utf-8") as fr:
        contentOfHtml = fr.read()

    # 替换文本
    pattern = re.compile(r'<!--搜索结束-->.*<!-- 版权信息 -->', re.DOTALL)
    str_to_html = pattern.sub(str_All, contentOfHtml)

    icon_js = content.iloc[0, 4]
    pattern = re.compile(r'//at.alicdn.com/t/font_2561558.*\.js')
    str_to_html = pattern.sub(icon_js, str_to_html)

    # 写出到html
    html_path = r"..\index.html"
    with open(html_path, 'w', encoding="utf-8") as fw:
        fw.write(str_to_html)

    print("\n* * * * * OK，请上传到 github.io * * * * *\n")

def git_operation(repoPath):
    """ python 操作 git 上传 """
    r = Repo(repoPath)
    r.index.add('.')
    timeNow = time.strftime("%Y%m%d%H%M%S", time.localtime())
    r.index.commit(timeNow)
    r.remote().push('master')
    print("\n* * * * * 已使用命令行上传到 github.io * * * * *\n")
    print("\n* * * * * https://xdd1997.github.io/ * * * * *\n")

def main():
    bookmarksFile = r"bookmarks_2022_9_15.html"
    xlsxName = r"url_collectd.xls"
    repoPath = r"D:\Git\xdd1997.github.io"
    # URL_LIST = read_bookmarks(bookmarksFile)
    # save_content_to_xlsx(URL_LIST, xlsxName)
    write_index_From_xlsx(xlsxName)
    # git_operation(repoPath)

if __name__=="__main__":
    main()