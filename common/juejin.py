# -*- coding=utf-8 -*-
"""
@FileName: juejin.py
@Author: JunDay
@Date: 2019/7/6
@Doc describing: 掘金网相关操作
"""

import requests

class JueJin(object):
    """ 掘金网相关操作类 """

    def __init__(self, phone, pwd):
        self.phone_number = phone
        self.password = pwd
        self.user_info = self.login()

    def login(self):
        """ 登录方法 """
        url = "https://juejin.im/auth/type/phoneNumber"
        params = {
            "phoneNumber" : self.phone_number,
            "password" : self.password
        }

        res = requests.post(url, json=params, verify=False)
        if res.status_code == 200:
            return res.json()
        return {}

    @property
    def token(self):
        """ 获取登录后 token 的方法 """
        token = self.user_info.get('token')
        return token

    @property
    def client_id(self):
        """ 获取用户 clientId 的方法 """
        client_id = self.user_info.get('clientId')
        return client_id

    @property
    def user_id(self):
        """ 获取用户 userId 的方法 """
        user_id = self.user_info.get('userId')
        return user_id

    def search_tags(self, key='', amount=100):
        """
        根据关键字搜索标签的方法
        Args:
            key: 需要进行搜索的关键字，默认为空字符串，则搜索全部标签
            amount: 需要显示的最大数量
        Returns:
            搜索出来的全部结果字典
        """
        url = f"https://gold-tag-ms.juejin.im/v1/tag/type/new/search/{key}/page/1/pageSize/{amount}"
        headers = {
            "X-Juejin-Src": "web",
            "X-Juejin-Token": self.token,
            "X-Juejin-Uid": self.user_id
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        return {}

    def categories(self):
        """ 获取分类列表方法 """
        url = "https://gold-tag-ms.juejin.im/v1/categories"
        headers = {
            "X-Juejin-Src": "web",
            "X-Juejin-Token": self.token,
            "X-Juejin-Uid": self.user_id
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        return {}

    def create_draft(self, title, category, markdown='', html='', content='', type='markdown'):
        """
        新建草稿方法,
        todo: 暂时还没有加标签的功能，待添加
        Args:
            title: 文章标题
            category: 文章分类 ID
            markdown: markdown 文本内容，默认为空字符
            html: html 文本内容，默认为空字符
            content: 内容，默认为空字符
            type: 发布类型，默认为 markdown
        Returns:
            创建好的草稿 ID
        """
        url = "https://post-storage-api-ms.juejin.im/v1/draftStorage"
        params = {
            "uid" : self.user_id,
            "device_id" : self.client_id,
            "token" : self.token,
            "src" : "web",
            "category" : category,
            "content" : content,
            "html" : html,
            "markdown" : markdown,
            "screenshot" : "",
            "isTitleImageFullscreen" : "",
            "tags" : "",
            "title" : title,
            "type" : type
        }
        res = requests.post(url, data=params, verify=False)
        if res.status_code == 200:
            post_id = res.json().get('d')[0]
            return post_id
        else:
            raise Exception(f"文章创建失败，接口返回内容:{res.text}")


    def publish_draft(self, post_id):
        """
        发布草稿方法
        Args:
            post_id: 草稿 ID，由发布草稿接口返回
        Returns:

        """
        url = "https://post-storage-api-ms.juejin.im/v1/postPublish"
        params = {
            "uid" : self.user_id,
            "device_id" : self.client_id,
            "token" : self.token,
            "src" : "web",
            "postId" : post_id
        }
        res = requests.post(url, data=params, verify=False)
        if res.json().get('m') != r"文章已发布":
            raise Exception(f"文章发布失败，接口返回内容:{res.text}")


if __name__ == "__main__":
    juejin = JueJin('15302685753', 'Zheng654321')
    print(juejin.token)
    category = "5562b428e4b00c57d9b94b9d"
    post_id = juejin.create_draft('接口创建的文章', category)
    juejin.publish_draft(post_id)