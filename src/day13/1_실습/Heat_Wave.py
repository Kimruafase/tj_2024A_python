import pandas as pd
from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)

CORS(app)

hot05 = pd.read_csv("hot05.csv", encoding="utf-8",engine="python")
hot06 = pd.read_csv("hot06.csv", encoding="utf-8",engine="python")
# print(hot05); print(hot06)

hot = pd.concat([hot05, hot06])

# print(hot)
# 데이터 전체 출력
print(hot.to_json(orient="records", force_ascii=False))

# 기술 통계
# 1. 전체 통계
print(hot.describe().to_json(orient='columns',force_ascii=False))

# 2. 일시별로 묶기
print(hot.groupby("일시")['평균상대습도(%)'].describe().to_json(orient='index',force_ascii=False))

# 3. 최고 체감 온도 최다 5개
print(hot["최고체감온도(°C)"].value_counts().head().to_json())

# 4. 습도 중복 제거
print(hot["지점"].unique().tolist())

@app.route("/hot1", methods=["GET"])
def hot1() :
    return json.loads(hot.describe().to_json(orient='columns',force_ascii=False))

@app.route("/hot2", methods=["GET"])
def hot2() :
    return json.loads(hot.groupby("일시")['평균상대습도(%)'].describe().to_json(orient='index',force_ascii=False))

@app.route("/hot3", methods=["GET"])
def hot3() :
    return json.loads(hot["최고체감온도(°C)"].value_counts().head().to_json())

@app.route("/hot4", methods=["GET"])
def hot4() :
    return hot["지점"].unique().tolist()

@app.route("/hot5", methods=["GET"])
def hot5() :
    return json.loads(hot.to_json(orient="records", force_ascii=False))

if __name__ == "__main__" :
    app.run(host="0.0.0.0",debug=True)