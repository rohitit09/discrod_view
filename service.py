from elasticsearch import Elasticsearch,exceptions
es = Elasticsearch()

def insert(doc):
    '''
    this function is used to store serach data of a particular user
    params:
        doc: array of dictionary contains data generated from google search of a particular user.
    '''
    for i in doc:
        res = es.index(index="user_history", body=i)
        print(res['result'])


def get_data(query,id):
    '''
    this function is used to get the hostorical serach data of a particular user
    params:
        query: string to be serached for
        id: user id
    '''
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
        res = es.search(index="user_history",body=q) # searching in elastic seach
        res=res['hits']['hits'][:6] # only fetching first 6 record
        if len(res)>0:
            res=[i['_source']['link'] for i in res]
            res='\n'.join(res)
        return res
    except exceptions.NotFoundError as e:
       return "No recent hostory present"
