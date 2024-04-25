from utils.getPublicData import getAllCommentsData,getAllArticleData
from datetime import datetime
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw
commentsList = getAllCommentsData()
articleList = getAllArticleData()

def getHomeTagsData():
    # 文章个数
    articleLenMax = len(articleList)
    # 最高点赞微博-作者
    likeCountMax = 0
    likeCountMaxAuthorName = ''
    # 最多城市
    cityDic = {}
    for article in articleList:
        if likeCountMax < int(article[1]):
            likeCountMax = int(article[1])
            likeCountMaxAuthorName = article[11]
        if article[4] != '无':
            if cityDic.get(article[4], -1) == -1:
                cityDic[article[4]] = 1
            else:
                cityDic[article[4]] += 1
    cityDicSorted = list(sorted(cityDic.items(),key=lambda x:x[1],reverse=True))
    return articleLenMax,likeCountMaxAuthorName,cityDicSorted[0][0]

def getHomeCommentsLikeCountTopFore():
    return list(sorted(commentsList,key=lambda x:int(x[2]),reverse=True))[:4]

def getHomeArticleCreatedAtChart():
    xData = list(set([x[7] for x in articleList]))
    xData = list(sorted(xData,key=lambda x:datetime.strptime(x,'%Y-%m-%d').timestamp(),reverse=True))
    yData = [0 for x in range(len(xData))]
    for article in articleList:
        for index,j in enumerate(xData):
            if article[7] == j:
                yData[index] += 1
    return xData,yData

def getHomeTypeChart():
    typeDic = {}
    for article in articleList:
        if typeDic.get(article[8],-1) == -1:
            typeDic[article[8]] = 1
        else:
            typeDic[article[8]] += 1
    resultData = []
    for key,value in typeDic.items():
        resultData.append({
            'name':key,
            'value':value
        })
    return resultData

def getHomeCommentCreatedChart():
    createAtDic = {}
    for comment in commentsList:
        if createAtDic.get(comment[1], -1) == -1:
            createAtDic[comment[1]] = 1
        else:
            createAtDic[comment[1]] += 1
    resultData = []
    for key, value in createAtDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData

def stopWordList():
    return [line.strip() for line in open('./model/stopWords.txt',encoding='utf8').readlines()]

def getUserNameWordCloud():
    text = ''
    stopWords = stopWordList()
    for comment in commentsList:
        text += comment[5]
    cut = jieba.cut(text)
    newCut = []
    for word in cut:
        if word not in stopWords:newCut.append(word)
    string = ' '.join(newCut)
    wc = WordCloud(
        width=1000,
        height=600,
        background_color='#fff',
        colormap='Blues',
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig('./static/authorNameCloud.jpg',dpi=500)

