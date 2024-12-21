from fastapi import FastAPI, HTTPException
from knnVectorSearch import knn_search
from getEmbedding import get_embedding
from elasticsearch import Elasticsearch
from pydantic import BaseModel

app = FastAPI()

es = Elasticsearch("https://allmartsystem.shop/elastic")
# es = Elasticsearch("http://localhost:9200")

# 요청 스키마 정의
class IndexRequest(BaseModel):
    name: str
    sku: str

@app.get("/fapi")
async def root():
    return {"message": "Connected to FastAPI"}

@app.get("/fapi/search")
async def search_sku(query: str):
    try:
        print(f"Received query: {query}")  # 쿼리 로그

        # Elasticsearch 검색 수행
        results = knn_search("products", query)

        # 응답 데이터 검증
        if "hits" not in results or "hits" not in results["hits"]:
            raise ValueError("Invalid response structure from knn_search")

        # SKU 리스트 추출
        sku_list = [
            hit["_source"]["sku"]
            for hit in results["hits"]["hits"]
            if "_source" in hit and "sku" in hit["_source"]  # 데이터 검증 추가
        ]

        print("SKU List:", sku_list)  # SKU 리스트 로그

        return {"skuList": sku_list}

    except Exception as e:
        print(f"Error during SKU search: {str(e)}")  # 에러 로그
        raise HTTPException(status_code=500, detail=f"Error during SKU search: {str(e)}")



@app.post("/fapi/index")
async def index_data(request: IndexRequest):
    try:
        # 요청에서 값 가져오기
        name = request.name
        sku = request.sku
        
        # 이름으로 임베딩 생성
        embedding = get_embedding(name).tolist()

        # Elasticsearch 문서 생성 (SKU를 ID로 사용)
        doc = {"title": name, "embedding": embedding, "sku": sku}

        # Elasticsearch에 저장 (동일한 SKU면 업데이트)
        es.index(index="products", id=sku, body=doc)

        print("상품 등록 성공!!!")

        return {"message": f"Document indexed in 'products' with SKU '{sku}' and title '{name}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
