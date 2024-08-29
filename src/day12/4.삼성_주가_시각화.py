# day12 > 4.삼성_주가_시각화.py

# 실습 1 : 삼성전자의 최근 1년 시세 정보를 CSV 로 다운 받아서 pandas 의 DataFrame 으로 읽어오기
# CSV 파일을 DataFrame 으로 읽어서 출력
# 삼성전자의 최근 1년 시세 중 일자별 종가를 차트를 막대 차트로 표현

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import xlabel, ylabel

# 1. csv 파일 DataFrame 으로 읽기
    # 주의할 점 : 파일들의 인코딩 방식 -> utf-8, cp949, ISO-8859 등
df = pd.read_csv("data_4949_20240829.csv", encoding="cp949", engine="c")

# 2. DataFrame 확인
print(df)

# 3. 그래프 x축 쓰기 위한 길이 확인
print(len(df))

# 4. 바 크기 만들기 위해서 y축 데이터 확인
print(df["종가"])

# 5. x, y축 데이터 설정
x = df["일자"]            # pandas 의 DataFrame 객체의 일자(열)만 x축으로 사용
y = df["종가"]            # pandas 의 DataFrame 객체의 종가(열)만 y축으로 사용

# 6. y축 데이터 설정 후 plt.bar 로 바 그래프 설정
plt.bar(x,y)
# for i in df.loc[:, '종가'] :
#     # y축 데이터 확인용
#     print(i)
#     # 바 그래프 생성
#     plt.bar(x,i)

# 7. 그래프 제목 설정
plt.title("Samsung Chart")

# 8. x, y축 제목 설정
xlabel("date")
ylabel("closing price")

# 7. 실행
plt.show()