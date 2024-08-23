# day08 > task10 > Service.py

from Region import Region

def personData() :
    list = []
    f = open("인천광역시_부평구_인구현황.csv", "r") # 파일 열기
    next(f)                                     # 파일 첫번쨰 줄 스킵
    pop = f.read()                              # 파일 전체 읽여서 저장
    lines = pop.split("\n")                     # 줄바꿈 처리한 기준으로 자름
    for i in lines[ 0 : len(lines)-2 ] :                            # 반복문
        if i :                                  # 반복 변수가 존재한다면
            cols = i.split(",")                 # "," 기준으로 잘라서 변수에 저장
            # print( cols[1] )
            popluation = Region(cols[0], cols[1], cols[2], cols[3], cols[4])    # Region 클래스 생성자로 인수 5개 넣어서 생성
            list.append(popluation)             # 리스트에 대입
    f.close()                                   # 파일 닫음
    return list                                 # 리스트 반환
