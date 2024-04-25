import time
import requests
import csv
import os
from datetime import datetime

def init():
    if not os.path.exists('./articleComments.csv'):
        with open('./articleComments.csv','w',encoding='utf-8',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'articleId',
                'created_at',
                'likes_counts',
                'region',
                'content',
                'authorName',
                'authorGender',
                'authorAddress',
                'authorAvatar'
            ])

def writerRow(row):
    with open('./articleComments.csv', 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

def get_data(url,params):
    headers = {
        'Cookie': "SINAGLOBAL=4784814304210.35.1708950523299; UOR=,,cn.bing.com; ULV=1710885149638:3:2:2:9477896080440.691.1710885149624:1710860919465; PC_TOKEN=9fac55dd7b; ALF=1715241469; SUB=_2A25LEIStDeRhGeBO6FUW8S7PzjuIHXVob5hlrDV8PUJbkNANLVHtkW1NSh8f5HEA8nuJDWn7R859lKt1RzusWfuX; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Eh-1zR9E8Y.1AaKfwgV.u5JpX5KzhUgL.Foq7e0MNeK50SKM2dJLoI7fi-JH_9giLMo-XeoM7",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return None

def getAllArticleList():
    artileList = []
    with open('./articleData.csv','r',encoding='utf-8') as reader:
        readerCsv = csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            artileList.append(nav)
    return artileList

def parse_json(response,artileId):
    for comment in response:
        created_at = datetime.strptime(comment['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        likes_counts = comment['like_counts']
        try:
            region = comment['source'].replace('来自', '')
        except:
            region = '无'
        content = comment['text_raw']
        authorName = comment['user']['screen_name']
        authorGender = comment['user']['gender']
        authorAddress = comment['user']['location']
        authorAvatar = comment['user']['avatar_large']
        writerRow([
            artileId,
            created_at,
            likes_counts,
            region,
            content,
            authorName,
            authorGender,
            authorAddress,
            authorAvatar
        ])

def start():
    commentUrl = 'https://weibo.com/ajax/statuses/buildComments'
    init()
    articleList = getAllArticleList()
    for article in articleList:
        articleId = article[0]
        print('正在爬取id值为%s的文章评论' % articleId)
        time.sleep(1)
        params = {
            'id':int(articleId),
            'is_show_bulletin':2
        }
        response = get_data(commentUrl,params)
        parse_json(response,articleId)



if __name__ == '__main__':
    start()








