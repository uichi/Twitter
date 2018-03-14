# -*- coding:utf-8 -*-
import tweepy
import pandas as pd
import time
import os
import csv
from oauth_key import *

class GetTweetData:
    
    def __init__(self, genre, repeats, items):
        self.genre   = genre
        self.repeats = repeats
        self.items   = items
            
    def collect(self):
        if not os.path.isdir('tweets/' + self.genre + '_tweets'):
            os.mkdir('tweets/' + self.genre + '_tweets')
            
        for repeat in range(self.repeats):
            print(str(repeat+1) + "週目です。")
            for item_number in range(len(self.items)):
                search_word = self.items['search_word'][item_number]
                print('検索後 : ', search_word)
                
                #ツイートファイルを作成するときの名前に使用
                tweet_file_name = self.items['item_name'][item_number]
                dir_name = tweet_file_name + '_tweets'
                if not os.path.isdir('tweets/' + self.genre + '_tweets' + '/' + dir_name):
                    os.mkdir('tweets/' + self.genre + '_tweets' + '/' + dir_name)
                    
                #認証キーは別ファイルをimportで持ってくる
                auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
                auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
                api = tweepy.API(auth)

                #ツイート格納変数
                tweet_list = []
                print('アクセス開始')
                start = time.time()
                day = time.strftime("%Y%m%d%H%M")
                
                def connect_api(search, counts):
                    global tweets
                    try:
                        tweets = api.search(q=search, count=counts, exclude="retweets")
                        return tweets
                    except:
                        print("tweepy.error.TweepError: 接続エラーです。")
                        print("1分ほどお待ちください。\n")
                        time.sleep(60)
                        self.connect_api(search=search, counts=counts)

                #1回アクセスした際に収集するツイート数
                param_counts = 10
                connect_api(search=search_word, counts=param_counts)
                for tweet in tweets:
                    tweet_list.append(tweet.text)
                    time.sleep(0.25)
                    
                elapsed_time = time.time() - start
                print("アクセスから" + str(elapsed_time) + "秒かかりました。\n")
                print("ファイルを作成します。\n")
                df = pd.DataFrame(tweet_list, columns=["tweets"])
                df.to_csv('tweets/' + self.genre + '_tweets/' + dir_name + "/" + tweet_file_name + day + ".csv", index=False, encoding='utf-8')
            print(str(repeat+1) + "周しました。")
            if self.repeats == repeat+1:
                break
            print("休憩だよ! 30分ほど待ってね!\n")
            time.sleep(60*29)
        print("終わったよ!")

tweet_genre = str(input('ジャンルを入力してください。: \n'))
repeat_collection  = int(input('何回繰り返しますか?\n'))
items = pd.read_csv('keyword/' + tweet_genre + '_keyword.csv', encoding='utf-8')

get_tweet_data = GetTweetData(genre=tweet_genre, repeats=repeat_collection, items=items)
get_tweet_data.collect()
