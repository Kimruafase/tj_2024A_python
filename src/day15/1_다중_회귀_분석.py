# day15 > 1_다중_회귀_분석.py

# [1] 데이터 수집
import pandas as pd
from statsmodels.formula.api import ols

data = pd.DataFrame({
    '운동시간': [1, 2, 3, 4, 5, 2, 3, 4, 5, 6,
                1, 2, 3, 4, 5, 2, 3, 4, 5, 6],
    '게임시간': [2, 3, 4, 5, 6, 3, 4, 5, 6, 7,
                2, 3, 4, 5, 6, 3, 4, 5, 6, 7],
    '체중': [60, 62, 64, 66, 68, 65, 67, 69, 71, 73,
            62, 64, 66, 68, 70, 64, 66, 68, 70, 72]
})

# [2] 데이터 통계분석 -> 운동 시간에 따른 체중 변화 비교
    # [2-1] 모델 수식 정의
r_formula= "체중 ~ 운동시간 + 게임시간"

    # [2-2] 모델 피팅
model = ols(r_formula, data = data).fit()

    # [2-3] 모델 결과 확인
print(model.params)     # 회귀 계수
"""
Intercept      38.722222
운동시간        -18.277778          # 평균적으로 운동 시간이 1시간 많아질 때마다 체중이 18.27 감소
게임시간         20.444444          # 평균적으로 게임 시간이 1시간 많아질 때마다 체중이 20.44 증가
"""

print(model.pvalues)    # p값
"""
Intercept       1.404150e-24
운동시간         6.968463e-22       # p값이 0.05 이하 -> 귀무 가설 기각 가능
게임시간         5.508640e-28       # p값이 0.05 이하 -> 귀무 가설 기각 가능
"""

# [3] 학습된 모델 기준으로 새로운 샘플 체중을 예측하자 -> 운동시간과 게임시간을 알고 있는 상태에서 체중 예측하기
new_data = pd.DataFrame({
    "운동시간" : [0, 4, 4],
    "게임시간" : [2, 5, 4]
})

# 위의 [2] 에서 학습된 모델을 이용한 예측 수행
    # 모델_객체.predict(새로운_샘플)
sample_predict = model.predict(new_data)

print(sample_predict)
"""
0     79.611111
1     67.833333
2    145.277778
"""

sns.set_style("dark")
sns.distplot(red_wine_quality, kde = True, color = "red", label = "red wine")
sns.distplot(white_wine)