# day12 > 6_부동산_기술_통계.py
import json

import pandas as pd

# 1. Flask 모듈 가져오기
from flask import Flask

# 2-1. CORS 허용, 서로 다른 port 간의 데이터 통신 허용
from flask_cors import CORS

apart = pd.read_csv("아파트(전월세)_실거래가_20240829162019.csv", sep=",",header=0, engine="python", encoding="cp949")

# 부동산 기본 정보 출력
print(apart.info())

# 띄워 쓰기를 "_" 로 변경
apart.columns = apart.columns.str.replace(" ", "_")
print(apart.head())

# 부동산 기술 통계
def desc1() :
    desc = apart.describe().to_dict()
    desc_list = []
    desc_list.append(desc)
    print(desc_list)
    return desc_list

# 전월세 기준 부동산 기술 통계
def desc2() :
    desc2 = apart.groupby("전월세구분")["전용면적(㎡)"].describe().to_dict()
    desc2_list = []
    desc2_list.append(desc2)
    print(desc2)
    print(desc2_list)
    return desc2_list

# 부평구의 동명을 중복 없이 출력
def desc3() :
    local = apart["시군구"].unique().tolist()
    dic = {}
    for i in local :
        dic[f"{i}"] = i
    dic_json = json.dumps(dic, ensure_ascii=False)
    return dic_json

# 가장 거래 수가 많은 단지명 1~5등 출력
def desc4() :
    count = apart["단지명"].value_counts()
    count_rank = count.head().to_json(force_ascii=False)
    print(count_rank)
    return count_rank

# 2. Flask 객체 생성, # 1과 # 2의 코드 고정
app = Flask(__name__)

# 모든 HTTP 에 대해 CORS 허용
CORS(app)


@app.route("/apart1", methods=["GET"])
def apart1():
    desc = desc1()
    return desc

@app.route("/apart2", methods=["GET"])
def apart2():
    desc = desc2()
    return desc

@app.route("/apart3", methods=["GET"])
def apart3():
    desc = desc3()
    return desc

@app.route("/apart4", methods=["GET"])
def apart4():
    desc = desc4()
    return desc

# 3. Flask 웹 실행
if __name__ == "__main__" :
    app.run(host="0.0.0.0", debug=True)
    # http://127.0.0.1:5000
    # http://localhost:5000
    # http://192.168.30.239:5000