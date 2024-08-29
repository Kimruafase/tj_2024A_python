# day12 > 3_Pandas_시각화.py
from idlelib.iomenu import encoding

import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt

# [1] pandas 이용해서 csv 파일 생성해보기
# 1. 리스트 변수 a ~ f 까지 선언해서 값 저장
a = [500, 450, 520, 610]
b = [690, 700, 820, 900]
c = [1100, 1030, 1200, 1380]
d = [1500, 1650, 1700, 1850]
e = [1990, 2020, 2300, 2420]
f = [1020, 1600, 2200, 2550]

# 2. 인덱스 에 넣을 제목 리스트 생성
index1 = ["2015년", "2016년", "2017년", "2018년", "2019년", "2020년"]

# 3. 각 열에 맞는 제목 리스트 생성
columns1 = ["1분기", "2분기", "3분기", "4분기"]

# 4. 2차원 배열 DataFrame 사용하기 위해서 list1 리스트 생성해서 a ~ f 까지 저장
list1 = [a,b,c,d,e,f]

# 5. pandas 의 DataFrame 이용해서 행과 열에 제목 정해주고 2차원 배열 생성
list2 = pd.DataFrame(list1, columns = columns1, index = index1)

# 6. 생성한 2차원 배열을 csv 파일로 변환
list2.to_csv("sales.csv", encoding="utf-8", mode="w", index = True)

# [2] matplotlib 이용해서 차트 만들기
# 1. 차트에 표시할 샘플 데이터 준비 (위에 되어 있음)

# 2. x축의 길이를 샘플 데이터의 길이만큼으로 설정
x = range(len(a))

# 3. 라인 plot(선 차트)에 x 축과 y 축 지정하여 라인 플롯 형성, list1 의 반복문을 통해서 반복변수 i 를 y축 데이터로 설정함
for i in list1 :
    plt.plot(x, i)

# 4. 차트 제목 넣기
plt.title("2015 - 2020 Quarterly Sales")

# 5. x축 레이블(제목) 설정
plt.xlabel("Quarters")

# 6. y축 레이블(제목) 설정
plt.ylabel("sales")

# 7. 눈금 이름 리스트 설정, x축
xLabel = ["first", "second", "third", "fourth"]
plt.xticks(x, xLabel, fontsize = 10)

# 8. 범례(막대 구문 이름 표시)
plt.legend(index1)

# 9. 차트 실행
plt.show()



