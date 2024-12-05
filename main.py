from fastapi import FastAPI, HTTPException
from knnVectorSearch import knn_search
from createIndexWithNori import create_index_with_nori
from getEmbedding import get_embedding
from elasticsearch import Elasticsearch
from pydantic import BaseModel

app = FastAPI()

# es = Elasticsearch("http://10.10.10.54:9200")
es = Elasticsearch("http://localhost:9200")

# FastAPI 서버 시작 시, 인덱스를 생성
create_index_with_nori("products")  # 인덱스 생성 (한 번만 실행)

# 요청 스키마 정의
class IndexRequest(BaseModel):
    productName: str

@app.get("/")
async def root():
    return {"message": "Connected to FastAPI"}

@app.get("/search")
async def search(query: str):
    try:
        results = knn_search("products", query)
        simplified_results = [
            {
                "id": hit["_id"],
                "title": hit["_source"]["title"],
                "score": hit["_score"]
            }
            for hit in results["hits"]["hits"]
        ]
        return {"query": query, "results": simplified_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/index")
async def index_data(request: IndexRequest):
    try:
        # 상품명을 doc_id로 사용
        productName = request.productName
        doc_id = productName  # 상품명을 doc_id로 지정
        embedding = get_embedding(productName).tolist()
        doc = {"title": productName, "embedding": embedding}

        # Elasticsearch에 저장 (동일한 doc_id면 업데이트)
        es.index(index="products", id=doc_id, body=doc)
        return {"message": f"Document indexed in 'products' with title '{productName}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
