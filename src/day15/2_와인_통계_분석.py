# day15 > 2_와인_통계_분석.py
    # day12 > 5_와인_통계_분석.py

# day12 > 5_와인_통계_분석.py

# 목표 : 와인 속성을 분석하여 품질 등급을 예측한다

# 1. 데이터 수집 : winequality-red.csv, winequality-white.csv

# 2. 데이터 준비 :
# 2 - 1. CSV 파일의 열 구분자를 ";" 세미콜론 -> "," 쉼표로 변경하여 CSV 파일 재생성

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm


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
r_formula = ("quality ~ fixed_acidity + volatile_acidity + citric_acid + residual_sugar + chlorides + free_sulfur_dioxide + "
             "total_sulfur_dioxide + density + pH + sulphates + alcohol") # 종속 변수와 독립 변수 정의

# (3) ols (선형 회귀 모델)    -> 최소 제곱법
regression_result = ols(r_formula, data = wine).fit()
regression_result.summary()
print(regression_result.summary())
"""
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                quality   R-squared:                       0.292
Model:                            OLS   Adj. R-squared:                  0.291
Method:                 Least Squares   F-statistic:                     243.3
Date:                Wed, 04 Sep 2024   Prob (F-statistic):               0.00
Time:                        10:06:02   Log-Likelihood:                -7215.5
No. Observations:                6497   AIC:                         1.445e+04
Df Residuals:                    6485   BIC:                         1.454e+04
Df Model:                          11                                         
Covariance Type:            nonrobust                                         
========================================================================================
                           coef    std err          t      P>|t|      [0.025      0.975]
----------------------------------------------------------------------------------------
Intercept               55.7627     11.894      4.688      0.000      32.447      79.079
fixed_acidity            0.0677      0.016      4.346      0.000       0.037       0.098
volatile_acidity        -1.3279      0.077    -17.162      0.000      -1.480      -1.176
citric_acid             -0.1097      0.080     -1.377      0.168      -0.266       0.046
residual_sugar           0.0436      0.005      8.449      0.000       0.033       0.054
chlorides               -0.4837      0.333     -1.454      0.146      -1.136       0.168
free_sulfur_dioxide      0.0060      0.001      7.948      0.000       0.004       0.007
total_sulfur_dioxide    -0.0025      0.000     -8.969      0.000      -0.003      -0.002
density                -54.9669     12.137     -4.529      0.000     -78.760     -31.173
pH                       0.4393      0.090      4.861      0.000       0.262       0.616
sulphates                0.7683      0.076     10.092      0.000       0.619       0.917
alcohol                  0.2670      0.017     15.963      0.000       0.234       0.300
==============================================================================
Omnibus:                      144.075   Durbin-Watson:                   1.646
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              324.712
Skew:                          -0.006   Prob(JB):                     3.09e-71
Kurtosis:                       4.095   Cond. No.                     2.49e+05
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 2.49e+05. This might indicate that there are
strong multicollinearity or other numerical problems.
"""

# 학습된 회귀 분석 모델로 새로운 샘플 예측하기
sample1 = wine[wine.columns.difference(["quality", "type"])]
sample1 = sample1[0:5][:]
sample1_predict = regression_result.predict(sample1)
print(sample1_predict)
"""
0    4.997607
1    4.924993
2    5.034663
3    5.680333
4    4.997607
dtype: float64
"""
print(wine[0:5]["quality"])
"""
0    5
1    5
2    5
3    6
4    5
Name: quality, dtype: int64
"""
data = {"fixed_acidity" : [8.5, 8.1], "volatile_acidity" : [0.8, 0.5], "citric_acid" : [0.3, 0.4], "residual_sugar" : [6.1, 5.8],
        "chlorides" : [0.055, 0.04], "free_sulfur_dioxide" : [30.0, 31.0], "total_sulfur_dioxide" : [98.0, 99],
        "density" : [0.996, 0.91], "pH" : [3.25, 3.01], "sulphates" : [0.4, 0.35], "alcohol" : [9.0, 0.88]}
sample2 = pd.DataFrame(data, columns=sample1.columns)
print(sample2)  # 확인용
"""
   alcohol  chlorides  ...  total_sulfur_dioxide  volatile_acidity
0     9.00      0.055  ...                  98.0               0.8
1     0.88      0.040  ...                  99.0               0.5
[2 rows x 11 columns]
"""

sample2_predict = regression_result.predict(sample2)
print(sample2_predict)
"""
0    4.809094
1    7.582129
dtype: float64
"""


# 시각화
sns.set_style("dark")   # 히스토그램의 차트 배경색 설정

    # distplot 객체 생성하여 차트 설정
    # kde : 커널 밀도 추정
    # 밀도 : 어떤 값 또는 구간에 데이터가 얼마나 집중되어 있는지 나타내는 값
sns.distplot(red_quality_group, kde = True, color = "red", label = "red wine")
sns.distplot(white_quality_group, kde = True, label="white wine")

plt.title("Quality of Wine Type")   # 차트 제목
plt.legend()    # 차트 범례 표시

plt.show()      # 차트 보기

# 부분 회귀 시각화에 사용할 등급(종속 변수)과 고정산(독립 변수)을 제외한 모든 열 이름을 리스트로 구성
others = list(set(wine.columns).difference(set(["quality", "fixed_acidity"])))

# partregress : 부분 회귀
    # 종속 변수 : quality
    # 독립 변수 : fixed_acidity
    # others : 다중 회귀 분석에서 분석할 부분 독립 변수를 제외한 나머지 독립 변수 리스트,
    # 고정산 (fixed_acidity)이 등급과의 관계에서 다른 변수들이 미치는 영향을 제거하기 위해서
    # data = wine -> 분석에 사용되는 DataFrame
p, resids = sm.graphics.plot_partregress("quality", "fixed_acidity", others, data= wine, ret_coords=True)

# 차트 보기
plt.show()

# 차트 크기 설정
fig = plt.figure(figsize=(8, 13))

# 다중 회귀 분석 결과를 부분 회귀 플롯으로 그리드 형식으로 차트화
sm.graphics.plot_partregress_grid(regression_result, fig = fig)

# 차트 보기
plt.show()

"""
    > 각 플롯(차트)에서 독립 변수(각 와인 속성)와 종속 변수(등급) 간의 선형 관계의 강도를 차트로 표시
    
    > 기울기, 잔차의 패턴, 점들의 분호 등을 관찰하여 독립 변수가 종속 변수에 미치는 영향 확인
        > 잔차란? 회귀 분석에서 실제 데이터와 회귀 모델 예측한 값과의 차이
        > ex_ 아파트 가격을 예측하는 모델을 만들었을 때 : 실제 가격은 10억인데 모델이 예측한 가격이 8억이라고 할 때 잔차는 2억이다.
            > 잔차가 0에 가까울수록 모델이 데이터 포인트를 잘 예측했다고 할 수 있다.    
            > 잔차가 크면 모데링 데이터 포인트를 잘 예측하지 못했다.
            > 잔차는 모델 성능을 평가하고 개선할 부분을 찾는데 중요한 역할을 한다.
    
    > 플롯이 선형적이고 잔차가 무작위 분포하면 데이터가 잘 설명되고 있는 상태, 점들이 선형에서 크게 벗어나면 모델을 개선할 필요가 있다.
"""