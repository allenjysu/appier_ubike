#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib
import gzip
import json
import MySQLdb
from datetime import datetime


from ConfigParser import SafeConfigParser

config_file = '../config/config.ini'
config = SafeConfigParser(os.environ)
config.read(config_file)
db_host = config.get('mysql', 'host')
db_name = config.get('mysql', 'database')
user = config.get('mysql', 'user')
password = config.get('mysql', 'password')
conn = MySQLdb.connect(host=db_host, user=user, passwd=password, db=db_name)

url = config.get('ubike', 'url')
# print "downloading with urllib"
urllib.urlretrieve(url, "data.gz")
f = gzip.open('data.gz', 'r')
jdata = f.read()
f.close()
data = json.loads(jdata)
c = conn.cursor()
conn.set_character_set('utf8')

for key, value in data["retVal"].iteritems():
    sno = value["sno"]
    sna = value["sna"]
    tot = value["tot"]
    sbi = value["sbi"]
    sarea = value["sarea"]
    mday = value["mday"]
    lat = value["lat"]
    lng = value["lng"]
    ar = value["ar"]
    sareaen = value["sareaen"]
    snaen = value["snaen"]
    aren = value["aren"]
    bemp = value["bemp"]
    act = value["act"]

    sql = "INSERT INTO data(sno,tot,sbi,bemp,act,utime) VALUES(%s,%s,%s,%s,%s,%s)"
    del_sql = "DELETE FROM data where sno = \"%s\"" % sno
    try:

        c.execute(del_sql)
        c.execute(sql, (sno, tot, sbi, bemp, act, datetime.now()))
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        pass

    # print "NO." + sno + " " + sna

conn.close()
