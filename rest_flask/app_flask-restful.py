#!/usr/bin/python3

import json
from flask import Flask, request
from flask_restful import Resource, Api
from skills import Skills, ListSkills

class Developer(Resource):
    def get(self, idx):
        try:
            response = devs[idx]
        except IndexError:
            response = {'status': 1, 'message': 'Developer not registered'}
        return response

    def put(self, idx):
        data = json.loads(request.data)
        devs[idx] = data
        return data

    def delete(self, idx):
        try:
            devs.pop(idx)
            response = {'status': 0, 'message': 'Dev successfully deleted'}
        except IndexError:
            response = {'status': 1, 'message': 'Dev not registered'}
        return response

    
class ListDevs(Resource):
    def get(self):
        return devs

    def post(self):
        data = json.loads(request.data)
        devs.append(data)
        return {'status': 0, 'message': 'Dev successfully registered'}

devs = [
    {
        'name': 'Linus',
        'skills': ['linux', 'c', 'rust', 'git']
    },
    {
        'name': 'Guido',
        'skills': ['python', 'c', 'linux']
    }
]

app = Flask(__name__)
api = Api(app)

api.add_resource(ListDevs, '/dev', '/dev/')
api.add_resource(Developer, '/dev/<int:idx>', '/dev/<int:idx>/')
api.add_resource(ListSkills, '/skill', '/skill/')
api.add_resource(Skill, '/skill/<int:idx>', '/skill/<int:idx>/')

if __name__ == '__main__':
    app.run(debug=True)
    
