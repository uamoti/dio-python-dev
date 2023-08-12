#!/usr/bin/python3

import json
from flask_restful import Resource
from flask import request

class Skill(Resource):
    def get(self, idx):
        try:
            response = skillist[idx]
        except IndexError:
            response = {'status': 1, 'message': 'Skill not registered'}
        return response

    def put(self, idx):
        try:
            data = json.loads(request.data)
            skillist[idx] = data
            return data
        except IndexError:
            return {'status': 1, 'message': 'Skill not registered'}

    def delete(self, idx):
        try:
            skillist.pop(idx)
            response = {'status': 0, 'message': 'Skill successfully deleted'}
        except IndexError:
            response = {'status': 1, 'message': 'Skill not registered'}
        return response

        
class ListSkills(Resource):
    def get(self):
        return skillist

    def post(self):
        data = request.data
        skillist.append(data)
        return {'status': 0, 'message': 'Skill successfully registered'}


skillist = ['linux', 'c', 'python', 'git', 'rust']
