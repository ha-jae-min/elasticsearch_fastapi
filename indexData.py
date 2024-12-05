from elasticsearch import Elasticsearch
from getEmbedding import get_embedding

es = Elasticsearch("http://10.10.10.54:9200")

def index_data(index_name, doc_id, text):
    embedding = get_embedding(text).tolist()  # NumPy 배열을 리스트로 변환
    doc = {
        "title": text,
        "embedding": embedding
    }
    es.index(index=index_name, id=doc_id, body=doc)
    print(f"'{text}' 문서가 인덱스 '{index_name}'에 저장되었습니다.")


# # 색인 과정 흐름
# {
#   "title": "이천쌀 20kg",
#   "embedding": [0.23, -0.41, 0.85, ...]  // 벡터 임베딩
# }
