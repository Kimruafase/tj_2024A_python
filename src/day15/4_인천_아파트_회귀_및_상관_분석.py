# day15 > 4_인천_아파트_회귀_및_상관_분석.py
from idlelib.iomenu import encoding

# [1] 가설 : 아파트 "층"과 "건축년도"가 증가하면 "아파트_거래금액"도 비싸질 것이다.

# [2] 주제 : 아파트 "층"과 "건축년도"에 따른 거래금액 추이 비교 분석

# [3] 분석 방법 : 다중 회귀 분석, 상관 분석

# 종속 변수 : 거래금액, 독립 변수 : 층, 건축년도

# 1. 데이터 수집
import pandas as pd
from statsmodels.formula.api import ols, glm
import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm

data =  pd.read_csv("아파트(매매)_실거래가_20240904134550.csv", encoding="cp949",skiprows=15, thousands=",")
# print(data)

# null 값이 있는지 확인
# print(data.isnull().sum())

# 회귀 분석

# 거래금액 : 종속 변수, 층 + 건축년도 : 독립 변수1 + 독립 변수2
r_formula = "거래금액 ~ 층 + 건축년도"

# ols 메소드로 회귀 분석 진행, 매개변수의 첫번째 인자로 종속 변수와 독립 변수로 구성된 변수를 주고
# 두번째 인자는 실제 사용할 변수값을 가진 DataFrame 을 지정한다.
# 완성된 선형회귀 모델은 fit() 함수에 의해 실행되어 regression_result 에 저장된다.
regression_result = ols(r_formula, data = data).fit()
regression_result.summary()

# 선형 회귀 분석 결과 출력
print(regression_result.summary())
"""
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                   거래금액   R-squared:                       0.372
Model:                            OLS   Adj. R-squared:                  0.372
Method:                 Least Squares   F-statistic:                     8213.
Date:                Wed, 04 Sep 2024   Prob (F-statistic):               0.00
Time:                        14:47:10   Log-Likelihood:            -3.0890e+05
No. Observations:               27734   AIC:                         6.178e+05
Df Residuals:                   27731   BIC:                         6.178e+05
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept  -1.826e+06   1.93e+04    -94.699      0.000   -1.86e+06   -1.79e+06
층            575.1930     13.499     42.610      0.000     548.734     601.652
건축년도         926.7088      9.643     96.104      0.000     907.809     945.609
==============================================================================
Omnibus:                    18329.776   Durbin-Watson:                   1.594
Prob(Omnibus):                  0.000   Jarque-Bera (JB):           950094.233
Skew:                           2.552   Prob(JB):                         0.00
Kurtosis:                      31.216   Cond. No.                     3.87e+05
==============================================================================
"""
# 차트의 크기를 지정
fig = plt.figure(figsize=(8, 13))

# 다중 선형 회귀 분석 결과를 갖고 있는 regression_result 를 이용해
# 각 독립 변수의 부분 회귀 플롯을 구한다.
sm.graphics.plot_partregress_grid(regression_result, fig = fig)

# 차트 확인
plt.show()

# 연속형 데이터만 가능하므로 연속형 데이터 열만 추출
data2 = data.select_dtypes(include=[int, float, bool])

# 상관 관계 분석을 위해 DataFrame 에서 corr() 함수 사용
# pearson(피어슨) 상관 계수를 적용하여 상관 계수를 구한다.
apart_corr = data2.corr(method="pearson")

# 상관 계수 출력
print(apart_corr)
"""
               NO        본번        부번  ...      거래금액         층      건축년도
NO       1.000000  0.010013  0.016562  ... -0.091830 -0.046893 -0.058934
본번       0.010013  1.000000 -0.115911  ... -0.110629 -0.008953  0.240463
부번       0.016562 -0.115911  1.000000  ... -0.094270 -0.056279 -0.133272
전용면적(㎡) -0.035989 -0.014673 -0.021945  ...  0.650295  0.170733  0.211530
계약년월    -0.775305 -0.006796 -0.014301  ...  0.064343  0.033352  0.035814
계약일     -0.036876  0.000922 -0.007046  ...  0.004254 -0.002072  0.001612
거래금액    -0.091830 -0.110629 -0.094270  ...  1.000000  0.403498  0.575204
층       -0.046893 -0.008953 -0.056279  ...  0.403498  1.000000  0.374632
건축년도    -0.058934  0.240463 -0.133272  ...  0.575204  0.374632  1.000000
"""

# 상관 계수를 csv 파일로 저장
apart_corr.to_csv("인천_아파트_상관_계수표.csv", index=True, encoding="cp949")
