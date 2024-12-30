'''
Author: CatalyzeSec
LastEditTime: 2024-12-30 16:17:07
'''
#!/usr/bin/python3.9
# -*- coding:utf-8 -*- 

import sys
from lxml import etree
import sqlite3
import unicodecsv as ucsv

host=''
result_list=[] 

# 通过颜色判断漏洞等级
def htm_parse(l):
    html_str = etree.tostring(l).decode('utf-8')    #字节解码为字符串     
    if '#91243E' in html_str:
        info=u"严重 - "+l.text
    elif '#DD4B50' in html_str:
        info=u"高危 - "+l.text
    elif '#F18C43' in html_str:
        info=u"中危 - "+l.text
    elif '#F8C851' in html_str:
        info=u"低危 - "+l.text           
    elif '#67ACE1' in html_str:
        info=u'信息泄露 - '+l.text
    else:
        info='Parsing error,Check that the versions are consistent.'
    return info

# 解析html文件
def main(filename):
    global host
    html = etree.parse(filename, etree.HTMLParser())
    ls = html.xpath('/html/body/div[1]/div[3]/div')
    for i in ls:
        # 获取主机IP地址
        if "font-size: 22px; font-weight: 700; padding: 10px 0; overflow-wrap: break-word" in etree.tostring(i).decode('utf-8'):
            host = i.text
        elif "this.style.cursor" in etree.tostring(i).decode('utf-8'):
            result = host + " - " + htm_parse(i)
            print(result)
            result_list.append(result)
    return result_list 
	
# 查询数据库
def select(ip,id):
    conn = sqlite3.connect('vuln.db')
    conn.text_factory = lambda x: str(x, 'gbk', 'ignore')
    cursor = conn.cursor()
    for row in cursor.execute("select * from VULNDB where Plugin_ID=?", (id,)):
        return [ip, row[1], row[2], row[3], row[4]]
    conn.close()
		
# 写入csv文件
if __name__ == '__main__':
    filename = sys.argv[1]
    list_host = main(filename)
	#list_host=[u'192.168.98.254 - 高危 - 10203 - rexecd Service Detection',u'192.168.98.254 - 高危 - 11233 - rexecd Service Detection']
	
    new_filename = filename + '.csv'
    with open(new_filename, 'wb') as f:
        w = ucsv.writer(f, encoding = 'gbk')
        title=[u'服务器IP',u'漏洞名称',u'风险级别',u'漏洞描述',u'修复建议']
        w.writerow(title)
        
        for i in list_host:
            info = i.split('-',3)
            result = select(info[0],info[2])
            if result is not None:
                data = result
            else:
                data = info[0],info[3],info[1]
            w.writerow(data)