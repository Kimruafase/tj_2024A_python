# day07 > task9 > Main.py

"""
    CSV 파일 다루기
    파일 : 인천광역시_부평구_인구현황.csv
    [조건 1] 부평구의 동마다 Region 객체 생성
    [조건 2] Region 객체 변수 1. 동 이름 2. 총 인구수 3. 남자 인구수 4. 여자 인구수 5. 세대수
    [조건 3] 모든 객체를 리스트에 담은 상태에서 모든 객체의 정보를 f포메팅으로 콘솔창에 출력
    [조건 4] 출력 시 동마다 남 녀 비율 계산해서 출력하시오.
"""
from Region import Region

list = []
def load() :
    try :
        f = open("인천광역시_부평구_인구현황.csv", "r") # 파일 열기
        next(f)                                     # 파일 첫번쨰 줄 스킵
        pop = f.read()                              # 파일 전체 읽여서 저장
        lines = pop.split("\n")                     # 줄바꿈 처리한 기준으로 자름
        for i in lines :                            # 반복문
            if i :                                  # 반복 변수가 존재한다면
                cols = i.split(",")                 # "," 기준으로 잘라서 변수에 저장
                popluation = Region(cols[0], cols[1], cols[2], cols[3], cols[4])    # Region 클래스 생성자로 인수 5개 넣어서 생성
                list.append(popluation)             # 리스트에 대입
        f.close()                                   # 파일 닫음
        return list                                 # 리스트 반환
    except Exception :
        return list


if __name__ == "__main__" :
    print("--start--")
    list = load()               # load() 메소드 호출 후 리스트에 대입
    for i in list :             # 반복문
        ratio = i.ratio(i.people, i.man)    # 반복변수의 ratio 메소드 호출해서 반복변수의 people 객체와 man 객체 매개변수로 보내고 계산값 반환받음
        print(f"{i.region:5s}, {i.people:5d}, {i.man:5d}, {i.woman:5d}, {i.home:5d}, {ratio}% {100-ratio}%")    # 객체와 ratio 메소드 계산값 출력

