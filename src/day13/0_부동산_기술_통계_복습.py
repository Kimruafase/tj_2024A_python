# day13 > 0_부동산_기술_통계_복습.py
# [1] 인천광역시 부평구 전월세 1년치 csv 수집 # 부동산 실거래가 : https://rt.molit.go.kr/pt/xls/xls.do?mobileAt=
# [2] CSV 파일을 판다스의 데이터프레임 으로 불러오기
# [3] 데이터 탐색(기술통계)
    # 전체 기술통계 결과를 SPRING index6.html 테이블형식으로 출력  ( HTTP 매핑 임의로 정의 )
# [4] 데이터 모델링( 그룹화 )
    # 전월세 기준으로 그룹해서 전용면적의 기술통계 결과를 SPRING index6.html 테이블형식으로 [3]번 테이블 위에 출력  ( HTTP 매핑 임의로 정의 )


# [5] 추가
    # 1. 부평구의 동 명을 중복없이 출력하시오.
    # 2. 가장 거래수가 많은 단지명 을 1~5 등까지 출력하시오.

# 0. 모듈 가져오기
import pandas as pd
import json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

df = pd.read_csv("아파트(전월세)_실거래가_20240829162019.csv", encoding="cp949")
    # encoding = "utf-8" 기본값 (안 될 경우 "cp949" 사용)
    # skiprows = n : 특정 n행까지 스킵하고 csv 파일 읽기 가능
print(df)

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