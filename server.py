from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TASKS = {
    'task1': {
        'task': 'This is task 1',
    },
    'task2': {
        'task': 'This is task 2',
    },
    'task3': {
        'task': 'This is task 3',
    },
}

parser = reqparse.RequestParser()
parser.add_argument('task')

class Task(Resource):
    def get(self, task_id):
        if f'task{task_id}' not in TASKS:
            abort(404, message=f'Task {task_id} does not exist')
        return TASKS[f'task{task_id}']

    def delete(self, task_id):
        if f'task{task_id}' not in TASKS:
            abort(404, message=f'Task {task_id} does not exist')
        del TASKS[f'task{task_id}']
        return '', 204

    def put(self, task_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TASKS[f'task{task_id}'] = task
        return task, 201

class Tasks(Resource):
    def get(self):
        return TASKS

api.add_resource(Tasks, '/tasks')
api.add_resource(Task, '/task/<task_id>')

if __name__ == '__main__':
    app.run(debug=True)
