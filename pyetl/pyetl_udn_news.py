import requests
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

# 以下程式碼會先將所有新聞文章網址爬下來
# url_1 = 'https://udn.com/search/word/2/%E6%96%B0%E5%86%A0%E8%82%BA%E7%82%8E' # 新冠肺炎

print(datetime.now())

total_links = []

for i in range(75, 5375):
    # start with page 75, since the previous pages is all on 2021, end by 5375
    url = f'https://udn.com/api/more?page={i}&id=search:%E6%96%B0%E5%86%A0%E8%82%BA%E7%82%8E&channelId=2&type=searchword&last_page=5374'
    print(url)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    json_str = json.loads(res.text)

    for i in range(0, len(json_str['lists'])):
        date = json_str['lists'][i]['time']['dateTime']
        date_formatter = "%Y-%m-%d %H:%M:%S"
        if (datetime.strptime(date, date_formatter) > datetime.strptime('2019-11-01', '%Y-%m-%d')) and \
                (datetime.strptime(date, date_formatter) < datetime.strptime('2021-01-01', '%Y-%m-%d')):
            if (json_str['lists'][i]['titleLink']) not in total_links:  # to connect original list after error happened
                total_links.append(json_str['lists'][i]['titleLink'])
    sleep_time = random.randint(6, 10)
    time.sleep(sleep_time)

print(datetime.now())

column = ['link']
df = pd.DataFrame(data = total_links, columns = column)
df.to_csv(r'./links.csv', index=0, encoding='utf-8-sig', header=None)


# 以下程式碼會將每個新聞網址裡所需的內容取出
total_links =[]

with open(r'./links.csv', 'r', encoding = 'utf-8-sig') as single_list :
    for each_line in single_list.readlines() :
        total_links.append(each_line.replace('\n', ''))

total_list = []

for i in total_links :
    headers = {'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7', 'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

    res = requests.get(i, headers=headers)
    soup = BeautifulSoup(res.text)
    single_list = []
    single_list.append('新冠肺炎')
    try :
        single_list.append(soup.select_one('time[class="article-content__time"]').text)
        single_list.append(i)
        single_list.append(soup.select_one('h1[class="article-content__title"]').text)
        single_list.append(soup.select_one('div[class="article-content__paragraph"]').text.replace('\n','').replace('\r','').replace(' 跨年疫情新冠肺炎',''))
        total_list.append(single_list)
    except AttributeError :
        try :
            single_list.append(re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}',soup.select_one('h1[class="story_art_title"]').text).group())
            single_list.append(i)
            single_list.append(soup.select_one('h1[class="story_art_title"]').text.split('分享')[0])
            content = ''
            for i in soup.select('p'):
                content += i.text
            single_list.append(content)
            total_list.append(single_list)
        except Exception as e :
            print(e)
    time_sleep = random.randint(6,10)
    time.sleep(time_sleep)

columns = ['Key Word', 'Time', 'Website', 'News Article', 'Content']
df = pd.DataFrame(data = total_list, columns = columns)
df.to_csv(r'./content.csv', index=0, encoding='utf-8-sig', header=None)