import math
from collections import Counter
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import json
from operator import itemgetter
def jobkoreaInfo(result):
    # 1페이지의 url 정보를 통해 페이지 갯수 계산 가능
    url = "https://www.jobkorea.co.kr/Search/?stext=%EC%9E%90%EB%B0%94&tabType=recruit&Page_No=1"
    response = urllib.request.urlopen(url)
    # 응답 객체를 실행시 가져 오는 코드 값이 200 이라면
    if response.getcode() == 200:
        # 응답 객체를 읽어서 htmlData에 저장
        htmlData = response.read()
        # BeautifulSoup 메소드를 통해서 html 파싱
        soup = BeautifulSoup(htmlData, 'html.parser')
        # 클래스 util-total-count 인 html 마크업을 찾아서 "em" 마크업 선택 후 1번째 "em" 태그 마크업의 string 값 가져옴
        total = soup.select_one('.util-total-count').select('em')[0].string;
        # 쉼표 제거 후 정수 타입 변환
        total= int( total.replace(',', ''))
        # print(total)

        # 페이지 = 전체 게시물 수 / 한 페이지 당 게시물 수, 만약 20으로 나눠서 0으로 떨어지지 않는 다면 + 1 함
        # math.floor() 함수를 통해 소숫점 무조건 내림 처리함
        pages = math.floor(total / 20 if total % 20 == 0 else total / 20 + 1)
        # 페이지 계산 확인용
        print(pages)

        # 임의로 페이지 1 ~ 5로 설정
        for page in range(1, 6):
            # url 페이지 1 ~ 5까지 반복문을 통해 url 변수를 지정해줌
            url=f'https://www.jobkorea.co.kr/Search/?stext=%EC%9E%90%EB%B0%94&tabType=recruit&Page_No={page}'
            response=urllib.request.urlopen(url)
            if response.getcode()==200:
                print('통신 성공')
                # 3. 통신 응답 결과를 읽어 와서 크롤링 파싱 준비
                htmlData = response.read()
                soup = BeautifulSoup(htmlData, 'html.parser')
                # print(soup)
                # 4. 분석한 HTML 식별자들을 파싱, find, findall, select, select_one
                # 4-1 테이블 전체 파싱
                # util-total-count 클래스 속성을 갖고 있는 html 마크업에 접근 후 "em" 마크업 접근해서 1번 인덱스의 strimg 값 가져옴
                total = soup.select_one('.util-total-count').select('em')[0].string
                #print(total)

                # list-item 마크업을 접근해서 list 변수에 저장
                list=soup.select('.list-item')
                #print(list)
                # list 리스트만큼 반복문 돌림
                for row in list:
                    # 만약 클래스 속성이 list-section-corp 인 마크업을 선택했을 때
                    # 1번째 인덱스에서 "a" 접근 후 1번째 인덱스에 문자열 값이 없다면
                    # contiue 가장 최근의 반복문으로 돌아감
                    if row.select('.list-section-corp')[0].select('a')[0].string==None:
                        continue

                    # 회사명에 클래스 속성이 list-section-corp 인 마크업을 선택 후 1번 인덱스에서 "a" 태그 선택해서 1번째 인덱스의 값을 공백 제거해서 가져옴
                    company=row.select('.list-section-corp')[0].select('a')[0].string.strip()
                    # 확인용
                    #print(company)

                    # 공고명 : 명에 클래스 속성이 information-title 인 마크업을 선택 후 1번 인덱스에서 "a" 태그 선택해서 1번째 인덱스의 값을 공백 제거해서 가져옴
                    title=row.select('.information-title')[0].select('a')[0].text.strip()
                    # 확인용
                    #print(title)

                    # 클래스 속성이 chip-information-group 인 html에 접근 후 1번 인덱스에서 li 선택 하고 [0]번째에 문자열 뽑아서 회사명 저장
                    career=row.select('.chip-information-group')[0].select('li')[0].string
                    #print(career)
                    # 클래스 속성이 chip-information-group 인 html에 접근 후 1번 인덱스에서 li 선택 하고 [1]번째에 문자열 뽑아서 공고명 저장
                    edu=row.select('.chip-information-group')[0].select('li')[1].string
                    # 클래스 속성이 chip-information-group 인 html에 접근 후 1번 인덱스에서 li 선택 하고 [2]번째에 문자열 뽑아서 경력 저장
                    contract=row.select('.chip-information-group')[0].select('li')[2].string
                    # 클래스 속성이 chip-information-group 인 html에 접근 후 1번 인덱스에서 li 선택 하고 [3]번째에 문자열 뽑아서 학력 저장
                    local=row.select('.chip-information-group')[0].select('li')[3].string
                    # 클래스 속성이 chip-information-group 인 html에 접근 후 1번 인덱스에서 li 선택 하고 [4]번째에 문자열 뽑아서 채용기간 저장
                    period=row.select('.chip-information-group')[0].select('li')[4].string

                    # info 리스트에 앞에서 생성한 변수들 다 넣어서 저장
                    info=[company,title,career,edu,contract,local,period]
                    # 확인용
                    print(info)
                    # result 리스트에 info 리스트를 append로 추가해줌
                    result.append(info)

            else:
                print('통신 실패')
        return

