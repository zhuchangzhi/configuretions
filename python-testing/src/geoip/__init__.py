import csv
import urllib2
import json
import time
import traceback
import logging
csv_file=open('D:\downFromCRT\dbip_cn_ipv4.csv','r')
reader=csv.reader(csv_file)
data=[]
for c1,c2,c3,c4,c5 in reader:
    ip=[c1,c2]
    data.append(ip)
csv_file.close()
csv_write=open('D:\downFromCRT\dbip_cn_ipv4_zh.csv','wb')
writer=csv.writer(csv_write)
for i in range(0,len(data)):
    params=data[i][0]
    req=urllib2.Request("http://ip.taobao.com/service/getIpInfo.php?ip=%s" % params)
    try:
        result=urllib2.urlopen(req)
    except Exception,e:
        logging.error(req.get_full_url())
        logging.error(e)
        continue
    r_json=json.loads(result.read())
    if not (r_json['code']):
        if (r_json['data']['country_id'] != 'CN'):
            continue
        for key in r_json['data']:
            print ("%s,%s" %(key,r_json['data'][key]))
        for key in r_json['data']:
            if (r_json['data'][key]):
                try:
                    data[i].append(r_json['data'][key].encode('gb2312'))
                except Exception,e:
                    logging.error(r_json['data'][key])
                    logging.error(e)
                    continue
            else:
                data[i].append('0')
    else:
        print 'failed'
        pass
    writer.writerow(data[i])
    time.sleep(0.06)
#    print i,data[i][0]
csv_write.close()