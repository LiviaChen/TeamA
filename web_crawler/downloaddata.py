import requests
import time
import random
import os
import csv

# n=1
# m= "%02d"%n
# print(m)

date = list()
for y in range(2016,2021):
    for m in range(1,13):
        dates=str(y)+"%02d"%m+"01"
        date.append(dates)

start = time.time()

# with open("stockID.json",'r') as fp:
#     datalist = json.load(fp)

datalist = list()
with open("bmstockno.csv",newline='',encoding='utf-8') as fp:
    rows = csv.reader(fp)
    for row in rows:
        datalist.append(int(row[0]))


for sno in datalist:
    sno = str(sno)
    for d in date:
        # https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date=20201101&stockNo=2330 原網址
        url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date="+d+"&stockNo="+sno
        r = requests.get(url)
        path = "./stockData/"+sno
        if not os.path.isdir(path):  # 如果資料夾不存在就建立
            os.mkdir(path)

        time.sleep(random.randint(6,11))
        with open(path+"/"+sno+"_"+d+".csv", "wb") as f:
            f.write(r.content)
        f.close()
        print(sno+"_"+d+" done")

end = (time.time() - start)
print("Time used:", end)