from elasticsearch import Elasticsearch
from getEmbedding import get_embedding
from sklearn.metrics.pairwise import cosine_similarity

# es = Elasticsearch("http://10.10.10.54:9200")
es = Elasticsearch("http://localhost:9200")

def knn_search(index_name, query_text, threshold=0.7):
    query_embedding = get_embedding(query_text).tolist()
    
    # 1. 벡터 검색 기반 스코어 계산
    vector_query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_embedding}
                }
            }
        }
    }

    response = es.search(index=index_name, body=vector_query)
    
    # threshold를 적용해 결과 필터링
    vector_filtered_results = [
        hit for hit in response["hits"]["hits"]
        if hit["_score"] - 1.0 >= threshold  # 스코어에서 1.0을 빼고 threshold와 비교
    ]

    # 2. 어휘 검색으로 후보군 확장
    lexical_query = {
        "query": {
            "match": {
                "title": {
                    "query": query_text,
                    "fuzziness": "AUTO",
                    "prefix_length": 1
                }
            }
        }
    }

    lexical_results = es.search(index=index_name, body=lexical_query)

    # 3. 두 결과를 병합 (중복 제거 및 스코어 조정 가능)
    combined_results = {hit["_id"]: hit for hit in vector_filtered_results}  # 벡터 결과 우선
    for hit in lexical_results["hits"]["hits"]:
        if hit["_id"] not in combined_results:  # 어휘 검색 결과 추가
            combined_results[hit["_id"]] = hit

    # 4. 스코어 기준 정렬
    sorted_results = sorted(combined_results.values(), key=lambda x: x["_score"], reverse=True)

    return {
        "hits": {
            "hits": sorted_results,
            "total": {"value": len(sorted_results), "relation": "eq"}
        }
    }
