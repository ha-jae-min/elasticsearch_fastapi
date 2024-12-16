from elasticsearch import Elasticsearch
from getEmbedding import get_embedding
from sklearn.metrics.pairwise import cosine_similarity

# es = Elasticsearch("http://10.10.10.54:9200")
es = Elasticsearch("http://localhost:9200")

def knn_search(index_name, query_text, threshold=0.7):
    try:
        # 1. 어휘 검색 쿼리 작성 (개선된 어휘 검색)
        lexical_query = {
            "query": {
                "match": {
                    "title": {
                        "query": query_text,
                        "fuzziness": "AUTO",  # 오타 보정
                        "prefix_length": 2,  # 최소 일치 길이
                        "max_expansions": 50  # 후보군 확장 제한
                    }
                }
            },
            "size": 50  # 어휘 검색 결과 제한
        }

        # 어휘 검색 실행
        lexical_response = es.search(index=index_name, body=lexical_query)

        # 2. 벡터 임베딩 생성
        query_embedding = get_embedding(query_text).tolist()

        # 벡터 검색 쿼리 작성
        vector_query = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_embedding},
                    },
                },
            },
            "size": 50  # 벡터 검색 결과 제한
        }

        # 벡터 검색 실행
        vector_response = es.search(index=index_name, body=vector_query)

        # 벡터 결과 필터링 (threshold 적용)
        vector_filtered_results = [
            hit for hit in vector_response["hits"]["hits"]
            if hit["_score"] - 1.0 >= threshold
        ]

        # 3. 어휘 검색 결과를 우선 순위로 병합
        combined_results = {hit["_id"]: hit for hit in lexical_response["hits"]["hits"]}
        for hit in vector_filtered_results:
            if hit["_id"] not in combined_results:  # 중복 제거
                combined_results[hit["_id"]] = hit

        # 4. 병합된 결과를 스코어 기준으로 정렬
        sorted_results = sorted(
            combined_results.values(),
            key=lambda x: x["_score"],
            reverse=True,
        )

        # 최종 결과 반환
        return {
            "hits": {
                "hits": sorted_results,
                "total": {"value": len(sorted_results), "relation": "eq"},
            }
        }

    except Exception as e:
        print(f"Error during KNN and lexical search: {str(e)}")
        raise RuntimeError(f"KNN and lexical search failed: {str(e)}")
