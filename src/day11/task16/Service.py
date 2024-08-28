import math
from collections import Counter
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import json
from operator import itemgetter
def jobkoreaInfo(result):
    url = "https://www.jobkorea.co.kr/Search/?stext=%EC%9E%90%EB%B0%94&tabType=recruit&Page_No=1"
    response = urllib.request.urlopen(url)
    if response.getcode() == 200:
        htmlData = response.read()
        soup = BeautifulSoup(htmlData, 'html.parser')
        total = soup.select_one('.util-total-count').select('em')[0].string;
        total= int( total.replace(',','')) ;print(total)

        pages= math.floor(total / 20 if total % 20 == 0 else total / 20 + 1) ; print(pages)

        for page in range(1, 6):
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
                total = soup.select_one('.util-total-count').select('em')[0].string
                #print(total)
                list=soup.select('.list-item'); #print(list)
                for row in list:


                    if row.select('.list-section-corp')[0].select('a')[0].string==None:
                        continue


                    company=row.select('.list-section-corp')[0].select('a')[0].string.strip()
                    #print(company)
                    title=row.select('.information-title')[0].select('a')[0].text.strip()
                    #print(title)
                    career=row.select('.chip-information-group')[0].select('li')[0].string
                    #print(career)
                    edu=row.select('.chip-information-group')[0].select('li')[1].string
                    contract=row.select('.chip-information-group')[0].select('li')[2].string
                    local=row.select('.chip-information-group')[0].select('li')[3].string
                    period=row.select('.chip-information-group')[0].select('li')[4].string
                    info=[company,title,career,edu,contract,local,period]
                    print(info)
                    result.append(info)

            else:
                print('통신 실패')
        return

def list2d_to_csv():
    result=[]
    jobkoreaInfo(result)
    try:
        qooqoo_tbl=pd.DataFrame(result,columns=('회사명','공고명','경력','학력','계약유형','지역','채용기간'))
        qooqoo_tbl.to_csv('jobkorea.csv',encoding='utf-8',mode='w',index=True)
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
    result = read_csv_to_json('jobkorea')
    total= len(result)

    car=[]
    for career in result:
        data = career.get('경력').replace('·','_').replace('↑','')
        data
        print(data)
        car.append(data)
    counter=dict(Counter(car))
    counter["총공고"]= total
    print(counter)
    list2 = [counter]
    return list2

if __name__=='__main__':
    #list2d_to_csv()
    #result2 = read_csv_to_json('jobkorea') # csv파일을 json으로 가져오는 서비스 호출
    #print(result2)
    load()