from elasticsearch import Elasticsearch
from createIndexWithNori import create_index_with_nori

def delete_index(index_name):
    # es = Elasticsearch("http://3.38.203.147:9200")
    es = Elasticsearch("http://localhost:9200")
    
    # 인덱스가 존재하는지 확인 후 삭제
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"인덱스 '{index_name}'가 삭제되었습니다.")
    else:
        print(f"인덱스 '{index_name}'를 찾을 수 없습니다.")

# 예시: "products" 인덱스 삭제
delete_index("products")

# 다시 생성
create_index_with_nori("products") 