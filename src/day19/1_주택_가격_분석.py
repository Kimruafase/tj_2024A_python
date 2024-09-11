# day19 > 1_주택_가격_분석.py

import numpy as np
import pandas as pd
from pyexpat import features
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns



# 1. 데이터 준비
"""
> 보스턴 주택 데이터 가져오기, sklearn 1.2 버전 이후 제공 X
from sklearn.datasets import load_boston

boston = load_boston()
print(boston)
"""
# 보스턴 주택 정보가 있는 URL
data_url = "http://lib.stat.cmu.edu/datasets/boston"

# 해당 URL 지정해서 DataFrame 으로 가져오기
# sep "\s+" : 데이터 간의 공백으로 구분된 csv
# skiprows = 22 : 위에서 22행까지 생략
# header = None : 헤더가 없다는 의미
raw_df = pd.read_csv(data_url, sep="\\s+", skiprows=22, header=None)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

# 주택 관련 변수들(독립 변수, feature)
# print(data.shape)
# 주택 가격(종속 변수, target)
# print(target.shape)

# 독립 변수의 이름
feature_names =  ['CRIM', 'ZN', 'INDUS','CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']

# 독립 변수 데이터와 독립 변수 이름으로 DataFrame 생성
boston_df = pd.DataFrame(data, columns= feature_names)
# print(boston_df.head())

boston_df["PRICE"] = target
# print(boston_df.head())
# print(boston_df.shape)  # (506, 14)

# print(boston_df.info()) # 열 이름, 열의 데이터 갯수, 데이터 타입, 메모리
"""
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 506 entries, 0 to 505
Data columns (total 14 columns):
 #   Column   Non-Null Count  Dtype  
---  ------   --------------  -----  
 0   CRIM     506 non-null    float64
 1   ZN       506 non-null    float64
 2   INDUS    506 non-null    float64
 3   CHAS     506 non-null    float64
 4   NOX      506 non-null    float64
 5   RM       506 non-null    float64
 6   AGE      506 non-null    float64
 7   DIS      506 non-null    float64
 8   RAD      506 non-null    float64
 9   TAX      506 non-null    float64
 10  PTRATIO  506 non-null    float64
 11  B        506 non-null    float64
 12  LSTAT    506 non-null    float64
 13  PRICE    506 non-null    float64
dtypes: float64(14)
memory usage: 55.5 KB
"""

# 2. 분석 모델 구축
# 1) target 과 feature 구분하기
# 종속 변수, target, 주택 가격
Y = boston_df["PRICE"]

# 독립 변수, feature, 주택 가격 외 정보
X = boston_df.drop(["PRICE"], axis = 1, inplace = False)

# 2) 훈련용 과 평가용 분할하기
    # train_test_split(독립 변수, 종속 변수, test_size = 분할 비율, random_state = 난수 생성 시드)
    # test_size = 0.3 -> 훈련용 data 는 70%, 테스트용 data 는 30%로 분할
    # x_train : 훈련용 독립 변수, x_test = 테스트용 독립 변수, y_train = 훈련용 종속 변수, y_test = 테스트용 종속 변수
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state= 156)

# print(x_train.shape)    # (354, 13)
# print(x_test.shape)     # (152, 13)

# 선형 회귀 모델 객체 생성
LR = LinearRegression()

# 훈련용 독립 변수 데이터와 훈련용 종속 변수 데이터로 모델 훈련
LR.fit(x_train, y_train)

# print(LR) # LinearRegression()

# Y 절편과 예측 계수 확인
# print(LR.intercept_)    # 40.995595172164506
# print(LR.coef_)
"""
[-1.12979614e-01  6.55124002e-02  3.44366694e-02  3.04589777e+00
 -1.97958320e+01  3.35496880e+00  5.93713290e-03 -1.74185354e+00
  3.55884364e-01 -1.42954516e-02 -9.20180066e-01  1.03966156e-02
 -5.66182106e-01]
"""

# 테스트용 독립 변수(주택 가격 외 정보, 30%의 데이터) 데이터를 통해서 예측 종속 변수 데이터 생성
y_predict = LR.predict(x_test)

