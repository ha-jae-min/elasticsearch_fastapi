from gensim.models import KeyedVectors
import numpy as np

# Gensim 사전 학습된 모델 로드
# model_path = "/home/ec2-user/product.vec"  # 실제 모델 경로로 수정
model_path = "C:\korea\product.vec"  # 실제 모델 경로로 수정
word2vec = KeyedVectors.load_word2vec_format(model_path, binary=False)

def get_embedding(text: str):
    tokens = text.split()  # 간단히 공백 기준으로 토큰화
    vectors = []

    for token in tokens:
        if token in word2vec:  # 사전에 있는 단어인지 확인
            vectors.append(word2vec[token])

    if vectors:  # 벡터가 있다면 평균 계산
        embedding = np.mean(vectors, axis=0)
    else:  # 벡터가 없으면 기본값 벡터 사용
        embedding = np.zeros(word2vec.vector_size)  # 0 벡터 대신 다른 값을 설정할 수도 있음
        embedding[0] = -1  # 예를 들어 첫 번째 값을 -1로 설정

    return embedding