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

class LifeSetting(Resource):
    """ 配置接口类 """

    parse = reqparse.RequestParser()
    parse.add_argument('session', type=str, location=['form','args'], help='')
    parse.add_argument('birthday', type=str, location='form', help='')
    parse.add_argument('age', type=int, location='form', help='')

    @marshal_with(RESPONSE)
    def get(self):
        args = self.parse.parse_args()
        session = args.get('session')
        if (not session) or (not LIFE_REDIS.conn.exists(session)):
            return {
                "code": 204,
                "msg": "session 不存在或已过期，请先登录！",
                "data": {}
            }
        setting = LIFE_REDIS.get_setting_by_session(session)
        return {
            "code": 100,
            "msg": "获取成功",
            "data": setting
        }

    @marshal_with(RESPONSE)
    def post(self):
        args = self.parse.parse_args()
        session = args.get('session')
        if (not session) or (not LIFE_REDIS.conn.exists(session)):
            return {
                "code": 204,
                "msg": "session 不存在或已过期，请先登录！",
                "data": {}
            }

        birthday = args.get('birthday')
        age = args.get('age') or 80
        if not birthday:
            return {
                "code": 107,
                "msg": "请上传生日字段！",
                "data": {}
            }

        life_time = LifeTime(birthday, age)
        LIFE_REDIS.add_setting(LIFE_REDIS.conn.get(session), life_time.data)
        return {
            "code": 100,
            "msg": "设置成功！",
            "data": life_time.data
        }
