import requests
import json
import pandas as pd
from elasticsearch import Elasticsearch

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
# }
# req = requests.post('http://localhost:9200/testindex/testtype/5',data=json.loads(testdata),headers=headers)
# print(req.text)

es = Elasticsearch(hosts='localhost', port='9200')
df = pd.read_csv('doc/news.csv')
doc_dict = df.to_dict('records')

count = 0
for doc in doc_dict[:5]:
    res = es.index(index="doc_index", id=count, body=doc)
    print(res['result'])
    count += 1