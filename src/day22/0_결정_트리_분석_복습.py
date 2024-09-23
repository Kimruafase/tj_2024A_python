# day22 > 0_결정_트리_분석_복습.py

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
import graphviz
from sklearn import tree

feature_name_df = pd.read_csv("UCI_HAR_Dataset/UCI HAR Dataset/features.txt", sep = "\s+",
                              header= None, names=["index", "feature_name"], engine="python")
# 1. sep = "\s+" -> 공백으로 구분된 csv 파일
# 2. header = None -> 제목이 없는 파일
# 3. names = [열 이름]

# print(feature_name_df.head())
"""
   index       feature_name
0      1  tBodyAcc-mean()-X
1      2  tBodyAcc-mean()-Y
2      3  tBodyAcc-mean()-Z
3      4   tBodyAcc-std()-X
4      5   tBodyAcc-std()-Y
"""

# print(feature_name_df.shape) # (561, 2)

feature_name= feature_name_df.iloc[:, 1].values.tolist()
# print(feature_name[:5]) # ['tBodyAcc-mean()-X', 'tBodyAcc-mean()-Y', 'tBodyAcc-mean()-Z', 'tBodyAcc-std()-X', 'tBodyAcc-std()-Y']
    # Dataframe 객체.iloc[행 슬라이싱]
    # Dataframe 객체.iloc[행 슬라이싱, 열 번호]
    # Dataframe 객체.iloc[:] -> 모든 행
    # Dataframe 객체.iloc[:, 1] -> 모든 행의 두번째 열 (첫번째 열 제외)
    # .values -> 열의 모든 값들을 추출
    # .tolist() -> 리스트로 변환 함수

# 5. 훈련용, 테스트용 파일 읽어오기
X_train = pd.read_csv("UCI_HAR_Dataset/UCI HAR Dataset/train/X_train.txt", delim_whitespace=True, header=None, encoding="latin-1")
X_train.columns = feature_name  # 피쳐 (열) 이름 대입

X_test = pd.read_csv("UCI_HAR_Dataset/UCI HAR Dataset/test/X_test.txt", delim_whitespace=True, header=None, encoding="latin-1")
X_test.columns = feature_name   # 피쳐 (열) 이름 대입

Y_train = pd.read_csv("UCI_HAR_Dataset/UCI HAR Dataset/train/y_train.txt",sep="\s+",header=None, names=["action"], engine="python")

Y_test = pd.read_csv("UCI_HAR_Dataset/UCI HAR Dataset/test/y_test.txt",sep="\s+",header=None, names=["action"], engine="python")

# print(X_train.shape)    # (7352, 561)
# print(X_test.shape)     # (2947, 561)
# print(Y_train.shape)    # (7352, 1)
# print(Y_test.shape)     # (2947, 1)

# print(X_train.head())
"""
   tBodyAcc-mean()-X  ...  angle(Z,gravityMean)
0           0.288585  ...             -0.058627
1           0.278419  ...             -0.054317
2           0.279653  ...             -0.049118
3           0.279174  ...             -0.047663
4           0.276629  ...             -0.043892
"""

# print(Y_train["action"].value_counts())
"""
action
6    1407
5    1374
4    1286
1    1226
2    1073
3     986
Name: count, dtype: int64
"""

# 6. 종속 변수의
label_name_df = pd.read_csv("UCI_HAR_Dataset/UCI HAR Dataset/activity_labels.txt", sep="\s+", header=None, names=["index", "label"], engine="python")

label_name = label_name_df.iloc[:,1].values.tolist()
# print(label_name)   # ['WALKING', 'WALKING_UPSTAIRS', 'WALKING_DOWNSTAIRS', 'SITTING', 'STANDING', 'LAYING']

