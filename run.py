# -*- coding=utf-8 -*-
"""
@FileName: run.py
@Author: JunDay
@Date: 2019/6/8
@Doc describing: 
"""

from flask import Flask
from flask_restful import reqparse
from api import create_api

app = Flask(__name__)


if __name__ == "__main__":
    api = create_api(app)
    app.run(debug=True, port=5050)