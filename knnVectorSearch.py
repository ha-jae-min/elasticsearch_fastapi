from elasticsearch import Elasticsearch
from getEmbedding import get_embedding

es = Elasticsearch("http://localhost:9200")

def knn_search(index_name, query_text):
    embedding = get_embedding(query_text).tolist()  # 쿼리를 벡터로 변환
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": embedding}
                }
            }
        }
    }
    return es.search(index=index_name, body=query)