"""
    데이터 수집 정리
    > 1. activity_labels.txt : 클래스(종속변수) 값에 따른 분류 값
    > 2. features.txt : 피처(독립변수) 값에 따른 필드(열) 이름
    > 3. 분류된 데이터 제공 vs train_test_split
        > 1) 훈련용
            > 1. X_train.txt
            > 2. Y_train.txt
            
        > 2) 테스트용
            > 1. X_test.txt
            > 2. Y_test.txt
    > 4. 변수
        > 1) X_train    : 독립 변수 Dataframe (훈련용)
        > 2) Y_train    : 종속 변수 Dataframe (훈련용)
        > 3) X_test     : 독립 변수 Dataframe (테스트용)
        > 4) Y_test     : 종속 변수 Dataframe (테스트용)
        > 5) label_name : 종속 변수 값에 따른 분류 값 ex_ 1 (걷기), 2 (오르기), 3 (내리기), 4 (앉기), 5(서 있기), 6 (쉬기)
"""
# 8. 결정 트리 모델 구축하기
dt_HAR = DecisionTreeClassifier(random_state=156) # 결정 트리 분류 분석 객체 생성

dt_HAR.fit(X_train, Y_train)    # 피팅 (지도 학습)

# 9. 모델 예측(샘플 또는 테스트 데이터)
Y_predict = dt_HAR.predict(X_test)  # 피팅된 모델이 새로운 데이터의 독립 변수를 갖고 종속 변수를 예측한다.

# 10. 테스트 데이터를 이용한 모델 예측 정확도 확인
accuracy = accuracy_score(Y_test, Y_predict)    # 정확도 확인, 실제값(Y_test), 예측값(Y_predict)
# print(f"결정 트리 예측 정확도 : {accuracy:.4f}") # 결정 트리 예측 정확도 : 0.8548, 1에 가까울수록 예측을 잘하고 있다.

# 11. (모델 성능 개선) 최적의 하이퍼 매개변수 찾기 -> 최적의 정확도가 높은 트리 찾기, 정확도가 가장 높았을 때의 매개변수를 찾아보자
# 11 - 1. 결정 트리가 사용하는 하이퍼 매개변수 종류 출력
# print(f"결정 트리의 현재 하이퍼 매개변수 : \n{dt_HAR.get_params()}")
    # depth : 트리의 깊이, max_depth : 최대 트리의 길이
    # criterion : 노드 결정 방식
"""
{'ccp_alpha': 0.0, 'class_weight': None, 'criterion': 'gini', 'max_depth': None, 'max_features': None, 
'max_leaf_nodes': None, 'min_impurity_decrease': 0.0, 'min_samples_leaf': 1, 'min_samples_split': 2, 
'min_weight_fraction_leaf': 0.0, 'monotonic_cst': None, 'random_state': 156, 'splitter': 'best'}
"""

# 11 - 2. 최적의 하이퍼 매개변수를 찾을 설정하기 위해 변수 만들기
# params = {
#     "max_depth" : [6, 8, 10, 12, 16, 20, 24] # 다양한 트리의 최대 노드 깊이를 설정
# }

# 11 - 3. 다양한 하이퍼 매개변수 조합을 시도해서 최적의 하이퍼 매개변수를 찾는데 사용되는 모듈, 교차 검증 제공
    # cv 객체 생성
    # GridSearch(확인할 트리 모델 객체, param_grid= 테스트할 설정 변수, scoring = "정확도", cv = 교차 횟수, return_train_score = True)
    # scoring="accuracy"        -> 모델 평가 기준을 정확도 기준으로 하겠다는 뜻을 가진 속성
    # cv = 5                    -> 교차 검증 횟수, 데이터를 5개로 나누어서 5번 반복해서 모델 학습
    # return_train_score = True -> 검증 후 점수도 같이 반환하겠다는 뜻을 가진 속성
    # 미리 설정한 "params"의 "max_depth" 라는 최대 노드 깊이를 (5회) 교차 검증하는 cv 객체
# grid_cv = GridSearchCV(dt_HAR, param_grid=params, scoring="accuracy", cv=5, return_train_score=True)

    # cv 객체 테스트
# grid_cv.fit(X_train, Y_train)

    # 검증 결과를 DataFrame 객체로 변환
# cv_result_df = pd.DataFrame(grid_cv.cv_results_)

    # 필요한 열(필드) 확인
