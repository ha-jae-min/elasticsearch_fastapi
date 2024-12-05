from elasticsearch import Elasticsearch
from getEmbedding import get_embedding

es = Elasticsearch("http://10.10.10.54:9200")

def create_index_with_nori(index_name):
    # 인덱스 설정
    settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "nori_analyzer": {  # 사용자 정의 nori 분석기
                        "type": "custom",
                        "tokenizer": "nori_tokenizer"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {  # nori 분석기 적용
                    "type": "text",
                    "analyzer": "nori_analyzer"
                },
                "embedding": {  # 벡터 필드
                    "type": "dense_vector",
                    "dims": 200  # 임베딩 차원
                }
            }
        }
    }
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=settings)
        print(f"인덱스 '{index_name}' 생성 완료!")
    else:
        print(f"인덱스 '{index_name}' 이미 존재.")

