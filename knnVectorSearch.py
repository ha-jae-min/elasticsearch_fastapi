from elasticsearch import Elasticsearch
from getEmbedding import get_embedding
from sklearn.metrics.pairwise import cosine_similarity

# es = Elasticsearch("http://10.10.10.54:9200")
es = Elasticsearch("http://localhost:9200")

def knn_search(index_name, query_text, threshold=0.7):  # threshold 추가
    query_embedding = get_embedding(query_text).tolist()

    # 1. 어휘 기반 검색으로 후보군  narrowing
    candidate_query = {
        "match": {
            "title": {  # 또는 다른 적절한 필드
                "query": query_text,
                "fuzziness": "AUTO",  # Fuzziness 추가 (AUTO, 1, 2 등)
                "prefix_length": 2,  # prefix_length 추가
                "max_expansions": 50  # 확장 갯수 제한
            }
        }
    }



    candidate_results = es.search(index=index_name, body={"query": candidate_query, "size": 1000}) # 최대 100개 후보군

    filtered_results = []


    # 2. 후보군의 embedding과 비교하여 threshold 이상인 결과만 필터링
    for hit in candidate_results["hits"]["hits"]:
        doc_embedding = hit["_source"].get("embedding")  # embedding 필드가 없을 경우 처리
        if doc_embedding:
            similarity = cosine_similarity([query_embedding], [doc_embedding])[0][0]
            if similarity >= threshold:
               hit["_score"] = similarity  # score 업데이트
               filtered_results.append(hit)

    # score 기준으로 정렬
    filtered_results.sort(key=lambda x: x["_score"], reverse=True)


    return {
        "hits": {
            "hits": filtered_results,
            "total": {
                "value": len(filtered_results),  # 총 히트 수 업데이트
                "relation": "eq"  #  관계를 eq로 설정
            }
        }


    }