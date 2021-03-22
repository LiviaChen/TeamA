from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from elasticsearch import Elasticsearch
import urllib.parse

# Create your views here.
def hello(request):
    curr_stock = request.GET.get("curr_stock")
    if curr_stock != None :
        curr_stock = urllib.parse.unquote(curr_stock)
    else :
        curr_stock = '葡萄王 (1707)'
    return render(request, 'index.html', {
        'data1': ['中　化 (1701)', '葡萄王 (1707)', '生　達 (1720)', '美吾華 (1731)', '五　鼎 (1733', '杏　輝 (1734)', '喬　山 (1736)',
                  '中化生 (1762)', '和康生 (1783)', '科　妍 (1786)', '神　隆 (1789)', '景　岳 (3164)', '永　信 (3705)', '佳　醫 (4104)', '雃　博 (4106)', '懷　特 (4108)', '旭　富 (4119)', '亞諾法 (4133)', '麗豐-KY (4137)', '龍燈-KY (4141)', '國光生 (4142)', '承業醫 (4164)', '佐登-KY (4190)', '華　廣 (4737)', '台　耀 (4746)'],
        'data2': ['萬　企 (2701)','華　園 (2702)','國　賓 (2704)','六　福 (2705)','第一店 (2706)', '晶　華 (2707)', '美食-KY (2723)', '王　品 (2727)', '雄　獅 (2731)', '鳳　凰 (5706)', '新天地 (8940)', '好樂迪 (9943)'],
        'curr_stock' : curr_stock,
    })

def queryEsTest(request):
    query_str = request.GET.get("queryStr")
    es = Elasticsearch(hosts='https://search-teb103es-2tfxz65sltgjodqg25agsynztm.us-east-2.es.amazonaws.com/',
                       http_auth=('David', 'David_830414'))
    res = es.search(index="doc_index", body={"query": {"match": {'內容': str(query_str)}}})
    return JsonResponse(res['hits']['hits'], safe=False)