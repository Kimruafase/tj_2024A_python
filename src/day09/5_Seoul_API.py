# day09 > 5_Seoul_API.py
import json
import urllib
import urllib.request

# 연습문제 : 서울 열린 데이터 광장에서 민주주의 서울 자유제안을 크롤링하여 JSON 파일로 저장하시오.

# https://data.seoul.go.kr/dataList/OA-2563/S/1/datasetView.do

# url : http://openAPI.seoul.go.kr:8088/(인증키)/xml/ChunmanFreeSuggestions/1/5
# 인증키 : key, xml : JSON, service : ChunmanFreeSuggestions,  1 : start(페이징 시작 번호) , 5 : end(페이징 끝 번호)

key = "564b72425070706f383766514a5548"

def getRequestUrl(url) :
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        print(f" >> CODE 1 요청 URL : {response}")
        if response.getcode() == 200:
            return response.read().decode("utf-8")
    except Exception as e:
        print(e)
        return None

def getSuggestionItem(start, end) :
    # 기본 URL
    base = "http://openapi.seoul.go.kr:8088/"

    parameter = f"{key}/json/ChunmanFreeSuggestions"    # 인증키 포함한 url
    parameter += f"/{start}"                            # 시작 페이징 번호 포함 url
    parameter += f"/{end}"                              # 끝 페이징 번호 포함 url

    url = base + parameter  # url 예시 : http://openAPI.seoul.go.kr:8088/(인증키)/xml/ChunmanFreeSuggestions/1/5
    print(f"url : {url}")

    responseDecode = getRequestUrl(url)  # 4. url 요청 후 응답 객체 받기
    if responseDecode == None:  # 5. 만약에 응답 객체가 None 이라면 None 반환
        return None
    else:  # 6. 만약 응답객체가 존재하면 json 형식을 파이썬 객체로 반환
        return json.loads(responseDecode)
        # Python : json.loads() -> JSON 형식 -> python 형식 변환, json.dumps() -> python 형식 -> JSON 형식(문자열 타입) 변환
        # JS : JSON.parse() -> JSON 형식 -> JS 형식 변환, JSON.stringfy() -> JS 형식 -> JSON 형식(문자열 타입) 변환


def getSuggestionService(start,end) :
    jsonResult = []                             # jsondata 담을 리스트 선언

    jsonData = getSuggestionItem(start, end)    # 페이징 첫 번호와 끝 번호 보내서 json 데이터 받아옴
    if jsonData != None :                       # 만약 데이터가 존재한다면
        print(jsonData)
        for item in jsonData['ChunmanFreeSuggestions']['row'] : # 데이터의 ChunmanFreeSuggestions 안에 리스트 row 의 반복변수 item 만큼 반복
            print( item )
            num = item["SN"]                                    # 데이터 각각 추출해서 가져옴
            title = item["TITLE"]
            content = item["CONTENT"]
            score = item["VOTE_SCORE"]
            date = item["REG_DATE"]
            dic = {"SN" : num, "TITLE" : title, "CONTENT" : content, "VOTE_SCORE" : score, "REG_DATE" : date}   # 딕셔너리에 key 와 value 담고
            jsonResult.append(dic)                                                                              # jsonResult 에 대입
    else :
        return
    return jsonResult






def main() :
    # api 서비스 이용 요청 시 필요한 데이터 값 입력받기
    start = int(input("페이징 첫 번호를 입력해주세요. \n"))
    end = int(input("페이징 마지막 번호를 입력해주세요. \n"))

    jsonResult = []  # 1. 수집할 데이터를 저장할 리스트 객체
    jsonResult = getSuggestionService(start,end)
    print(jsonResult)  # 확인용

    with open(f"ChunmanFreeSuggestion__{start}__{end}.json","w",encoding="utf-8") as file :
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        file.write(jsonFile)

if __name__ == "__main__" :
    main()