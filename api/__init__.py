# -*- coding=utf-8 -*-
"""
@FileName: __init__.py.py
@Author: JunDay
@Date: 2019/6/8
@Doc describing: 
"""

from flask_restful import Api
from .user_info import UserInfo

def create_api(app):
    api = Api(app)
    api.add_resource(UserInfo, '/user_info')