# day12 > 3.Pandas_시각화.py
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt

a = [500, 450, 520, 610]
b = [690, 700, 820, 900]
c = [1100, 1030, 1200, 1380]
d = [1500, 1650, 1700, 1850]
e = [1990, 2020, 2300, 2420]
f = [1020, 1600, 2200, 2550]
index1 = ["2015년", "2016년", "2017년", "2018년", "2019년", "2020년"]
list1 = [a,b,c,d,e,f]

list2 = pd.DataFrame(list1, columns = ["1분기", "2분기", "3분기", "4분기"], index=index1)

list2.to_csv("sales.csv", encoding="utf-8", mode="w", index = True)

# 1) 차트에 표시할 샘플 데이터 준비
x = range(len(a))

# 2) 라인 plot(선 차트)에 x 축과 y 축 지정하여 라인 플롯 형성
plt.plot(x, a, color="green")
plt.plot(x, b, color="red")
plt.plot(x, c, color="blue")
plt.plot(x, d, color="orange")
plt.plot(x, e, color="black")
plt.plot(x, f, color="yellow")

# 3) 차트 제목 넣기
plt.title("2015 - 2020 Quarterly Sales")

# 4) x축 레이블(제목) 설정
plt.xlabel("Quarters")

# 5) y축 레이블(제목) 설정
plt.ylabel("sales")

# 6) 눈금 이름 리스트 설정, x축
xLabel = ["first", "second", "third", "fourth"]
plt.xticks(x, xLabel, fontsize = 10)

# 7) 눈금 이름 리스트 설정, y축
yLabel = ["500", "1000", "1500", "2000", "2500"]


# 범례(막대 구문 이름 표시)
plt.legend(["2015", "2016", "2017", "2018", "2019", "2020"])

# 6) 차트 실행
plt.show()