def list2d_to_csv():
    result=[]
    # jobkoreaInfo() 메소드 호출해서 result 리스트에 값 받아옴
    jobkoreaInfo(result)
    try:
        # pandas의 DataFrame 을 통해 2차원 배열로 재탄생
        jobkorea_tbl=pd.DataFrame(result,columns=('회사명','공고명','경력','학력','계약유형','지역','채용기간'))

        # .to_csv() 메소드를 통해 cvs 파일 생성
        jobkorea_tbl.to_csv('jobkorea.csv',encoding='utf-8',mode='w',index=True)
        return True
    except Exception as e:
        print(e)
        return False

def read_csv_to_json(fileName):
    #1. 판다스를 이용한 csv를 데이터프레임으로 가져오기
    df = pd.read_csv(f'{fileName}.csv',encoding='utf-8',engine='python',index_col=0)
        # index_col=0: 판다스의 데이터프레임워크 형식 유지(테이블형식)
    # 2. 데이터프레임 객체를 JSON으로 가져오기
    jsonResult = df.to_json(orient='records', force_ascii=False)
        # to json(): 데이터프레임 객체 내 데이터를 JSON 반환함수
            # orient='records': 각 행마다 하나의 JSON 객체로 구성
            # force_ascii=Fale: 아스키 문자 사용 여부: True(아스키 사용), False(유니코드 utf-8)
    # 3. JSON 형식의 py타입(객체타입-리스트/딕셔너리)으로 변환
    result = json.loads(jsonResult) # import json 모듈 호출 # json.loads() 문자열타입(json형식) ---> py타입(json형식) 변환
    return result

def load():
    # read_csv_to_json 메소드 호출해서 result에 담음
    result = read_csv_to_json('jobkorea')
    # result 의 길이를 재서 총 공고의 갯수로 계산
    total= len(result)

    # 경력별 분류 데이터를 담기 위한 리스트 선언
    car=[]

    # 채용 정보를 담은 리스트를 반복문 실행
    for career in result:
        # 반복변수가 "경력" 탭을 참조해서 "·"를 "_" 로, "↑"를 "" 로 바꿔서 data 변수에 저장
        data = career.get('경력').replace('·','_').replace('↑','')
        data

        # 확인용
        print(data)

        # 경력별 분류 데이터를 car 리스트에 append로 추가함
        car.append(data)

    # car 리스트를 Counter 내장 함수를 통해서 같은 값끼리 숫자를 세주고 그것을 dict()틀 통해서 딕셔너리의 키와 값으로 바꿔줌
    counter=dict(Counter(car))
    # 딕셔너리에 key"총 공고" 와 vaule total을 추가함
    counter["총공고"]= total
    # 확인용
    print(counter)

    # list2 리스트에 counter 를 리스트로 담아서 저장
    list2 = [counter]
    # list2 반환
    return list2

if __name__=='__main__':
    #list2d_to_csv()
    #result2 = read_csv_to_json('jobkorea') # csv파일을 json으로 가져오는 서비스 호출
    #print(result2)
    load()