# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2021/08/24 19:00
# @author  : Lindeci
# @function: post service of fastapi
 
from pydantic import BaseModel
from fastapi import FastAPI,Query
from fastapi.responses import RedirectResponse
import re

import redis

import mysql.connector
import mysql.connector.pooling
from threading import Semaphore
from contextlib import contextmanager
import time
from concurrent.futures import ThreadPoolExecutor

import base_62_converter

MY_URL = "http://159.75.208.85:8080"
APP_HOST = "0.0.0.0"
APP_PORT = 8080
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

mysql_config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'port': '3306',
  'database': 'bit_ly',
  'charset': 'utf8',
  'raise_on_warnings': True
}

app = FastAPI()

redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
rs = redis.Redis(connection_pool=redis_pool)

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mysql_pool",
                                                      pool_size = 30,
                                                      **mysql_config,
                                                      connection_timeout=5)

cnx = cnxpool.get_connection()
cursor = cnx.cursor()
sql ="select ifnull(max(id),0) lastrowid from t_short_url"
cursor.execute(sql)
[(lastrowid,)] = cursor.fetchall()
cursor.close()
cnx.close()

def get_from_mysql_url_long(url: str):
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        sql ="select id,url_short from t_short_url where url_long = '" + url + "'"
        cursor.execute(sql)
        data = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()
    return data

def get_from_mysql_id(id: int):
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        sql ="select url_long from t_short_url where id = " + str(id)
        cursor.execute(sql)
        data = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()
    return data
        
def store_url_mysql(id:int, url: str, shortUrl:str):
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        sql ="insert into t_short_url(id,url_long,url_short) value(" + str(id) + ",'" + url + "','" + shortUrl + "')"
        print(sql)
        cursor.execute(sql)
        cnx.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

class Item(BaseModel):
    url: str = None
 
@app.post('/newurl')
async def newurl(request_data: Item):
    global lastrowid
    shortenUrl = rs.get("URL:" + request_data.url)
    if shortenUrl:
        res = {"url":request_data.url,"shortenUrl":shortenUrl}
    else:
        data = get_from_mysql_url_long(request_data.url)
        if data:
            [(id,url_short)] = data
            rs.set("URL:" + request_data.url,str(id) + ':' + url_short)
            res = {"url":request_data.url,"shortenUrl":url_short}
        else:
            id = lastrowid + 1
            shortenUrl = base_62_converter.int_to_string(id)
            store_url_mysql(id, request_data.url, shortenUrl)
            rs.set("URL:" + request_data.url, str(id) + ":" + shortenUrl)
            rs.set("shortenUrl:"+shortenUrl,str(id) + ":" + request_data.url)
            lastrowid = id
            res = {"url":request_data.url,"shortenUrl":shortenUrl}
    return res
        

@app.get('/{shortenUrl}')
async def redirect(shortenUrl: str):
    print(shortenUrl)
    matchObj = re.match( r'(^([a-zA-Z0-9]{9}))$', shortenUrl, re.M|re.I)
    if not matchObj:
        res = {"error":shortenUrl + " does not match [a-zA-Z0-9]{9}."}
        return res
    value = rs.get("shortenUrl:" + shortenUrl)
    print(value)
    if value:
        print(value)
        value = str(value, encoding = "utf-8")
        [id,url] = value.split(':',1)
        print("test1",url)
        return RedirectResponse("http://"+url, status_code = 302)
    else:
        id = base_62_converter.string_to_int(shortenUrl)
        data = get_from_mysql_id(id)
        print(data)
        if data:
            [(url,)] = data
            print(url)
            rs.set("URL:" + url, str(id) + ":" + shortenUrl)
            rs.set("shortenUrl:"+shortenUrl,str(id) + ":" + url)
            return RedirectResponse(url, status_code=302)
        else:
            res = {"error":shortenUrl + " has not been generated, pls newurl it."}
            return res

 
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app,
                host=APP_HOST,
                port=APP_PORT,
                workers=1)
