# -*- coding:utf-8 -*-  
import csv
import urllib2
import json
import time
import traceback
import logging
import MySQLdb
csv_file=open('D:\downFromCRT\dbip_cn_ipv4-all.csv','r')
reader=csv.reader(csv_file)
data=[]
for c1,c2,c3,c4,c5 in reader:
    ip=[c1,c2]
    data.append(ip)
csv_file.close()
range_start=0
range_end=10
if (range_end > len(data)):
    range_end=len(data)
dataset=[]
for i in range(range_start,len(data)):
    if  not (i%10000) and i!=0:
        sql='insert into cn_ipv4_zh (startIP,endip) values (%s,%s)'
        db=MySQLdb.connect(host='rdsqdb52n6058wp07g7o.mysql.rds.aliyuncs.com', user='ip_data', passwd='YB60HEDDbL6v2HgCO6GK',db="ip_data", port=3306)
        cur=db.cursor()
        cur.executemany(sql,dataset)
        db.commit()
        db.close()
        dataset=[]
    dataset.append(data[i])
sql='insert into cn_ipv4_zh (startIP,endip) values (%s,%s)'
db=MySQLdb.connect(host='rdsqdb52n6058wp07g7o.mysql.rds.aliyuncs.com', user='ip_data', passwd='YB60HEDDbL6v2HgCO6GK',db="ip_data", port=3306)
cur=db.cursor()
cur.executemany(sql,dataset)
db.commit()
db.close()