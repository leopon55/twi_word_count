import requests
import os
import json
import pandas as pd
from pandas.io.json import json_normalize
import time

with open("twittertoken.txt") as f:
    bearer_token = f.read()
search_url = "https://api.twitter.com/2/tweets/counts/all"

# keywords = [
#         "キーワード1",
#         "キーワード2"
#         ]
years = ["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"] 
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]

def decide_params(ey,em,kw):
    # startt = sy + "-" + sm + "-01T00:00:00Z"
    endt = ey + "-" + em + "-01T00:00:00Z"
    # Optional params: start_time,end_time,since_id,until_id,next_token,granularity
    # query_params = {'query': keyword,'granularity': 'day', 'start_time': startt,"end_time": endt}
    query_params = {'query': kw,'granularity': 'day', "end_time": endt}
    return query_params


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveTweetCountsPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        if response.status_code == 420 or response.status_code == 429:
            time.sleep(900)
            connect_to_endpoint(url,params)
        raise Exception(response.status_code, response.text)
    else:
        print("    通信正常")
    return response.json()


def responses_to_pandas(response):
    # df_json = pd.read_json(json_response, orient ='index')

    # 文字列に変換してから、辞書として読み込み
    info = json.loads(json.dumps(response))
    df = json_normalize(info['data'])
    return(df)

def each_to_all(dfe, dfa):
    return(pd.concat([dfa,dfe],join="inner"))

def pandas_to_csv(df,kw):
    df.to_csv("./data/" + kw + "onTwitter"+".csv",
        index=False)
    print(kw + "done")
    print("\n==================================\n")

def get_kw():
    f = open('keywords.txt', 'r',encoding="utf-8")
    keywords = f.readlines()
    print(keywords)
    return(keywords)


def main():
    keywords = get_kw()

    for keyword in keywords:
        a = 1
        try: #readlinesの弊害
            keyword = keyword.replace('\n','')
        except:
            pass

        for year in years:
            for month in months:
                if year=="2006" and (month=="01" or month=="02" or month=="03"):
                    pass
                else:
                    print("loading: " + keyword + year + month)
                    query_params  = decide_params(year,month,keyword)
                    json_response = connect_to_endpoint(search_url, query_params)
                    time.sleep(4.6)#4.5秒以上開ければok(API取得制限)
                    df_each = responses_to_pandas(json_response)
                    
                    print("    count_ave: " + str(df_each['tweet_count'].mean()))
                    # print(json.dumps(json_response, indent=4, sort_keys=True))

                    if a == 1:
                        df_all = df_each
                        a += 1
                    else:
                        df_all = each_to_all(df_each, df_all)

        pandas_to_csv(df_all,keyword)
        time.sleep(3)

if __name__ == "__main__":
    main()

# cf https://github.com/twitterdev/Twitter-API-v2-sample-code
