# day07 > 2_모듈.py

# [1] import 모듈 이름
    # 모듈이름.함수명()
import mod1

mod1.add(3,4)

# [2] from 모듈이름 import 함수명

from mod1 import add
add(3,4)

# [3] from 모듈이름 import *
from mod1 import *
sub(3,4)

# [4]
import mod2
print(mod2.PI)  # 3.141592

a = mod2.math()
print(a)                      # <mod2.math object at 0x000002516405D430>
print(a.solv(2))              # 12.566368
print(mod2.add(3,4))    # 7

from mod2 import math, PI
print(PI)                    # 3.141592
b = math()
print(b)                     # <mod2.math object at 0x000002619CA2D7C0>

# [5] 다른 패키지의 모듈 호출
from src.day06.Task6 import Name
s = Name("qqq",10)