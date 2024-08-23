# day08 > 2_Flask_HTTP.py

# Flask 순서 (번호 순)

from flask import Flask # (1)

app = Flask(__name__)   # (2)


class Test :
    pass

# ------------------- HTTP 매핑 ------------------- #
# @app.route("HTTP 경로 정의"), method 와 methods 의 차이점
# return : Flask 에서 보낼 수 있는 HTTP Response Content - Type 은 파이썬의 LIST, 딕셔너리 타입, 문자열 타입(JSON) 제공
@app.route("/1", methods = ["GET"])   # Spring -> GetMapping()
def index1() :
    return "Hello HTTP Method GET"

@app.route("/2", methods = ["POST"])    # Spring -> PostMapping()
def index2() :
    return [3,4]                            # HTTP Response Content-Type -> Content-Type : text/html , application/json
                                            # True, 3 은 타입 오류 발생, Flask 는 논리, 정수 타입으로 HTTP 응답이 불가능하다.

@app.route("/3", methods = ["PUT"])     # Spring -> PutMapping()
def index3() :
    return {"result" : True}                # HTTP Response Content-Type -> Content-Type:	application/json, Spring Boot 에서 @ResponseBody 와 유사

@app.route("/4", methods = ["DELETE"])  # Spring -> DeleteMapping()
def index4() :
    return "True"                             # Class 는 타입 오류 발생, Flask 는 파이썬 객체로 HTTP 응답이 불가능하다.

# ------------------------------------------------ #

if __name__ == "__main__" : # (3)
    app.run(debug = True)   # debug = True -> 디버그(정보 또는 오류를 콘솔 출력 제공) 모드