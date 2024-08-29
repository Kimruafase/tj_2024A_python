# day12 > 2_Matplotlib.py

# 파이썬에서 데이터를 시각화 해주는 패키지
# 데이터 분석 결과를 시각화하여 직관적으로 이해하기 위해서 사용
# 선(라인) 차트, 바 차트, 파이(원형) 차트, 히스토그램, 산점도 등등

# 1. 설치
"""
>  Matplotlib 모듈 설치
    > 방법 1. from bs4 에 커서를 두고 빨간 느낌표 출력 후 -> install package
    > 방법 2. 상단 메뉴 -> file -> python interpreter -> [+] 버튼 클릭 후 Matplotlib 검색 후 패키지 선택 -> 설치
        > pip : 파이썬에서 패키지 소프트웨어를 설치 / 관리하는 시스템
    > 방법 3. 터미널 열고 pip install matplotlib
"""

# 2. 모듈 가져오기
import matplotlib
from matplotlib.pyplot import xlabel

# 3. 버전 확인
print(matplotlib.__version__)   # 3.9.2

# 4. pyplot 모듈 import
import matplotlib.pyplot as plt

# 5. 예제 1
# 1) 차트에 표시할 샘플 데이터 준비
x = [2016, 2017, 2018, 2019, 2020]
y = [350, 410, 520, 695, 543]

# 2) 라인 plot(선 차트)에 x 축과 y 축 지정하여 라인 플롯 형성
plt.plot(x, y)

# 3) 차트 제목 넣기
plt.title("Annual sales")

# 4) x축 레이블(제목) 설정
plt.xlabel("year")

# 5) y축 레이블(제목) 설정
plt.ylabel("sales")

# 6) 차트 실행
plt.show()


# 6. 예제 2
# 1) 샘플 데이터
y1 = [350, 410, 520, 695]
y2 = [200, 250, 385, 350]
# 0부터 y1 리스트의 길이만큼 리스트 생성 [0,1,2,3]
x = range(len(y1))

# 2) x축과 y축 데이터를 지정하여 바 차트 생성, .bar(), width : 막대 굵기, color : 막대 색상
plt.bar(x, y1, width=0.7, color="blue")
plt.bar(x, y2, width=0.7, color="red", bottom=y1)

# 3) 차트 제목
plt.title("Quarterly sales")

# 4) x축 레이블(제목)
plt.xlabel("Quarters")

# 5) y축 레이블(제목)
plt.ylabel("sales")

# 6) 눈금 이름 리스트 설정
xLabel = ["first", "second", "third", "fourth"]
plt.xticks(x, xLabel, fontsize = 10)

# 7) 범례(막대 구문 이름 표시)
plt.legend(["chair", "desks"])

# 8) 차트 실행
plt.show()

# 7. 예제 3 (산점도) : x축과 y축의 값 관계를 시각화, 각 데이터 포인트는 두 변수의 값을 x축과 y축에 대응시켜 점으로 표현

# 1) 데이터 준비
import random

x = [random.random() for i in range(50)]    # 50개의 요소를 난수로 생성하여 리스트 생성
# print(x)
y = [random.random() for i in range(50)]
# print(y)

# 2) 산점도 차트 생성
plt.scatter(x, y)

# 3) 차트 실행
plt.show()

