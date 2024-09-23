# day22 > 1_결정_트리_분석_예제.py

# 데이터 수집 -> https://raw.githubusercontent.com/rickiepark/hg-mldl/master/fish.csv
# 어종의 크기와 모양을 나타내는 여러 특성들을 바탕으로 어종명 예측하기
# Species : 어종명, Weight : 무게, Length : 길이, Diagonal : 대각선 길이, Height : 높이, width : 너비

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

# [1] 데이터 불러오기 및 확인
data = pd.read_csv("https://raw.githubusercontent.com/rickiepark/hg-mldl/master/fish.csv")
# print(data.head())
"""
  Species  Weight  Length  Diagonal   Height   Width
0   Bream   242.0    25.4      30.0  11.5200  4.0200
1   Bream   290.0    26.3      31.2  12.4800  4.3056
2   Bream   340.0    26.5      31.1  12.3778  4.6961
3   Bream   363.0    29.0      33.5  12.7300  4.4555
4   Bream   430.0    29.0      34.0  12.4440  5.1340
"""

# [2] 데이터 분할
x = data[["Weight", "Length", "Diagonal", "Height", "Width"]]
# print(x)
"""
     Weight  Length  Diagonal   Height   Width
0     242.0    25.4      30.0  11.5200  4.0200
1     290.0    26.3      31.2  12.4800  4.3056
2     340.0    26.5      31.1  12.3778  4.6961
3     363.0    29.0      33.5  12.7300  4.4555
4     430.0    29.0      34.0  12.4440  5.1340
..      ...     ...       ...      ...     ...
154    12.2    12.2      13.4   2.0904  1.3936
155    13.4    12.4      13.5   2.4300  1.2690
156    12.2    13.0      13.8   2.2770  1.2558
157    19.7    14.3      15.2   2.8728  2.0672
158    19.9    15.0      16.2   2.9322  1.8792
"""

y = data["Species"]
# print(y)
"""
0      Bream
1      Bream
2      Bream
3      Bream
4      Bream
       ...  
154    Smelt
155    Smelt
156    Smelt
157    Smelt
158    Smelt
Name: Species, Length: 159, dtype: object
"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

# [3] 결정 트리 모델로 훈련용 데이터 피팅
model = DecisionTreeClassifier(random_state=156)

model.fit(x_train, y_train)

# [4] 훈련된 모델 데이터를 기반으로 테스트용 데이터 예측하고 예측 정확도 확인하기
y_predict = model.predict(x_test)

accuracy = accuracy_score(y_test, y_predict)
print(f"개선 전 결정 트리 정확도 : {accuracy}") # 0.625

# [5] 최적의 하이퍼 파라미터 찾기
# params = {"max_depth" : [2, 6, 10, 14], "min_samples_split" : [2, 4, 6, 8]}
params = {"max_depth" : [2, 6, 10, 14], "min_samples_split" : [2, 4, 6, 8]}

grid_cv = GridSearchCV(model, param_grid=params, scoring="accuracy", cv = 5, return_train_score=True)

grid_cv.fit(x_train, y_train)

cv_result_df = pd.DataFrame(grid_cv.cv_results_)
# print(cv_result_df[["param_max_depth", "param_min_samples_split", "mean_test_score", "mean_train_score"]])
"""
    param_max_depth  param_min_samples_split  mean_test_score  mean_train_score
0                 2                        2         0.603162          0.648672
1                 2                        4         0.603162          0.648672
2                 2                        6         0.612253          0.648672
3                 2                        8         0.603162          0.648672
4                 6                        2         0.738340          0.849183
5                 6                        4         0.729249          0.855924
6                 6                        6         0.738340          0.855924
7                 6                        8         0.729249          0.855924
8                10                        2         0.739526          0.979775
9                10                        4         0.748221          0.954954
10               10                        6         0.729644          0.936900
11               10                        8         0.747826          0.925638
12               14                        2         0.738735          1.000000
13               14                        4         0.747826          0.968437
14               14                        6         0.729644          0.939147
15               14                        8         0.756522          0.932380
"""

print(f"최고 평균 정확도 : {grid_cv.best_score_:.4f}, 최적 하이퍼 매개변수 : {grid_cv.best_params_}")
# 최고 평균 정확도 : 0.7565, 최적 하이퍼 매개변수 : {'max_depth': 14, 'min_samples_split': 8}

# [6] 최적의 하이퍼 파라미터 기반으로 모델 개선 후 테스트용 데이터 예측 정확도 확인하기
model2 = DecisionTreeClassifier(max_depth = 10, min_samples_split=8)

model2.fit(x_train, y_train)

y_predict2 = model2.predict(x_test)

accuracy2 = accuracy_score(y_test, y_predict2)
print(f"개선 후 결정 트리 정확도 : {accuracy2}")    # 0.6458333333333334

# 차트 시각화

tree.plot_tree(model2, feature_names=["Weight", "Length", "Diagonal", "Height", "Width"], class_names=["Bream", "Roach", "Whitefish", "Parkki", "Perch", "Pike", "Smelt"])

plt.show()

