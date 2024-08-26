# day09 > 3_Tour_API.py
import json
import urllib.request
from http.client import responses
from tkinter.ttk import Treeview

# 준비
# (1) 공공데이터 포털 : https://www.data.go.kr -> 로그인
# (2) 출입국관광통계서비스 검색
# (3) 활용 신청

key = "nwPZ%2F9Z3sVtcxGNXxOZfOXwnivybRXYmyoIDyvU%2BVDssxywHNMU2tA55Xa8zvHWK0bninVkiuZAA4550BDqIbQ%3D%3D"

# [CODE 1]
def getRequestUrl(url) :
    req = urllib.request.Request(url)
    try :
        response = urllib.request.urlopen(req)
        print(f" >> CODE 1 요청 URL : {response}")
        if response.getcode() == 200 :
            return response.read().decode("utf-8")
    except Exception as e :
        return None

# [CODE 2] 지정한 날짜, 지정한 국가, 구분을 받아서 url 요청하기
def getTourismStatsItem(yyyymm, nat_cd, ed_cd) :
    # 1. 출입국관광통계의 기본 URL
    base = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"

    # 2. 매개변수 : 인증키, 연월, 국가코드, 출입국 구분 코드
    parameter = f"?_type=json&serviceKey={key}"
    parameter += f"&YM={yyyymm}"
    parameter += f"&NAT_CD={nat_cd}"
    parameter += f"&ED_CD={ed_cd}"

    # 3. 합치기
    url = base + parameter
    print(f"url : {url}")
    responseDecode = getRequestUrl(url) # 4. url 요청 후 응답 객체 받기
    if responseDecode == None :         # 5. 만약에 응답 객체가 None 이라면 None 반환
        return None
    else :                              # 6. 만약 응답객체가 존재하면 json 형식을 파이썬 객체로 반환
        return json.loads(responseDecode)
        # Python : json.loads() -> JSON 형식 -> python 형식 변환, json.dumps() -> python 형식 -> JSON 형식(문자열 타입) 변환
        # JS : JSON.parse() -> JSON 형식 -> JS 형식 변환, JSON.stringfy() -> JS 형식 -> JSON 형식(문자열 타입) 변환

# [CODE 3]
def getTourismStateService(nat_cd, ed_cd, nStartYear, nEndYear) :
    jsonResult = []                             # 수집한 데이터를 저장할 리스트 객체
    dataEND = f"{str(nEndYear)}{str(12)}"       # 마지막 년도의 마지막 월 (12월)
    isDataEnd = 0                               # data 의 끝을 확인하는 변수
    for year in range(nStartYear, nEndYear + 1) :   # 시작 년도부터 마지막 년도까지 반복, range ( n (부터) , m (미만))
        print(f" >> year : {year}")
        for month in range(1, 13) :             # 1 ~ 12월까지 반복
            print(f" >> month : {month}")
            if(isDataEnd == 1) :
                break
            # 0>2 : 오른쪽 정렬 >, 2 : 자릿 수, 0 빈칸이면 0채움 # 1 -> 01, 10 -> 10, 5 -> 05
                # str(데이터) : 문자열 타입으로 반환하는 함수
            yyyymm = f"{str(year)}{str(month):0>2}"
            print(f" >> yyyymm : {yyyymm}")

            # 지정한 날짜, 지정한 국가, 구분을 전달하여 요청 후 응답 받음
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)
            if jsonData != None :
                print(jsonData)
                # 만약에 지정한 날짜의 내용물이 없으면
                if jsonData["response"]["body"]["items"] == "" :
                    isDataEnd = 1   # 지정한 날짜에 내용물이 없으므로 반복문 종료
                    print(" >> 데이터 없음")
                    break
                # 아니고 내용물이 있으면
                natName = jsonData["response"]["body"]["items"]["item"]["natKorNm"].replace(" ", "")    # 국가명, 공백 제거
                num = jsonData["response"]["body"]["items"]["item"]["num"]  # 관광객 수
                # 딕셔너리 : 국가명, 국가 코드, 연도 월, 방문자수
                dic = {"nat_name" : natName, "nat_cd" : nat_cd, "yyyymm" : yyyymm, "visit_cnt" : num}
                jsonResult.append(dic)

            else :
                isDataEnd = 1
    return jsonResult

# [CODE 0]
def main() :

    # API 서비스 요청 시 필요한 매개변수들을 입력받기
    nat_cd = int(input("국가 코드 (중국 : 112 / 일본 : 130 / 미국 : 275) \n"))    # 2. 국가 코드(공식 문서 참고한 것)
    nStartYear = int(input("데이터를 몇 년부터 수집할 까요?\n"))                   # 3. 데이터 수집 시작 연도
    nEndYear = int(input("데이터를 몇 년까지 수집할까요?\n"))                      # 4. 마지막 데이터의 연도
    ed_cd = "E"                                                               # 5. 구분 ("E" : 방한외래관광객(입국), "D" : 해외 출국)

    # 6. 서비스 요청 후 응답 객체 받기
    jsonResult = []                                                           # 1. 수집할 데이터를 저장할 리스트 객체
    jsonResult = getTourismStateService(nat_cd,ed_cd,nStartYear,nEndYear)
    print(jsonResult)   # 확인용

    # 7. 응답 받은 Python 객체를 json 으로 변한 후 파일 처리
    with open(f"{nat_cd}__{nStartYear}__{nEndYear}.json","w",encoding="utf-8") as file :
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        file.write(jsonFile)

if __name__ == "__main__" :
    main()

