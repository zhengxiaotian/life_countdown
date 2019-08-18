# -*- coding=utf-8 -*-
"""
@FileName: life_redis_setting.py
@Author: JunDay
@Date: 2019/8/17
@Doc describing: 
"""

import redis
import random
import string

class LifeRedis(object):
    def __init__(self):
        self.conn = redis.Redis(db=1, decode_responses=True)
        self.user_db = "life_countdown:user_info:"
        self.setting_db = "life_countdown:user_setting:"

    def add_user(self, user_name, pwd):
        """
        添加用户的方法
        Args:
            user_name: 用户名
            pwd: 密码
        Returns:
            添加结果
        """
        if self.conn.hexists(self.user_db, user_name):
            return False
        else:
            self.conn.hset(self.user_db, user_name, pwd)
        return True

    def generate_session(self, user_name):
        """
        生成用户对应的 session
        Args:
            user_name: 用户名
        Returns:
            返回生成的 session key
        """
        session = user_name + '_' + ''.join(random.sample(string.ascii_uppercase, 16))
        self.conn.set(session, user_name)
        self.conn.expire(session, time=300)
        return session

    def add_setting(self, user_name, setting):
        """
        给指定用户添加配置信息
        Args:
            user_name: 用户名
            setting: 配置信息
        Returns:
            添加结果
        """
        self.conn.hmset(self.setting_db + user_name, setting)
        return True

    def get_life_setting(self, user_name):
        """
        通过用户名获取所有生命倒计时项目配置信息
        Args:
            user_name: 用户名
        Returns:
            生命倒计时项目配置信息
        """
        if not self.conn.exists(self.setting_db + user_name):
            return {}

        setting = self.conn.hgetall(self.setting_db + user_name)
        return setting

    def get_setting_by_session(self, session):
        """
        通过 session 获取用户配置信息
        Args:
            session: 登录下发的 session
        Returns:
            用户配置信息
        """
        if not self.conn.exists(session):
            return {}
        user_name = str(self.conn.get(session))
        setting = self.get_life_setting(user_name)
        return setting

# if __name__ == "__main__":
#     life = LifeRedis()
#     life.add_user('sky', 123456)
#     session = life.generate_session('sky')
#     life_setting = {
#         "birthday": "1994-03-12 12:00:00",
#         "age": 80
#     }
#     life.add_setting('sky', life_setting)
#     setting = life.get_setting_by_session(session)
#     print(setting)