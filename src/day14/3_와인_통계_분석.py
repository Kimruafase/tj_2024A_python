# day14 > 3_와인_통계_분석.py
    # day12 > 5_와인_통계_분석.py

# day12 > 5_와인_통계_분석.py

# 목표 : 와인 속성을 분석하여 품질 등급을 예측한다

# 1. 데이터 수집 : winequality-red.csv, winequality-white.csv

# 2. 데이터 준비 :
# 2 - 1. CSV 파일의 열 구분자를 ";" 세미콜론 -> "," 쉼표로 변경하여 CSV 파일 재생성

import pandas as pd

# pandas 로 구분자 가져올 때 sep = "csv 구분자", 기본 값은 ,(쉼표)
# header = 0 -> 첫번째 행을 열 이름으로 지정하겠다는 의미
red_pd = pd.read_csv("winequality-red.csv", sep=";", header=0, engine="python")
white_pd = pd.read_csv("winequality-white.csv",sep=";", header=0, engine="python")

# 새로운 CSV 파일로 만들기
    # index = False : DataFrame 의 index 열은 CSV 파일에 포함하지 않는다.
red_pd.to_csv("winequality-red2.csv", index=False)
white_pd.to_csv("winequality-white2.csv", index=False)

# 2 - 2. 데이터 병합하기, 레드 와인과 화이트 와인을 분석하기 위해 하나로 합치기
    # .head() : DataFrame 의 위에서부터 5개 행 출력
print(red_pd.head())
    # 열 추가 : .insert(삽입할 열 위치, colums = "열 이름", value = 값)
    # 0번째(첫번째) 열에 type 열 이름으로 value = "red" 값들을 추가
red_pd.insert(0,column="type",value="red")
print(red_pd.head())

    # (1599, 13), shape : 행 갯수와 열 갯수 반환
print(red_pd.shape)
    # 1599, 인덱스 번호를 넣으면 행 갯수나 열 갯수만 따로 반환 가능
print(red_pd.shape[0])

print(white_pd.head())

white_pd.insert(0,column="type",value="white")
print(white_pd.head())

    # (4898, 13)
print(white_pd.shape)

# 3. 두 개의 DataFrame 합치기, pd.concat([첫번째 DataFrame, 두번째 DataFrame])
wine = pd.concat([red_pd,white_pd])
print(wine)
    # (6497, 13)
print(wine.shape)

# 4. 합친 와인 DataFrame 을 다시 CSV 파일로 변환
wine.to_csv("wine.csv",index=False)

# 5. 데이터 탐색
    # 1) DataFrame 의 기본 정보 출력
print(wine.info())
"""
<class 'pandas.core.frame.DataFrame'>
Index: 6497 entries, 0 to 4897
Data columns (total 13 columns):
 #   Column                Non-Null Count  Dtype  
---  ------                --------------  -----  
 0   type                  6497 non-null   object 
 1   fixed acidity         6497 non-null   float64
 2   volatile acidity      6497 non-null   float64
 3   citric acid           6497 non-null   float64
 4   residual sugar        6497 non-null   float64
 5   chlorides             6497 non-null   float64
 6   free sulfur dioxide   6497 non-null   float64
 7   total sulfur dioxide  6497 non-null   float64
 8   density               6497 non-null   float64
 9   pH                    6497 non-null   float64
 10  sulphates             6497 non-null   float64
 11  alcohol               6497 non-null   float64
 12  quality               6497 non-null   int64  
dtypes: float64(11), int64(1), object(1)
memory usage: 710.6+ KB
None
"""

    # 2) 기술 통계
        # 열 이름에 공백이 있다면 "_" 로 변경
wine.columns = wine.columns.str.replace(" ","_")
print(wine.head())
    # 3) 통계
    # .describe() : 속성(열)마다의 갯수, 평균, std, 최솟값, 전체에 대한 백분율 25%, 50%, 75%, 최댓값
print(wine.describe())
print(wine.describe()["quality"])           # 와인의 quality 통계
print(wine.describe()["quality"].to_list())   # 와인의 quality 통계 리스트

    # 4) 와인 quality 중복값 제거 후 정렬
print(wine["quality"].unique())         # [5 6 7 4 8 3 9]
print(wine.quality.unique())            # [5 6 7 4 8 3 9]
print(sorted(wine.quality.unique()))    # [3 4 5 6 7 8 9]

    # 5) 특정한 열(등급)별로 갯수 반환
print(wine.quality.value_counts())
"""
6    2836
5    2138
7    1079
4     216
8     193
3      30
9       5
"""
    # 6) 갯수 반환한 것을 리스트나 json 타입으로 변환
print(wine["quality"].value_counts().to_list()) # [2836, 2138, 1079, 216, 193, 30, 5]
print(wine["quality"].value_counts().to_json()) # {"6":2836,"5":2138,"7":1079,"4":216,"8":193,"3":30,"9":5}

