# day17 > 3_지리_정보.py
import json

# 주제 : 커피 매장의 주소를 이용한 지도에 마커 표시하기
# 실습파일 준비 : CoffeeBean.csv

import pandas as pd
from flask import Flask
from flask_cors import CORS

# 1. 데이터 수집
df = pd.read_csv("CoffeeBean.csv", encoding="cp949", index_col=0)

# print(df)

# 2. 데이터 가공
    # 주소 데이터를 행정구역 주소 체계에 맞게 정리 # 실습 제외

# 3. 프리롬 제외
    # 지도 시각화는 카카오 지도로 실습

# 4. 플라스크화
app = Flask(__name__)

CORS(app)

@app.route("/")
def index() :
    # DataFrame 객체를 json 으로 변환
    json_data = df.to_json(orient="records", force_ascii=False)

    # json 형식을 py 형식으로 변환
    result = json.loads(json_data)
    return result

if __name__ == "__main__" :
    app.run(host="0.0.0.0", debug=True)