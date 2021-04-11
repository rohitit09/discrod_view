from elasticsearch import Elasticsearch,exceptions
es = Elasticsearch()

def insert(doc):
    for i in doc:
        res = es.index(index="user_history", body=i)
        print(res['result'])


def get_data(query,id):
    q={
        "query" : {
            "bool" : {
                "must" : [
                        {
                            "query_string" : {
                                "query" : "*"+query+"*",
                                "fields" : ["title"]
                            }
                        },{
                            "query_string" : {
                                "query" :    id,
                                "fields" : ["author_id"]
                            }
                        }
                ]
            }
        }
    }
    try:
        res = es.search(index="user_history",body=q)
        res=res['hits']['hits'][:6]
        if len(res)>0:
            res=[i['_source']['link'] for i in res]
            res='\n'.join(res)
        return res
    except exceptions.NotFoundError as e:
       return "No recent hostory present"
