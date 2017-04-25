# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
from apt.package import Record
sys.path.append("..")

import os
import json
import MySQLdb
import math
from ConfigParser import SafeConfigParser

config_file = '../config/config.ini'
config = SafeConfigParser(os.environ)
config.read(config_file)
db_host = config.get('mysql', 'host')
db_name = config.get('mysql', 'database')
user = config.get('mysql', 'user')
password = config.get('mysql', 'password')
conn = MySQLdb.connect(host=db_host, user=user, passwd=password, db=db_name)
conn.set_character_set('utf8')


def ubike_check(json_data):
    # print "sample_create:",json_data
    body = {}
    aryStation = []
    sql = "select info.sno ,sna , lat, lng , power( power (lat-%s,2) + power(lng-%s,2), 1.0/2) as dis , data.sbi as sbi, sna from info inner join data on data.sno = info.sno order by dis asc limit 3" % (
        json_data["lat"], json_data["lng"])
    c = conn.cursor()
    c.execute(sql)
    data = c.fetchall()
    radius = triangleCircle(data)
    for record in data:
        station = record[6]
        b = {
            #"sno" : record[0],
            "station": station,
            "num_ubike": record[5]
            #"sna" : record[1],
            #"lat" : record[2],
            #"lng" : record[3],
            #"dit" : record[4]
        }
        aryStation.append(b)

    body["station"] = aryStation
    body["radius"] = radius
    body["taipei"] = is_inTaipei(radius, data)
    body["full"] = is_full(json_data)

    return body


def is_inTaipei(radius, data):
    if data[0][4] - radius > 0.0 and data[1][4] - radius > 0.0 and data[2][4] - radius > 0.0:
        return False
    else:
        return True


def is_full(json_data):
    sql = "select count(sno) as count from data where tot != sbi"
    c = conn.cursor()
    c.execute(sql)
    data = c.fetchall()
    return data[0][0]


def triangleCircle(data):
    x0 = float(data[0][2])
    y0 = float(data[0][3])
    x1 = float(data[1][2])
    y1 = float(data[1][3])
    x2 = float(data[2][2])
    y2 = float(data[2][3])
    a = math.sqrt(math.pow(x0 - x1, 2) + math.pow(y0 - y1, 2))
    b = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    c = math.sqrt(math.pow(x2 - x0, 2) + math.pow(y2 - y0, 2))

    p = (a + b + c) / 2
    S = math.sqrt(p * (p - a) * (p - b) * (p - c))
    radius = a * b * c / (4 * S)
    return radius
