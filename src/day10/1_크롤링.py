# day10 > 1_크롤링.py

# 정적 웹 페이지 크롤링

# [1] 설치
"""
    > (1) BeautifulSoup 모듈 설치
        > 방법 1. from bs4 에 커서를 두고 빨간 느낌표 출력 후 -> install package
        > 방법 2. 상단 메뉴 -> file -> python interpreter -> [+] 버튼 클릭 후 BeautifulSoup 검색 후 패키지 선택 -> 설치
            > pip : 파이썬에서 패키지 소프트웨어를 설치 / 관리하는 시스템

    > (2) HTML 파싱
        > 변수명 = BeautifulSoup(HTML 파일 객체, "html.parser")

    > (3) 파싱 메소드 , 속성
        > 1) .find( 식별자 , 속성명 = 값 )   : 지정한 식별자 과 속성명 동일한 태그 조회
            > find( div )
            > find( div , class_="box1" )
            > find( div , id = "box2" )

        > 2) .select_one()
            > select_one( div 또는 .box1 또는 #box2 )

        > 3) .findAll() : 지정한 식별자가 일치한 여러개 태그 추출해서 리스트로 반환

        > 4) .select()
            > .태그명    : 해당 태그들의 첫번째태그 추출
            > .text     : 마크업 사이의 문자열 반환 , 자식 , 자손 가능 , 주로 중첩텍스트 일때
            > .string   : 마크업 사이의 문자열 , 자식만 가능 , 자손 불가능 , 주로 단일텍스트 일떄
            > .attrs    : 해당 마크업의 속성 목록/리스트 반환
"""
from fileinput import close

from bs4 import BeautifulSoup

# [2] HTML 파일 객체
htmlFile = open("1_웹페이지.html", encoding="utf-8")

# [3] BeautifulSoup 객체 생성
htmlObj = BeautifulSoup(htmlFile, "html.parser")
print(htmlObj)
"""
---- 실행 결과 ----

<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Title</title>
</head>
<body>
    <div>
        [1] 여기를 크롤링 하세요.
    </div>
    <div class="box1">
        [2] 여기를 크롤링 하세요.
    </div>
    <div id="box2">
        [3] 여기를 크롤링 하세요.
    </div>
</body>

"""

# [4] 특정 마크업 조회하기, .find(식별자), select_one(식별자) : 지정한 식별자의 마크업 조회하기
print(htmlObj.find("div"))
"""
    <div>
        [1] 여기를 크롤링 하세요.
    </div>
"""
print(htmlObj.select_one("div"))
"""
    <div>
        [1] 여기를 크롤링 하세요.
    </div>
"""

# [5] 특정 마크업 여러개 조회하기, findAll(식별자), select(식별자) : 지정한 식별자의 마크업 여러개 조회하기
print(htmlObj.findAll("div"))
"""
    [<div>
        [1] 여기를 크롤링 하세요.
    </div>, 
    <div class="box1">
        [2] 여기를 크롤링 하세요.
    </div>, 
    <div id="box2">
        [3] 여기를 크롤링 하세요.
    </div>]
"""
print(htmlObj.select("div"))    # 검색 결과가 동일하다.
"""
    [<div>
        [1] 여기를 크롤링 하세요.
    </div>, 
    <div class="box1">
        [2] 여기를 크롤링 하세요.
    </div>, 
    <div id="box2">
        [3] 여기를 크롤링 하세요.
    </div>]
"""

# [6] .text : 호출된 마크업의 내용을 담은 문자열 반환, 조회, .string 도 가능하다.
print(htmlObj.find("div").text)     # [1] 여기를 크롤링 하세요.
print(htmlObj.find("div").string)   # [1] 여기를 크롤링 하세요.

# [7] 반복문과 같이 활용
for div in htmlObj.select("div") :  # 모든 div를 추출해서 리스트 반환한 다음 리스트 길이만큼 반복문 처리
    print(div.string)               # div 하나씩 내용을 추출
"""
---- 실행 결과 ----

        [1] 여기를 크롤링 하세요.
    

        [2] 여기를 크롤링 하세요.
    

        [3] 여기를 크롤링 하세요.
"""

# [8] class 식별자를 이용한 조회
print(htmlObj.find(".box1"))    # None
print(htmlObj.find("box1"))     # None
print(htmlObj.find("div",class_= "box1"))
"""
    <div class="box1">
        [2] 여기를 크롤링 하세요.
    </div>
"""
print(htmlObj.select_one(".box1"))
"""
    <div class="box1">
        [2] 여기를 크롤링 하세요.
    </div>
"""
print(htmlObj.find("div",id="box2"))
"""
    <div id="box2">
        [3] 여기를 크롤링 하세요.
    </div>
"""
print(htmlObj.select_one("#box2"))
"""
    <div id="box2">
        [3] 여기를 크롤링 하세요.
    </div>
"""

