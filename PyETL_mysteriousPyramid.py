import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import random

stock_name_type = {}
stock_link = []

for p in list(range(1,7)) + list(range(8,13)) + list(range(14,19)) + list(range(20,32)) : # create page loop

    headers = {'User-Agent': 'put_user_agent_here'}
    url = f'https://norway.twsthr.info/StockHoldersTopWeek.aspx?CID={p}&Show=1'
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text)
    stock_info = soup.select('td[style="text-decoration: underline"]') # decide selecting label

    for i in stock_info : # loop到爬下來的bs4.element.ResultSet物件中
        if stock_info.index(i) % 2 == 0 : # 單數項是股數類別，雙數的是股票名稱
            stock_name_type[i.text] = stock_info[stock_info.index(i)+1].text
            stock_link.append('https://norway.twsthr.info/' + i.a['href'].split('/')[1])
    print(stock_link)
    sleep_time = random.randint(6, 10)
    time.sleep(sleep_time)

total_entry = []
a = time.time() # count the starting time
for i in stock_link_p31 :
    url = i
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text)
    each_stock_name = soup.select_one('p[style="font-size:21px"]').text.replace(' ','')
    data_weekly_one = soup.select('tr[class="lDS"]')
    data_weekly_two = soup.select('tr[class="lLS"]')
    for j in (data_weekly_one + data_weekly_two) :
        single_entry = []
        single_entry.append(each_stock_name)
        single_entry.append(stock_name_type_p31[each_stock_name])
        if j.select('td')[2].text.replace('\xa0', '').isdigit() :
            for k in range(2, 15) :
                single_entry.append(j.select('td')[k].text.replace('\xa0', ''))
            total_entry.append(single_entry)
        else :
            continue
    total_entry = sorted(total_entry)
    sleep_time = random.randint(10, 15)
    time.sleep(sleep_time)
b = time.time() # count the ending time, can do further b-a to get the duration

columns = ['股票名稱', '股票類別',
 '資料日期',
 '集保總張數',
 '總股東人數',
 '平均張數/人',
 '>400張大股東持有張數',
 '>400張大股東持有百分比',
 '>400張大股東人數',
 '400~600張人數',
 '600~800張人數',
 '800~1000張人數',
 '>1000張人數',
 '>1000張大股東持有百分比',
 '收盤價']

df = pd.DataFrame(data=total_entry, columns = columns)
print(df)

df.to_csv(r'./total_entry.csv', index=0, encoding='utf-8-sig')