# print(y_predict)
"""
[23.15424087 19.65590246 36.42005168 19.96705124 32.40150641 17.66341192
 30.32844101 17.8513932  10.86187069 12.83177966 21.18350434 16.41212257
 28.66817527 37.01110952 23.42172197 24.56906089 14.55434775 11.51023436
 30.27784089 23.48027467 22.86210577 17.61623753 21.2528808  17.29802868
 34.06118291  7.19879841 13.39928425 19.4234468  13.2423286   8.3336837
 29.34933073 11.83768837 19.84125562 23.97623235 16.34351261 13.20973749
 14.3352014  17.26323753 17.37091562 23.84644351 32.8390912   9.3866759
 19.06694335 -3.98840206 19.87721947 21.26003361 24.17775745 35.35923599
 20.32415303 28.23212889 32.67560962 40.83910565 41.19126206 19.78588457
 25.0134137  24.13111046 19.62715719 33.49344219 23.61402811 15.31513017
 22.70657074 25.78436589 23.99723589  8.78013424 21.81929237 39.68193998
 32.8907251  30.20417723 14.35610647 23.56129992 13.6987184  32.17099211
 36.43647957 27.41243794 21.43887413 29.94548936 20.80737308 26.76489459
 23.19924205 18.7295963  30.4434358  17.92366103 19.96350973 22.90321583
 30.35722286 19.1416058  34.82981423 35.95421976 21.08435113 28.16227294
 33.9844885  13.09683348 25.83254741 28.31598334 24.09461934 26.53533695
 13.78463019 27.52845855 30.96700768 22.15390363 27.52458794 20.92341491
 12.20099558 16.86757413 23.1869979  25.27201058 24.87600819 29.56220534
 14.39300773 23.74503763 23.00928065 27.59611128 14.63924951 19.88668982
 20.77437658 36.65236819 24.34502539 11.00066258 17.85805638 31.97402161
 31.8757576  23.05268046 27.47026659 34.21658142 21.45953092 25.732922
  8.82822141 16.45252491 24.54156705 30.71990499 20.78378788 19.29671324
 34.96155332 20.95681683 35.98751661 22.43270522 19.44758239 18.41029637
 19.11220591 23.80294646 23.17652339 19.34566115 14.73400581 15.68343526
 35.65243238 21.07768237 29.71070004 21.10104869 24.5559244  24.09374799
 18.47882862 31.83335094]
"""

# 테스트용 종속 변수 데이터와 예측용 종속 변수 데이터 간의 MSE, RMSE, R**2 SCORE(결정 계수), Y절편, 회귀 계수 값 측정
# y_test    : 동일한 feature 정보를 갖고 있는 실제 주택 가격
# y_predict : 동일한 feature 정보를 갖고 만든 예측 주택 가격
MSE = mean_squared_error(y_test, y_predict)
RMSE = np.sqrt(MSE)
R2_SCORE = r2_score(y_test, y_predict)
print(f" MSE = {MSE}")              # MSE = 17.296915907902093
print(f" RMSE = {RMSE}")            # RMSE = 4.158956107955708
print(f" R2_SCORE = {R2_SCORE}")    # R2_SCORE = 0.757226332313893

print(f" Y절편 = {LR.intercept_}")    # Y절편 = 40.995595172164506
# 회귀 계수 값 = [ -0.1   0.1   0.    3.  -19.8   3.4   0.   -1.7   0.4  -0.   -0.9   0. -0.6]
print(f" 회귀 계수 값 = {np.round(LR.coef_, 1)}")    # 기울기

coef = pd.Series(data = np.round(LR.coef_, 2), index= X.columns)
coef.sort_values(ascending=False)
print(coef)
"""
CRIM       -0.11
ZN          0.07
INDUS       0.03
CHAS        3.05
NOX       -19.80
RM          3.35
AGE         0.01
DIS        -1.74
RAD         0.36
TAX        -0.01
PTRATIO    -0.92
B           0.01
LSTAT      -0.57
dtype: float64
"""

# 3. 결과 시각화
fig, axs = plt.subplots(figsize = (16, 16), ncols= 3, nrows= 5)

x_features = ['CRIM', 'ZN', 'INDUS','CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']

for i, feature in enumerate(x_features) :   # for index, 요소값 in enumerate(리스트) :
    row = int(i / 3)    # i = 0, 1, 2 일때 row = 0, i = 3, 4, 5일 때 row = 1 ~ 그 후 반복
    col = i % 3         # i = 0 -> col = 0 , i = 1 -> col = 1, i = 2 -> col = 2 , 그 후 col = 0, 1, 2 반복
    sns.regplot(x = feature, y = "PRICE", data = boston_df, ax = axs[row][col])

    # y 절편은 독립 변수가 0 일 때 종속 변수의 값, 위치
    # 회귀 계수는 독립 변수가 1 증가할 때마다 종속 변수의 증가 or 감소를 나타냄, 기울기
    # 신뢰 구간은 차트에서 좁으면 관계가 안정적이라고 해석할 수 있다. 넓다면 예측이 불안정하고 관계가 불명확하다.
    # 신뢰 구간은 +- 5%로 잡는다.
plt.show()