# print(cv_result_df[["param_max_depth", "mean_test_score", "mean_train_score"]])
"""
param_max_depth  mean_test_score  mean_train_score
0                6         0.850791          0.944879
1                8         0.851069          0.982692
2               10         0.851209          0.993403
3               12         0.844135          0.997212
4               16         0.851344          0.999660
5               20         0.850800          0.999966
6               24         0.849440          1.000000
"""

    # 최적의 정확도 -> .best_score_ , 최적의 하이퍼 매개변수 -> .best_params_
# print(f"최고 평균 정확도 : {grid_cv.best_score_:.4f}, 최적 하이퍼 매개변수 : {grid_cv.best_params_}")
# 최고 평균 정확도 : 0.8513, 최적 하이퍼 매개변수 : {'max_depth': 16}
    # 사용처 : 다음에 모델 만들 때 최적의 하이퍼 매개변수를 사용하라
    # dt_HAR = DecisionTreeClassifier(max_depth = 16)

# 12. 최적의 하이퍼 파라미터 찾기2
params = {
    "max_depth" : [8, 6, 20],           # 트리의 최대 길이로 검증
    "min_samples_split" : [8, 16, 24]   # 노드를 분할하기 위해 사용되는 최수 샘플 수의 값들로 검증
}

grid_cv = GridSearchCV(dt_HAR, param_grid=params, scoring="accuracy", cv=5, return_train_score=True)

grid_cv.fit(X_train, Y_train)

cv_result_df = pd.DataFrame(grid_cv.cv_results_)

# print(cv_result_df[["param_max_depth", "param_min_samples_split", "mean_test_score", "mean_train_score"]])
"""
   param_max_depth  param_min_samples_split  mean_test_score  mean_train_score
0                8                        8         0.852023          0.981468
1                8                       16         0.854879          0.979836
2                8                       24         0.851342          0.978237
3                6                        8         0.850791          0.944675
4                6                       16         0.847662          0.944233
5                6                       24         0.846575          0.943621
6               20                        8         0.846040          0.994491
7               20                       16         0.848624          0.990479
8               20                       24         0.849167          0.986772
"""

# print(f"최고 평균 정확도 : {grid_cv.best_score_:.4f}, 최적 하이퍼 매개변수 : {grid_cv.best_params_}")
# 최고 평균 정확도 : 0.8549, 최적 하이퍼 매개변수 : {'max_depth': 8, 'min_samples_split': 16}

    # 결과 바탕으로 모델 재생성
dt_HAR2 = DecisionTreeClassifier(max_depth=8, min_samples_split=16)

    # 개선된 모델로 다시 피팅
dt_HAR2.fit(X_train, Y_train)

    # 개선된 모델로 다시 테스트
Y_predict2 = dt_HAR2.predict(X_test)

    # 예측 정확도 확인
print(accuracy_score(Y_test, Y_predict2))   # 0.8707159823549372


best_dt_HAR = grid_cv.best_estimator_

best_Y_predict = best_dt_HAR.predict(X_test)

best_accuracy = accuracy_score(Y_test, best_Y_predict)

# print(f"best 결정 트리 예측 정확도 : {best_accuracy:.4f}")
# best 결정 트리 예측 정확도 : 0.8717

feature_importance_values = best_dt_HAR.feature_importances_

feature_importance_values_s = pd.Series(feature_importance_values, index=X_train.columns)

feature_top10 = feature_importance_values_s.sort_values(ascending=False)[:10]

plt.figure(figsize=(10, 5))
plt.title("Feature Top 10")

sns.barplot(x = feature_top10, y = feature_top10.index)

# plt.show()

export_graphviz(best_dt_HAR, out_file="tree.dot", class_names=label_name, feature_names=feature_name, impurity=True, filled=True)

with open("tree.dot") as f:
    dot_graph = f.read()

graphviz.Source(dot_graph)


# * 결정 트리 모델 시각화
    # tree.plot_tree(결정 트리 모델 객체, feature_names = [피쳐 이름들], class_names = [클래스 레이블들])
tree.plot_tree(dt_HAR2, feature_names=feature_name, class_names=label_name)

plt.show()