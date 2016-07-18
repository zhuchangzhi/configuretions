# -*- coding:utf-8 -*-  
import csv
import urllib2
import json
import time
import traceback
import logging
import MySQLdb
data=[]
try:
    db=MySQLdb.connect(host='rdsqdb52n6058wp07g7o.mysql.rds.aliyuncs.com', user='ip_data', passwd='YB60HEDDbL6v2HgCO6GK',db="ip_data", port=3306,charset='UTF8')
    cur=db.cursor()
except Exception,e:
    logging.error(e)
    exit()
query_select_noupdated='SELECT startip FROM `cn_ipv4_zh` WHERE ver IS NULL order by startip desc'
try:
    cur.execute(query_select_noupdated)
    noupdated_IPs=cur.fetchall()
except Exception,e:
    logging.error(e)
    exit()
for i in noupdated_IPs:
    params=i
    req=urllib2.Request("http://ip.taobao.com/service/getIpInfo.php?ip=%s" % params)
    try:
        result=urllib2.urlopen(req)
    except Exception,e:
        logging.error(req.get_full_url())
        logging.error(e)
        continue
    r_json=json.loads(result.read())
    if not (r_json['code']):
        query_update='update `cn_ipv4_zh` set testedIP=%s,city=%s,area_id=%s,region_id=%s,area=%s,city_id=%s,country=%s,region=%s,isp=%s,country_id=%s,county=%s,isp_id=%s,county_id=%s,ver=%s where startIP=%s'
        for key in r_json['data']:
            if not (r_json['data'][key]):
                r_json['data'][key]='-'
        try:
            cur.execute(query_update,(r_json['data']['ip'],r_json['data']['city'].encode('utf8'),r_json['data']['area_id'],r_json['data']['region_id'],r_json['data']['area'].encode('utf8'),r_json['data']['city_id'],r_json['data']['country'].encode('utf8'),r_json['data']['region'].encode('utf8'),r_json['data']['isp'].encode('utf8'),r_json['data']['country_id'],r_json['data']['county'].encode('utf8'),r_json['data']['isp_id'],r_json['data']['county_id'],2,i))
            db.commit()
            logging.error('updated')
        except Exception,e:
            logging.error(e)
            continue
    else:
        logging.error('query from ip.taobao.com return error')
        logging.error(r_json['code'])
        continue
    time.sleep(0.6)
db.close()