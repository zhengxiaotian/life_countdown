# -*- coding=utf-8 -*-
"""
@FileName: __init__.py.py
@Author: JunDay
@Date: 2019/6/8
@Doc describing: 
"""

from flask_restful import Api
from .user_info import UserInfo
from .request_parser_test import Test, Todo
from .life import LifeUserLogin, LifeUserSign

def create_api(app):
    api = Api(app)
    api.add_resource(UserInfo, '/user_info')
    api.add_resource(Test, '/')
    api.add_resource(Todo, '/todo')
    api.add_resource(LifeUserSign, '/life/sign')
    api.add_resource(LifeUserLogin, '/life/login')