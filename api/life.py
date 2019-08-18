# -*- coding=utf-8 -*-
"""
@FileName: life.py
@Author: JunDay
@Date: 2019/8/18
@Doc describing: 
"""

from common.life_time import LifeTime
from common.life_redis_setting import LifeRedis
from flask_restful import Api, Resource, reqparse, fields, marshal_with

LIFE_REDIS = LifeRedis()
RESPONSE = {
    "code": fields.Integer,
    "msg": fields.String,
    "data": fields.Raw
}

class LifeUserSign(Resource):
    """
    生命项目用户注册类
    """
    parse = reqparse.RequestParser()
    parse.add_argument('user_name', type=str, location='form', required=True, help='用户名是必需的！')
    parse.add_argument('pwd', type=str, location='form', required=True, help='密码是必需的！')

    @marshal_with(RESPONSE)
    def post(self):
        args = self.parse.parse_args()
        user_name = args.get('user_name')
        pwd = args.get('pwd')
        if not LIFE_REDIS.add_user(user_name, pwd):
            return {
                "code": 101,
                "msg": "该用户名已存在！",
                "data": {}
            }

        return {
            "code": 100,
            "msg": "注册成功，请进行登录",
            "data": {}
        }

class LifeUserLogin(Resource):
    """
    生命项目用户登录接口类
    """
    parse = reqparse.RequestParser()
    parse.add_argument('user_name', type=str, location='form', required=True, help='用户名是必需的！')
    parse.add_argument('pwd', type=str, location='form', required=True, help='密码是必需的！')

    @marshal_with(RESPONSE)
    def post(self):
        args = self.parse.parse_args()
        user_name = args.get('user_name')
        pwd = args.get('pwd')

        if not LIFE_REDIS.conn.hexists(LIFE_REDIS.user_db, user_name):
            return {
                "code": 106,
                "msg": "用户不存在！",
                "data": {}
            }

        if pwd != LIFE_REDIS.conn.hget(LIFE_REDIS.user_db, user_name):
            return {
                "code": 107,
                "msg": "密码错误！",
                "data": {}
            }

        session = LIFE_REDIS.generate_session(user_name)
        return {
            "code": 100,
            "msg": "登录成功！",
            "data": { "session": session }
        }

