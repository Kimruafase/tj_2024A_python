# day08 > app > Controller.py

# flask 객체 가져오기
from App import app

@app.route("/", methods = ["GET"])
def index1() :
    return {"data1" : 1, "data2" : 2}

@app.route("/", methods = ["POST"])
def index2() :
    return [1,2,3]