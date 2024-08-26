# day09 > 4_Naver_API_2.py
import json
import urllib.request
import urllib
from http.client import responses

# 네이버 api 로 블로그에서 입력 받은 값에 대한 검색 결과를 크롤링 해서 JSON 파일로 저장하세요.

# 공문 : https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4

# 네이버 개발자 센터에서 어플리케이션 신청 후 발급받은 키와 비밀번호
naver_client_id = "rd1TQKTRVEscxcHwWU9v"
naver_client_secret = "J3i5BKyyBZ"

# [CODE 1] 1. 지정한 URL 의 요청을 실행하고 응답을 받는 함수
def getRequestUrl(url) :
        req = urllib.request.Request(url)                                   # 2. 지정한 URL 설정
        req.add_header("X-Naver-Client-Id", naver_client_id)            # 3. HTTP 요청 객체 내 HEADER 정보 추가
        req.add_header("X-Naver-Client-Secret",naver_client_secret)     # 4. HTTP 요청 시 네이버 api 키와 비밀번호 전송

        try :   # 예외처리
            response = urllib.request.urlopen(req)                          # 5. 지정한 url 실행 후 응답 반환
            print(f"code 1 요청 url 결과 상태 : {response.getcode()}")
            if response.getcode() == 200 :                                  # 6. 만약에 응답의 상태가 2xx 이면 성공
                return response.read().decode("utf-8")                      # 7. 실행된 url 내 모든 http 내용 읽어오기
        except Exception as e :
            print(e)
            return None                                                     # 8. 응답이 없으면 None

# [CODE 2]
# 0. 매개변수로 검색대상, 검색어, 시작번호, 한번에 표기할 갯수를 받아서 url 구성하여 getRequestUrl() 메소드에게 요청하여 응답 객체를 받아서 JSON 반환하는 함수
def getNaverSearch(node, srcText, page_start, display) :
    base = "https://openapi.naver.com/v1/search"                            # 1. 요청 url 의 기본 주소
    node = f"/{node}.json"                                                  # 2. 요청 url 의 검색 대상과 파일 이름
        # https://openapi.naver.com/v1/search/news.json
    parameter = f"?query={urllib.parse.quote(srcText)}&start={page_start}&display={display}"    # 3. 요청 url 의 파라미터
        # 공문 : https://developers.naver.com/docs/serviceapi/search/news/news.md#%ED%8C%8C%EB%9D%BC%EB%AF%B8%ED%84%B0
        # https://openapi.naver.com/v1/search/news.xml?query=%EC%A3%BC%EC%8B%9D&display=10&start=1&sort=sim
    url = base + node + parameter                                           # 4. url 합치기
    print(f"code 2 요청 URL : {url}")

    responseDecode = getRequestUrl(url)                                     # 5. url 요청을 하고 응답 받기, [CODE 1]

    if responseDecode == None :                                             # 6. 만약에 url 응답 객체가 없다면 None 반환
        return None
    else :                                                                  # 7. 응답 객체가 있다면 JSON 형식으로 반환
        return json.loads(responseDecode)                                   # json.loads(문자열) : Python 에서 json 형식으로 반환시키기 위해 사용

# [CODE 3]
def getPostData(post, jsonResult, cnt) :
    # 응답 받을 객체의 요소들 -> 공문 https://developers.naver.com/docs/serviceapi/search/news/news.md#%EC%9D%91%EB%8B%B5 에서 확인
    title = post["title"]
    description = post["description"]
    bloggername = post["bloggername"]
    bloggerlink = post["bloggerlink"]
    link = post["link"]

    dic = {"cnt" : cnt, "title" : title, "description" : description, "bloggername" : bloggername, "bloggerlink" : bloggerlink, "link" : link}
    jsonResult.append(dic)

    return

# [CODE 0]
def main() :
    node = "blog"                           # 1. 크롤링할 대상 [ 네이버가 제공하는 검색 대상 : 1. news 2. blog 3. shop 등등]
    srcText = input("검색어를 입력하세요. \n") # 2. 사용자 입력으로 받은 검색어 변수
    cnt = 0                                 # 3. 검색 결과 갯수
    jsonResult = []                         # 4. 검색 결과를 정리하여 저장할 리스트 변수

    # 5. 1부터 100까지의 검색 결과를 처리한다. 5. [code 2] 네이버 뉴스 검색 결과에 대한 응답을 저장하는 객체
    jsonResponse = getNaverSearch(node, srcText, 1, 100)
    # jsonResponse["total"] -> total : 총 검색 결과 개수, start : 검색 시작 위치, display : 한 번에 표시할 검색 결과 개수, item : 개별 검색 결과
    # JSON 형식의 결괏값에서는 items 속성의 JSON 배열로 개별 검색 결과를 반환합니다.
    # https://openapi.naver.com/v1/search/news.xml?query=월드컵&display=100&start=1
    print(f"jsonResponse : {jsonResponse}")
    total = jsonResponse["total"]   # 6. 전체 검색 결과 갯수

    # 7. 응답 객체가 None 이 아니면서 응답 객체의 display 가 0이 아니면 무한반복
    while((jsonResponse != None) and (jsonResponse["display"] != 0)) :
        # 8. 검색 결과 리스트(items) 에서 하나씩 item(post) 호출 # 공문 : https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4
        for post in jsonResponse["items"] : # 8. 응답 받은 검색 결과 중에서 한개를 저장한 객체
            cnt += 1    # 응답 개수 변수 1 증가
            # 9. [code 3] 검색 결과 한 개를 처리한다.
            getPostData(post, jsonResult, cnt)

        # 10. start 증가시킨다 , 첫번째 요청 -> 1 , 100 두번째 요청 -> 101 , 100 세번째 요청 -> 201, 100
        start = jsonResponse["start"] + jsonResponse["display"]

        # 11. 1 ~ 100
        # 무료 버전 기준으로 start : 1001 오류가 발생하면서 종료된다. 1001 이상 하기 위해서는 api 유료 계약 해야한다.
        jsonResponse = getNaverSearch(node, srcText, start, 100)    # 11. [code 2]

    # 12. 출력
    print(f"전체 검색 : {total}건")
    print(f"가져온 데이터는 {cnt}건")
    # print(jsonResponse) # 확인용

    # JSON 으로 파일 처리
    # file = open(f"{srcText}__naver__{node}.json","w",encoding="utf-8")
    #     # worldCup__naver__news.js
    # # python 객체를 json 문자열 타입으로 반환
    #     # json.dumps() : python 객체를 JSON 형식의 문자열로 반환 함수
    #         # json.dumps( 반환할 Python 객체, indent = 들여쓰기 수준, sort_keys = 알파벳 순으로 정렬, ensure_ascii = 아스키문자)
    #         # (1) 변환할 python 객체 : 딕셔너리 또는 리스트, jsonResult : 검색 결과를 정리하여 저장할 리스트 변수
    #         # (2) indent : 생략 시 들여쓰기 없음, 주로 4 정도가 가동성이 좋다
    #         # (3) sort_keys : True(key 값 기준으로 알파벳 순 정렬), False(딕셔너리 키 순서대로)
    #         # (4) ensure_ascii : True(아스키 코드 문자), False(UTF-8 인코딩으로 비 아스키코드 문자)
    # jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
    # # 파일 쓰기
    # file.write(jsonFile)
    # # 파일 닫기
    # file.close()

    with open(f"{srcText}__naver__{node}.json", "w",encoding="utf-8") as file :
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        file.write(jsonFile)

if __name__ == "__main__" :
    main()  # [CODE 0] 메소드 실행