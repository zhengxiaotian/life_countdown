# -*- coding=utf-8 -*-
"""
@FileName: request_parser_test.py
@Author: JunDay
@Date: 2019/6/17
@Doc describing: 
"""

from flask_restful import Resource, reqparse, fields, marshal_with
from flask import request


class Test(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rate', type=int, location='values', help='Rate to charge for this resource ')
    # parser.add_argument('name', type=str, required=True, help='Name cannot be blank!')
    parser.add_argument('name', type=str, dest='public_name', location='values')
    parser.add_argument('session_id', type=str, location='form')

    def post(self):
        print('test')
        print(request.headers)
        args = self.parser.parse_args()
        print('进入的参数：',args)
        response = {
            "code": 100,
            "message": "获取成功！",
            "session": args.get('session_id'),
            "data": {
                "rate": args.get('rate'),
                "name": args.get('public_name')
            }
        }
        return response, 201


resource_fields = {
    # 'name': fields.String(attribute='username'),
    'username': fields.List(fields.Raw),
    'address': fields.Integer,
    'data': {
        'code': fields.Integer,
        'msg': fields.String
    },
    'data_updated': fields.DateTime(dt_format='rfc822', default=20190912),
    'path': fields.Url('todo', absolute=True, scheme='https')
}

# resource_fields['data'] = {}
# resource_fields['data']['code'] = fields.Integer
# resource_fields['data']['msg'] = fields.String

class Todo(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, **kwargs):
        return {
            'username': [1,2,'3'],
            'address': '123',
            # 'data': {
            'code': 1008,
            'msg': 'request success!',
            # },
            'test': 'cen'
        }