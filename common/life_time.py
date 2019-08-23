# -*- coding=utf-8 -*-
"""
@FileName: life_time.py
@Author: JunDay
@Date: 2019/6/8
@Doc describing: 生活（生命））时间类
"""

import datetime


class LifeTime(object):
    def __init__(self, birthday, age=75):
        self.birthday = birthday
        self.birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d %H:%M:%S")
        end_day = ''.join([str(int(birthday[:4]) + age), birthday[4:]])
        self.end_day_date = datetime.datetime.strptime(end_day, "%Y-%m-%d %H:%M:%S")
        self.age = age

    @property
    def sum_times(self):
        """
        计算生命总时长的方法
        Returns: 生命总时间的对象

        """
        return self.end_day_date - self.birthday_date

    @property
    def remainder_times(self):
        return self.end_day_date - datetime.datetime.now()

    @property
    def used_times(self):
        return datetime.datetime.now() - self.birthday_date

    def set_birthday(self, birthday: str):
        self.birthday = birthday
        self.birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d %H:%M:%S")
        end_day = ''.join([str(int(birthday[:4]) + self.age), birthday[4:]])
        self.end_day_date = datetime.datetime.strptime(end_day, "%Y-%m-%d %H:%M:%S")

    def set_age(self, age: int):
        self.age = age
        end_day = ''.join([str(int(self.birthday[:4]) + self.age), self.birthday[4:]])
        self.end_day_date = datetime.datetime.strptime(end_day, "%Y-%m-%d %H:%M:%S")

    @property
    def data(self):
        return {
            "birthday": self.birthday,
            "age": self.age,
            "sum_days": self.sum_times.days,
            "remainder_days": self.remainder_times.days,
            "used_days": self.used_times.days,
            "end_day": datetime.datetime.strftime(self.end_day_date, "%Y-%m-%d %H:%M:%S")
        }