# 6. 데이터 모델링
    # 1) .groupby("그룹 기준")["속성명"]
    # type 속성으로 그룹해서 quality 속성 기술 통계 구하기
print(wine.groupby("type")["quality"].describe())
"""
        count      mean       std  min  25%  50%  75%  max
type                                                      
red    1599.0  5.636023  0.807569  3.0  5.0  6.0  6.0  8.0
white  4898.0  5.877909  0.885639  3.0  5.0  6.0  6.0  9.0
"""

    # 2) type 속성으로 그룹해서 quality 속성의 평균
print(wine.groupby("type")["quality"].mean())
"""
type
red      5.636023
white    5.877909
"""

    # 3) type 속성으로 그룹해서 quality 속성의 표준편차
print(wine.groupby("type")["quality"].std())
"""
type
red      0.807569
white    0.885639
"""

    # 4) type 속성으로 그룹해서 quality 속성의 평균, 표준편차
print(wine.groupby("type")["quality"].agg(["mean","std"]))
"""
           mean       std
type                     
red    5.636023  0.807569
white  5.877909  0.885639
"""

###############################################################################################################

# 1. t-test
    # 원인 변수(독립 변수) -> red, white                (명목형)
    # 결과 변수(종속 변수) -> quality (1, 2, 3, 4, 5)   (연속형)

# (1) 모듈 호출
from scipy import stats

# (2) 두 집단 표본 만들기
    # 확인
# print(wine.loc[wine["type"]== "red", "quality"])
    # pandas DataFrame
    # wine : 레드 와인과 화이트 와인 자료를 합친 DataFrame 객체
    # .loc(조건, 출력할 열)
red_quality_group = wine.loc[wine["type"] == "red", "quality"]        # type 열의 값이 red 이면 등급 출력
white_quality_group = wine.loc[wine["type"] == "white", "quality"]    # type 열의 값이 white 이면 등급 출력

# (3) t-test
t_amount , p_value = stats.ttest_ind(red_quality_group, white_quality_group)

# 음수는 첫번째 집단의 평균이 두번째 집단보다 낮다는 뜻이다. -> white 등급이 평균적으로 9.68 높다
print(t_amount) # -9.685649554187696
print(p_value)  # 4.888069044201508e-22 -> e-n n : 소수점 갯수

if p_value <= 0.05 :
    print(" 해당 가설은 유의미하다.")
else :
    print(" 해당 가설은 무의미하다.")

# 2. 회귀 분석 (다중 선형 회귀 분석)
# (1) 모듈 호출
from statsmodels.formula.api import ols, glm

# (2) 회귀 모형 수식 (종속 변수와 독립변수를 구성하는 방식 / 공식 : 종속변수명 ~ 독립변수1 + 독립변수2 + 독립변수3)
    # 종속 변수 (결과 / 연속성) 등급
    # 독립 변수 (원인 / 연속성) 알코올
    # 가설 : 알코올 수치에 따라 등급 확인
r_formula = "quality ~ alcohol" # 종속 변수와 독립 변수 정의

# (3) ols (선형 회귀 모델)    -> 최소 제곱법
regression_result = ols(r_formula, data = wine).fit()
regression_result.summary()
print(regression_result.summary())
"""
                            OLS Regression Results                            
==============================================================================
Dep. Variable:               (종속변수)  R-squared:                       0.197
Model:                            OLS   Adj. R-squared:                  0.197
Method:                 Least Squares   F-statistic:                     1598.
Date:                Tue, 03 Sep 2024   Prob (F-statistic):          1.50e-312
Time:                        12:53:42   Log-Likelihood:                -7623.4
No. Observations:                6497   AIC:                         1.525e+04
Df Residuals:                    6495   BIC:                         1.526e+04
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
(절편)          2.4053      0.086     27.988      0.000       2.237       2.574
(독립변수)       0.3253      0.008     39.970      0.000       0.309       0.341
==============================================================================
Omnibus:                      123.922   Durbin-Watson:                   1.636
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              258.800
Skew:                           0.031   Prob(JB):                     6.34e-57
Kurtosis:                       3.976   Cond. No.                         94.3
==============================================================================

Intercept (절편) : 독립변수가 0일때 종속변수의 예측값, x = 0 일 때의 y값
인과 관계 : 알코올과 와인 등급 관계
                 coef      std err        t      P>|t|       [0.025      0.975]
(독립변수)       0.3253      0.008     39.970      0.000       0.309       0.341

    > coef                 : 회귀 계수
        > 0.3253 -> 알코올과 와인 등급의 관계 해석 -> 알코올이 1 단위 증가할 때 마다 등급이 0.3253 증가함. (알코올이 3 증가 시 등급 1 증가 예측)
    > std err              : 표준 오차
    > t                    : t 검증 통계량
    > P > |t|              : t 검증 p값
        > 0.000 -> 0.05 보다 작으면 검증에 효과가 있다. 
    > [0.025        0.975] : 앞 뒤 2.5% 제외하고 사이에 존재하면 신뢰할 수 있는 구간을 뜻하다.
"""
