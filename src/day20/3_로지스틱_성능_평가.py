# day20 > 3_로지스틱_성능_평가.py

from sklearn.metrics import confusion_matrix, precision_score, f1_score, recall_score, roc_auc_score

# 실제 시험 합격 목록
y_true = [0, 0, 0, 1, 1, 0, 1, 1, 1, 1]

# 시험 예측 합격 목록
y_pred = [0, 0, 0, 0, 0, 1, 0, 1, 1, 1]

"""
    > 오차 행렬
        > 실제 클래스(값)은 행
        > 예측 클래스(값)은 열
        >
                TN  FP
                FN  TP
                
        > TP (true positive)    : 실제 값이 양성(1) 이고 예측값도 양성(1) 인 경우
        > TN (true negative)    : 실제 값이 음성(0) 이고 예측값도 음성(0) 인 경우
        > FP (false positive)   : 실제 값이 음성(0) 이고 예측값은 양성(1) 인 경우
        > FN (false negative)   : 실제 값이 양성(1) 이고 예측값은 음성(0) 인 경우
        
    > 정밀도
        > 정밀도 계산식 : 예측 성능을 더 정밀하게 하기 위해 참(TP)인 것의 비율 (예측 성능이 양성(1)인 것 중 실제 값이 양성(1)인 것의 비율)
        > TP / (TP + FP)
    
    > 재현율
        > 재현율 계산식 : 실제 양성 데이터를 정확하게 예측했는지 평가하는 지표 (실제 값이 양성(1)인 것들 중 예측값이 양성(1)인 것의 비율)
        > TP / (FN + TP)
    
    > F1 스코어
        > F1 스코어 계산식 : 정밀도와 재현율을 결합한 평가 지표로 서로 트레이드 오프 관계인 문제점을 고려하여 정확한 평가를 위해 사용됨
        > 2 * ((정밀도 * 재현율) / (정밀도 + 재현율))
        
    > ROC 기반의 AUC 스코어
        > FPR 계산식 : 실제 Negative인 데이터를 Positive로 거짓(false)로 예측한 비율 (실제 값이 음성(0)인 것들 중 예측값이 양성(1)인 비율)
        > FP / (FP + TN)
        
"""

# 1. 오차 행렬
print(confusion_matrix(y_true, y_pred))
"""
[[3 1]
 [3 3]]
    > TP - 3, TN - 5, FP - 1, FN - 1 
"""

# 2. 정밀도
print(precision_score(y_true, y_pred))  # 0.75  -> 수치가 높을수록 정밀하다고 할 수 있다.

# 3. 재현율
print(recall_score(y_true, y_pred))     # 0.5   -> 수치가 높을수록 재현을 잘 하고 있다고 볼 수 있다.

# 4. F1 스코어
print(f1_score(y_true, y_pred))         # 0.6   -> 수치가 높을수록 정밀도와 재현율의 균형이 잘 맞춰져 있다.

# 5. FPR
print(roc_auc_score(y_true, y_pred))    # 0.625 -> 수치가 1에 가까울수록 좋은 성능이라고 평가를 내릴수 있다.