from indexData import index_data

# 샘플 데이터 색인(엘라스틱서치에서 저장 + 검색준비를 의미함)
index_data("products", 1, "이천쌀 20kg")
index_data("products", 2, "쏼 15kg")
index_data("products", 3, "고흥쌀 10kg")
index_data("products", 4, "살 10kg")
index_data("products", 5, "메뚜기살 10kg")
index_data("products", 6, "모하메드살라 10kg")

print("샘플 데이터 색인(엘라스틱서치에서 저장 + 검색준비를 의미함) 완료")
