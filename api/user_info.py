# -*- coding=utf-8 -*-
"""
@FileName: user_info.py
@Author: JunDay
@Date: 2019/6/8
@Doc describing: 用户信息
"""

from flask_restful import Resource
from flask import request, Response
from common.life_time import LifeTime

class UserInfo(Resource):
    def get(self):
        args = request.args
        birthday = args['birthday']
        age = int(args['age'])
        life = LifeTime(birthday, age)
        response = {
            "code": 100,
            "message": "获取成功！",
            "data": life.data
        }
        return response