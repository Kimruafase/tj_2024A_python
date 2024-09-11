# day19 > 2_자동차_연비_분석.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

data_df = pd.read_csv("auto-mpg.csv", header=0, engine="python")
# print(data_df.shape)    # (398, 9)
# print(data_df.head())
"""
    mpg  cylinders  displacement  ... model_year  origin                   car_name
0  18.0          8         307.0  ...         70       1  chevrolet chevelle malibu
1  15.0          8         350.0  ...         70       1          buick skylark 320
2  18.0          8         318.0  ...         70       1         plymouth satellite
3  16.0          8         304.0  ...         70       1              amc rebel sst
4  17.0          8         302.0  ...         70       1                ford torino
"""

data_df = data_df.drop(["car_name", "origin", "horsepower"], axis = 1, inplace= False)
# print(data_df.shape)    # (398, 6)
# print(data_df.head())
"""
    mpg  cylinders  displacement  weight  acceleration  model_year
0  18.0          8         307.0    3504          12.0          70
1  15.0          8         350.0    3693          11.5          70
2  18.0          8         318.0    3436          11.0          70
3  16.0          8         304.0    3433          12.0          70
4  17.0          8         302.0    3449          10.5          70
"""

# print(data_df.info())
"""
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 398 entries, 0 to 397
Data columns (total 6 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   mpg           398 non-null    float64
 1   cylinders     398 non-null    int64  
 2   displacement  398 non-null    float64
 3   weight        398 non-null    int64  
 4   acceleration  398 non-null    float64
 5   model_year    398 non-null    int64  
dtypes: float64(3), int64(3)
memory usage: 18.8 KB
None
"""

# 데이터 분할
y = data_df["mpg"]
x = data_df.drop(["mpg"], axis=1, inplace=False)

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size= 0.3, random_state= 0)

# 선형 회귀 모델 구축 및 예측 데이터 생성
LR = LinearRegression()

LR.fit(x_train, y_train)

y_predict = LR.predict(x_test)

# 각종 선형 회귀 모델 평가 지표 측정
MSE = mean_squared_error(y_test, y_predict)
RMSE = np.sqrt(MSE)
R2_SCORE = r2_score(y_test, y_predict)
y_intercept = np.round(LR.intercept_, 2)
y_coef = np.round(LR.coef_, 2)

# print(f" MSE = {MSE}")                  # MSE = 13.22808190146073
# print(f" RMSE = {RMSE}")                # RMSE = 3.637043016168592
# print(f" R2_SCORE = {R2_SCORE}")        # R2_SCORE = 0.7884481821859446
# print(f" y_intercept = {y_intercept}")  # y_intercept = -9.24
# print(f" y_coef = {y_coef}")            # y_coef = [-0.16  0.01 -0.01 -0.06  0.72]

coef = pd.Series(data = y_coef, index= x.columns)
coef.sort_values(ascending= False)
# print(coef)
"""
cylinders      -0.16
displacement    0.01
weight         -0.01
acceleration   -0.06
model_year      0.72
dtype: float64
"""

# 시각화
fig, axs = plt.subplots(figsize = (16, 16), ncols=3, nrows= 2)

x_features = ["model_year", "acceleration", "displacement", "weight", "cylinders"]
plot_color = ["r", "b", "y", "g", "r"]

for i, feature in enumerate(x_features) :
    row = int(i / 3)
    col = i % 3
    sns.regplot(x = feature, y = "mpg", data = data_df, ax = axs[row][col])

# plt.show()

print("연비를 예측하고 싶은 차의 정보를 입력해주세요.")

cylinders_1 = int(input("cylinders : "))
displacement_1 = int(input("displacement : "))
weight_1 = int(input("weight : "))
acceleration_1 = int(input("acceleration : "))
model_year_1 = int(input("model_year : "))

mpg_predict = LR.predict([[cylinders_1, displacement_1, weight_1, acceleration_1, model_year_1]])

print(f"이 자동차의 예상 연비(MPG)는 {mpg_predict}입니다. ")
