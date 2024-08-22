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
        f = open("인천광역시_부평구_인구현황.csv", "r")
        next(f)
        pop = f.read()
        lines = pop.split("\n")
        for i in lines :
            if i :
                cols = i.split(",")
                popluation = Region(cols[0], cols[1], cols[2], cols[3], cols[4])
                list.append(popluation)
        f.close()
        return list
    except Exception :
        return list


if __name__ == "__main__" :
    print("--start--")
    list = load()
    for i in list :
        ratio = i.ratio(i.people, i.man)
        print(f"{i.region:5s}, {i.people:5d}, {i.man:5d}, {i.woman:5d}, {i.home:5d}, {ratio}% {100-ratio}%")

