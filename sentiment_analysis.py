#!/usr/bin/env python
# coding: utf-8

# # 商品評論-情感分析 sentiment analysis

# pip install pandas

import pandas as pd
from textblob import TextBlob
import os
import statistics

df = pd.read_csv('./amzon_ETL_20201218.csv')  # 讀取商品清單20個
itemlist = df['Description'].tolist()  # 將商品放進list中，方便將空白取代'_'

itemlistt = []  # 空list，將更新後的20個商品放入
for x in itemlist:
    x = x.replace(' ', '_')
    #     print(x) #type=str
    itemlistt.append(x)

web = ['amazon_reviews', 'target_reviews', 'wegmans_reviews']
for j in web:
    total_score = []
    items = []
    for i in itemlistt:  # 商品清單
        path = "./" + j + '/' + i + '.txt'  # 每個商品評論之檔名
        print(path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reviews = f.readlines()  # 讀取每條評論

            new_reviews = []
            for rev in reviews:
                rev = rev.replace('-', '').replace('\n', '').strip()
                if rev != '':
                    new_reviews.append(rev)
                else:
                    pass
            score = []
            for word in new_reviews:
                blob = TextBlob(word)
                a = blob.sentiment
                score.append(a[0])  # 每段文字的評分list
            reviews_score = round(statistics.mean(score) * 100, 2)  # 該商品所有評論分數的平均數*100，取小數2位
            print(reviews_score)
        except FileNotFoundError as fnf:
            print(fnf)
            pass
        except ValueError as valerr:
            print(valerr)
            pass
        print('---' + i + '---')
        total_score.append(reviews_score)
        items.append(i)
    data = {'Item': items, 'Score': total_score}
    new_df = pd.DataFrame(columns=['Item', 'Score'], data=data)
    print(new_df)
    save_path = './' + j + '_score.csv'   #以各別網站區分為檔名
    new_df.to_csv(save_path, index=False)
