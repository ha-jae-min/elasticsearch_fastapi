from fastapi import FastAPI, HTTPException
from knnVectorSearch import knn_search
from createIndexWithNori import create_index_with_nori

app = FastAPI()

# FastAPI 서버 시작 시, 인덱스를 생성
create_index_with_nori("products")  # 인덱스 생성 (한 번만 실행)

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

