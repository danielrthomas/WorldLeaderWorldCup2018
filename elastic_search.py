# build_index.py

ES_HOST = {
    "host": "localhost",
    "port": 9200
}

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


from elasticsearch import Elasticsearch
from worldcupleadertweets import get_all_tweets

# response = urlopen(FILE_URL)
# csv_file_object = csv.reader (response)
#
# header = csv_file_object.next ()
# header = [item.lower () for item in header]
#
# bulk_data = []
#
# for row in csv_file_object:
#     data_dict = {}
#     for i in range (len (row)):
#         data_dict[header[i]] = row[i]
#     op_dict = {
#         "index": {
#             "_index": INDEX_NAME,
#             "_type": TYPE_NAME,
#             "_id": data_dict[ID_FIELD]
#         }
#     }
#     bulk_data.append (op_dict)

# create ES client, create index
es = Elasticsearch (hosts=[ES_HOST])

names = ["turnbullmalcolm", "theresa_may"]

for name in names:

    results = get_all_tweets(name, False, False, True)
    # print (results)

    INDEX_NAME = results[0]['index']['_index']
    TYPE_NAME = 'leaders'

    ID_FIELD = results[0]['index']['_id']



    if es.indices.exists (INDEX_NAME):
        print("deleting '%s' index..." % (INDEX_NAME))
        res = es.indices.delete (index=INDEX_NAME)
        print(" response: '%s'" % (res))

    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }

    print("creating '%s' index..." % (INDEX_NAME))
    res = es.indices.create (index=INDEX_NAME, body=request_body)
    print(" response: '%s'" % (res))

    # bulk index the data
    print("bulk indexing...")
    res = es.bulk (index=INDEX_NAME, body=results, refresh=True)
    # print(" response: '%s'" % (res))


    # sanity check
    print("searching...")
    res = es.search (index=INDEX_NAME, size=2, body={"query": {"match_all": {}}})
    print(" response: '%s'" % (res))

# print("results:")
# for hit in res['hits']['hits']:
#     print(hit["_source"])