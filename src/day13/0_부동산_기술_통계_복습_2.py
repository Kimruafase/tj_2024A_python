# day13 > 0_부동산_기술_통계_복습_2.py

# 3년치 CSV 합치고 통계 내기

import pandas as pd

# apart_pd_2022 = pd.read_csv("아파트(전월세)_실거래가_20240830123958.csv",sep=",",engine="python")
# apart_pd_2023 = pd.read_csv("아파트(전월세)_실거래가_20240830124013.csv",sep=",",engine="python")
# apart_pd_2024 = pd.read_csv("아파트(전월세)_실거래가_20240830124027.csv",sep=",",engine="python")

# 0. 모듈 가져오기
import pandas as pd
import json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# 전체 DataFrame 객체 생성
df = pd.DataFrame() # 빈 DataFrame
for year in range(2022, 2025) : # 2022 ~ 2024
    # 각 년도별 CSV 파일을 반복문을 통해 여러번 호출
    df2 = pd.read_csv(f"{year}.csv", encoding="cp949",skiprows=15)
    print(df2.shape)    # .shape : 레코드 수, 열 갯수 확인
    df = pd.concat([df,df2])    # 기존 DataFrame 에 새로운 DataFrame 연결 / 연장
print(df.shape)

# df = pd.read_csv("아파트(전월세)_실거래가_20240829162019.csv", encoding="cp949")
#     # encoding = "utf-8" 기본값 (안 될 경우 "cp949" 사용)
#     # skiprows = n : 특정 n행까지 스킵하고 csv 파일 읽기 가능
# print(df)

# 1. 통계
    # count (갯수), mean(평균), std(표준편차), min(최솟값), max(최댓값), 25%(백분위), 50%(백분위), 75%(백분위)
# print(df.describe().to_json) # json 형식의 문자열 변환
print(json.loads(df.describe().to_json()))

# 2. 그룹화 통계
print(json.loads(df.groupby("전월세구분")["전용면적(㎡)"].describe().to_json()))

# 3. 중복 제거
print(df["시군구"])            # DataFrame 에서 특정 열만 추출
print(df["시군구"].unique())   # (중복 제거 후) 특정 열만 추출

# 4. 레코드 수 세기
# DataFrame 에서 특정 열의 레코드 수
print(df["단지명"].value_counts())
# DataFrame 에서 상위 5개만 추출 -> head()
print(df["단지명"].value_counts().head())
# json 타입으로 변경 후 python 타입으로 변경
print(json.loads(df["단지명"].value_counts().head().to_json()))

# [1]
@app.route("/trans1", methods = ["GET"])
def trans1( ):
    return json.loads(df.describe().to_json())

# [2]
@app.route("/trans2", methods = ["GET"])
def trans2( ):
    return json.loads(df.groupby("전월세구분")["전용면적(㎡)"].describe().to_json())

# [3]
@app.route("/trans3", methods = ["GET"])
def trans3( ):
    return list(df["시군구"].unique())

# [4]
@app.route("/trans4", methods = ["GET"])
def trans4( ):
    return json.loads(df["단지명"].value_counts().head().to_json())

if __name__ == "__main__" :
    app.run(host="0.0.0.0", debug=True)