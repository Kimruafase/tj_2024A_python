# day08 > app > App.py

from flask import Flask

app = Flask(__name__)

# Controller.py 의 Mapping Method 전부 호출
from Controller import *

if __name__ == "__main__" :
    app.run(debug = True)