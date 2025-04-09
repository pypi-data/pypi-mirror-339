# Import Elasticsearch package
from elasticsearch import Elasticsearch

# Connect to the elastic cluster
es = Elasticsearch("http://140.210.91.95:9200", basic_auth=("elastic", "bonc_test"))


def update_title_by_id(id, title):
    body = {
        "script": {
            "source": "ctx._source['infoTitle']='{}'".format(title)
        },
        "query": {
            "match": {
                "infoId": id
            }
        }
    }
    return es.index("bid_keywords").update_by_query(body=body)
