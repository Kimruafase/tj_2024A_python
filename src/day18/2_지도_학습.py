# day18 > 2_지도_학습.py

from sklearn.linear_model import LinearRegression   # 독립 변수를 2차원 배열로 사용한다.
import pandas as pd
from sklearn.model_selection import train_test_split    # 모델 평가 시 사용되는 라이브러리
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import numpy as np

# 예제 1
# [1] 데이터 준비
x = [[1], [2], [3], [4], [5]]   # 2차원 배열
y = [2, 4, 5, 4, 5]

# [2] 모델 생성, 회귀 LinearRegression
model = LinearRegression() # 선형 회귀 모델 객체 생성

# [3] 모델 훈련 (지도 학습)
model.fit(x, y)

# [4] y 절편과 회귀 계수 확인
print(model.intercept_) # y절편 -> 2.2, x가 0일 때 y값, 독립 변수가 0일 때 종속 변수의 값
print(model.coef_)      # 회귀 계수(coefficient) -> [0.6], 독립 변수가 1 단위로 증가할 때 종속 변수의 증가 단위

# [5] 예측 값 계산, .predict(새로운 독립 변수) -> 예측 함수
text_x = [[6], [4]]
result = model.predict(text_x)
print(result)   # [5.8 4.6]


# 예제 2
# 통계 프로세스 -> day15
# [1] 가설
# [2] 주제
# [3] 분석 방법
# [4] 결론 및 제언
# [5] 한계점

# 머신러닝 프로세스
# [0] 주제 : 신생아 몸무게에 따른 미래에 성인 키 예측
# [1] 데이터 수집
data = {
    "신생아_몸무게" : [3.5, 4.0, 3.8, 4.2, 3.9],   # 태어났을 때의 몸무게
    "성인_키" : [160, 165, 162, 170, 168]         # 성인이 됐을 때의 키
}

# [2] 데이터 전처리 및 훈련, 데이터 분할
    # 신생아_몸무게 = 독립 변수 / 피처 / 특성 변수
    # 성인_키 = 종속 변수 / 타겟 / 클래스
df = pd.DataFrame(data)
# print(df)
"""
   신생아_몸무게  성인_키
0      3.5   160
1      4.0   165
2      3.8   162
3      4.2   170
4      3.9   168
"""
feature = df[["신생아_몸무게"]]
# print(feature)
"""
 신생아_몸무게
0      3.5
1      4.0
2      3.8
3      4.2
4      3.9
"""
target = df["성인_키"]
# print(target)
"""
0    160
1    165
2    162
3    170
4    168
"""
    # train_test_split(독립 변수, 종속 변수, test_size = 테스트에 사용할 비율, random_state = 난수 시드)
x_train, x_test, y_train, y_test = train_test_split(feature, target, test_size = 0.2, random_state = 0)
    # test_size = 0.2 -> 20% 정도를 테스트 데이터로 사용, 나머지 80%를 훈련 데이터로 사용
    # x_train : 훈련 데이터에 사용할 독립 변수
    # x_text : 테스트 데이터에 사용할 독립 변수
    # y_train : 훈련 데이터에 사용할 종속 변수
    # y_text : 테스트 데이터에 사용할 종속 변수
# [3] 모델 구축 및 학습
    # 모델 구축
model1 = LinearRegression()
    # 모델 학습
# model1.fit(feature, target)
model1.fit(x_train, y_train)

# [4] 모델 평가
    # 독립 변수 테스트 데이터를 사용해서 종속 변수 예측 값 구한다.
    # ex_ 테스트 데이터 : (실제) 신생아_몸무게 -> 3.9, 성인_키 -> 168
    # (실제) 신생아_몸무게 3.9를 갖고 학습 모델의 (예측) 성인_키 -> 169
y_predict_value = model1.predict(x_test)
    # 실제값, 예측값
MAE = mean_absolute_error(y_test, y_predict_value)
print(f" MAE = {MAE}")  # 2.4038461538461604

MSE = mean_squared_error(y_test, y_predict_value)
print(f" MSE = {MSE}")  # 5.778476331360978

RMSE = np.sqrt(MSE)
print(f" RMSE = {RMSE}")    # 2.4038461538461604

R2_SCORE = r2_score(y_test, y_predict_value)
print(f" R2_SCORE = {R2_SCORE}")    # nan
# [5] 예측
    # 만약에 신생아 몸무게가 3.6 으로 태어났을 때 성인이 되면 키가 얼마가 될까요? 예측
    # 만약에 신생아 몸무게가 4.1 으로 태어났을 때 성인이 되면 키가 얼마가 될까요? 예측
new_weight = pd.DataFrame({
    "신생아_몸무게" : [3.6, 4.1]
})

result1 = model1.predict(new_weight)
print(result1)  # [161.02985075 168.11940299]