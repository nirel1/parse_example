import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

criminal_list = open("criminals.json")
doc = criminal_list.read()

es.index(index='list1', ignore=400,  id=0, body=json.loads(doc))

res = es.get(index="list1", id=0)
print(res['_source'])

es.indices.refresh(index="list1")

res = es.search(index="list1", body={"lastname": {"KURBANOVA": {}}, "firstname": {"ATIKAT": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])