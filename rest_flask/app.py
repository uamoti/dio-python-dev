#!/usr/bin/python3

import json
from flask import Flask, jsonify, request

tasks = [
    {
        'id': 0,
        'person': 'John',
        'task': 'Do the dishes',
        'completed': True
    },
    {
        'id': 1,
        'person': 'Mary',
        'task': 'Groceries',
        'completed': False
    }
]

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def task_list():
    if request.method == 'GET':
        return jsonify(tasks)
    else:
        task = json.loads(request.data)
        tasks.append(task)
        return jsonify({'status': 0, 'message': 'Task added sucessfully!'})

@app.route('/<int:idx>', methods=['GET'])
def get_task(idx):
    return jsonify(tasks[idx])

@app.route('/<int:idx>', methods=['PUT'])
def update_task(idx):
    tasks[idx]['completed'] = not tasks[idx]['completed']
    return jsonify({'status': 0, 'message': f'Task {idx} sucessfully updated!'})

if __name__ == '__main__':
    app.run(debug=True)
    
