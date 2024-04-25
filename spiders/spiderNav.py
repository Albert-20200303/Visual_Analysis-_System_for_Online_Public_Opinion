import requests
import csv
import numpy as np
import os

def init():
    if not os.path.exists('./navData.csv'):
        with open('./navData.csv','w',encoding='utf-8',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'typeName',
                'gid',
                'containerid'
            ])

def writerRow(row):
    with open('./navData.csv', 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

#爬取微博文本
def get_data(url):
    headers = {
        'Cookie': "SINAGLOBAL=4784814304210.35.1708950523299; UOR=,,cn.bing.com; ULV=1710885149638:3:2:2:9477896080440.691.1710885149624:1710860919465; PC_TOKEN=9fac55dd7b; ALF=1715241469; SUB=_2A25LEIStDeRhGeBO6FUW8S7PzjuIHXVob5hlrDV8PUJbkNANLVHtkW1NSh8f5HEA8nuJDWn7R859lKt1RzusWfuX; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Eh-1zR9E8Y.1AaKfwgV.u5JpX5KzhUgL.Foq7e0MNeK50SKM2dJLoI7fi-JH_9giLMo-XeoM7",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    params = {
        'is_new_segment':1,
        'fetch_hot':1
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response):
    navList = np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    for nav in navList:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        writerRow([
            navName,
            gid,
            containerid
        ])


if __name__ == '__main__':
    init()
    print("main")
    url = 'https://weibo.com/ajax/feed/allGroups'
    response = get_data(url)
    parse_json(response)