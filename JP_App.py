# encoding=utf-8
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import time

header = {'accept': 'application/json',
          'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'zh-CN,zh;q=0.9,de;q=0.8,en;q=0.7,zh-TW;q=0.6',
          'authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNSRjVITkJHUFEifQ.eyJpc3MiOiI4Q1UyNk1LTFM0IiwiaWF0IjoxNjA1NzQ4OTAwLCJleHAiOjE2MDg3NzI5MDB9.XseaOPnz6ms91grA71stRdHeepZMPbMU-AceqiAIetTivPr8sBQTV9Y1TG1GlAq1BOjbPFWk51rdm3CgxLmalg'
    , 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'origin': 'https://apps.apple.com',
          'referer': 'https://apps.apple.com/jp/app/uber-eats-%E3%82%A6%E3%83%BC%E3%83%90%E3%83%BC%E3%82%A4%E3%83%BC%E3%83%84-%E5%87%BA%E5%89%8D-%E3%83%87%E3%83%AA%E3%83%90%E3%83%AA%E3%83%BC%E6%B3%A8%E6%96%87/id1058959277',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-site',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
          }

def read_pageHtml(url):  # 获取网页源代码
    htmlr = requests.get(url, headers=header)
    bsObjHtml = BeautifulSoup(htmlr.text, features="html.parser")
    return bsObjHtml


if __name__ == "__main__":
    review_set = pd.DataFrame(columns=['date', 'rating', 'review'])
    data_count = {'2020': 0, '2019': 0, '2018': 0, '2017': 0, '2016': 0}
    for i in range(10,7780, 10):
        '''if i > 10000:
            i = i + 30000'''
        url = 'https://amp-api.apps.apple.com/v1/catalog/jp/apps/1058959277/reviews?l=ja&offset=' + str(
            i) + '&platform=web&additionalPlatforms=appletv%2Cipad%2Ciphone%2Cmac'
        page = read_pageHtml(url)
        try:
            page_dict = json.loads(page.text)
        except:
            continue
        if 'message' in page_dict.keys():
            time.sleep(10)
            continue
        if 'errors' in page_dict.keys():
            print(page_dict['errors'])
            continue
        for j in range(len(page_dict['data'])):
            date = page_dict['data'][j]['attributes']['date'][0:4]
            '''if data_count[date] >= 1500:
                continue
            else:'''
            data_count[date] = data_count[date] + 1
            rating = page_dict['data'][j]['attributes']['rating']
            title = page_dict['data'][j]['attributes']['title']
            review = title + page_dict['data'][j]['attributes']['review']
            review_set.loc[i * 10 + j] = [date, rating, review]
        print('\r{0}条数据已找到'.format(sum(data_count.values())), data_count, i, end='')
        '''if sum(data_count.values()) == 7500:
            break'''
    review_set.to_csv('JP-APP-7500.csv', index=0, encoding='utf_8_sig')
    print(review_set.head())
