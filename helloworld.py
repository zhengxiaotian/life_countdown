# -*- coding=utf-8 -*-
"""
@FileName: helloworld.py
@Author: JunDay
@Date: 2019/7/11
@Doc describing: 
"""
from flask import Flask
import json

app = Flask(__name__)

@app.route('/hello_world', methods=['GET',])
def hello_world():
    return json.dumps({"msg" : "Hello World!"})

if __name__ == "__main__":
    app.run(debug=True, port=5030)