# 연습
html = '''
    <h1 id="title">한빛출판네트워크</h1>
    <div class="top">
        <ul class="menu">
            <li><a href="http://wwww.hanbit.co.kr/member/login.html"class="login">로그인</a>
            </li>
        </ul>
        <ul class="brand">
            <li><a href="http://www.hanbit.co.kr/media/">한빛미디어</a></li>
            <li><a href="http://www.hanbit.co.kr/academy/">한빛아카데미</a></li>
        </ul>
    </div>'''

# [1] html 파싱 객체
soup = BeautifulSoup(html, "html.parser")
print(soup)
"""
<h1 id="title">한빛출판네트워크</h1>
<div class="top">
<ul class="menu">
<li><a class="login" href="http://wwww.hanbit.co.kr/member/login.html">로그인</a>
</li>
</ul>
<ul class="brand">
<li><a href="http://www.hanbit.co.kr/media/">한빛미디어</a></li>
<li><a href="http://www.hanbit.co.kr/academy/">한빛아카데미</a></li>
</ul>
</div>
"""
print(soup.prettify())
"""
<h1 id="title">
 한빛출판네트워크
</h1>
<div class="top">
 <ul class="menu">
  <li>
   <a class="login" href="http://wwww.hanbit.co.kr/member/login.html">
    로그인
   </a>
  </li>
 </ul>
 <ul class="brand">
  <li>
   <a href="http://www.hanbit.co.kr/media/">
    한빛미디어
   </a>
  </li>
  <li>
   <a href="http://www.hanbit.co.kr/academy/">
    한빛아카데미
   </a>
  </li>
 </ul>
</div>
"""

# [2] 태그(마크업) 파싱하기
    # 1. 파싱객체.마크업명
print(soup.h1)  # <h1 id="title">한빛출판네트워크</h1>
print(soup.div)
print()
"""
<div class="top">
<ul class="menu">
<li><a class="login" href="http://wwww.hanbit.co.kr/member/login.html">로그인</a>
</li>
</ul>
<ul class="brand">
<li><a href="http://www.hanbit.co.kr/media/">한빛미디어</a></li>
<li><a href="http://www.hanbit.co.kr/academy/">한빛아카데미</a></li>
</ul>
</div>
"""
print(soup.ul)
print()
"""
<ul class="menu">
<li><a class="login" href="http://wwww.hanbit.co.kr/member/login.html">로그인</a>
</li>
</ul>
"""
print(soup.li)
print()
"""
<li><a class="login" href="http://wwww.hanbit.co.kr/member/login.html">로그인</a>
</li>
"""
print(soup.a)   # <a class="login" href="http://wwww.hanbit.co.kr/member/login.html">로그인</a>
print()

print(soup.findAll("ul"))
print()
"""
[<ul class="menu">
<li><a class="login" href="http://wwww.hanbit.co.kr/member/login.html">로그인</a>
</li>
</ul>, 
<ul class="brand">
<li><a href="http://www.hanbit.co.kr/media/">한빛미디어</a></li>
<li><a href="http://www.hanbit.co.kr/academy/">한빛아카데미</a></li>
</ul>]
"""
print(soup.findAll("li"))
print()
"""
[<li><a class="login" href="http://wwww.hanbit.co.kr/member/login.html">로그인</a>
</li>, 
<li><a href="http://www.hanbit.co.kr/media/">한빛미디어</a></li>, 
<li><a href="http://www.hanbit.co.kr/academy/">한빛아카데미</a></li>]
"""
print(soup.findAll("a"))
print()
"""
[<a class="login" href="http://wwww.hanbit.co.kr/member/login.html">로그인</a>, 
<a href="http://www.hanbit.co.kr/media/">한빛미디어</a>, 
<a href="http://www.hanbit.co.kr/academy/">한빛아카데미</a>]
"""
# .attrs : 지정한 마크업의 속성의 이름과 값으로 딕셔너리 반환
print(soup.a.attrs) # {'href': 'http://wwww.hanbit.co.kr/member/login.html', 'class': ['login']}
print()

print(soup.a["href"])   # http://wwww.hanbit.co.kr/member/login.html
print()

print(soup.a["class"])  # ['login']
print()

print(soup.find("ul",attrs={"class" : "brand"}))    # vs find(마크업, class_="클래스명")
print()
"""
<ul class="brand">
<li><a href="http://www.hanbit.co.kr/media/">한빛미디어</a></li>
<li><a href="http://www.hanbit.co.kr/academy/">한빛아카데미</a></li>
</ul>
"""

print(soup.find(id="title"))    # <h1 id="title">한빛출판네트워크</h1>, vs .select_one("#ID명")
print()

print(soup.find(id="title").string) # 한빛출판네트워크
print()

print(soup.select("div > ul.brand > li"))
print()
"""
[<li><a href="http://www.hanbit.co.kr/media/">한빛미디어</a></li>, 
<li><a href="http://www.hanbit.co.kr/academy/">한빛아카데미</a></li>]
"""


for li in soup.select("div>ul.brand>li") :
    print(li.string)
"""
한빛미디어
한빛아카데미
"""
