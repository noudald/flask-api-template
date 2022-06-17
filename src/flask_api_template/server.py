'''A simple Flask API Template that can be used as a baseline for more advanced APIs.'''

from flask import Flask, request
from flask_restx import Resource, Api, fields

app = Flask(__name__)
api = Api(app)


TASKS = [
    {
        'task_id': 1,
        'user': 'Alice',
        'msg': 'This is task 1',
    },
    {
        'task_id': 2,
        'user': 'Bob',
        'msg': 'This is task 2',
    },
    {
        'task_id': 3,
        'user': 'Charlie',
        'msg': 'This is task 3',
    },
]


ns_task = api.namespace('Task', descript='Task description')

model_task_object = api.model('TaskObject', {
    'task_id': fields.Integer(
        title='Task identification number',
        description='Task identification number. Must be unique for task.',
        required=True,
        example=1
    ),
    'user': fields.String(
        title='User name',
        description='User assigned to specific task.',
        required=True,
        example='Dennis',
    ),
    'msg': fields.String(
        title='Task message',
        description='Task message describing what to do.',
        required=True,
        example='Do the laundry.'
    ),
})

model_task_message = api.model('TaskMessage', {
    'msg': fields.String(
        title='Task message',
        description='Message description if task has been performed.'
    ),
})

@ns_task.route('/<int:task_id>')
@ns_task.response(404, 'Task not found')
@ns_task.param('task_id', 'Task unique identification number', example=1)
class Task(Resource):
    @ns_task.marshal_with(model_task_object)
    def get(self, task_id):
        '''Get a specific task'''
        for task in TASKS:
            if task['task_id'] == task_id:
                return task, 200
        api.abort(404, f'Task id {task_id} does not exist')

    @ns_task.marshal_with(model_task_message)
    def delete(self, task_id):
        '''Delete a specific task'''
        for i, task in enumerate(TASKS):
            if task['task_id'] == task_id:
                del TASKS[i]
                return {'msg': f'Task with id {task_id} has been succesfully deleted.'}, 200
        api.abort(404, f'Task id {task_id} does not exist')

    @ns_task.expect(model_task_object)
    @ns_task.marshal_with(model_task_message)
    def put(self, task_id):
        '''Update a specific task'''
        for task in TASKS:
            if task['task_id'] == task_id:
                task = api.payload
                return {'msg': f'Task with id {task_id} has been succesfully updated.'}, 202

        TASKS.append(api.payload)
        return {'msg': f'New task with id {task_id} has been succesfully added.'}, 201


ns_tasks = api.namespace('Tasks', descript='Tasks list')

model_tasks_object = api.model('TasksObject', {
    'tasks': fields.List(
        fields.Nested(model_task_object),
        description='List of Tasks.'
    )
})

@ns_tasks.route('/tasks')
class Tasks(Resource):
    @ns_tasks.marshal_with(model_tasks_object)
    def get(self):
        '''Get list of tasks'''
        return {'tasks': TASKS}


if __name__ == '__main__':
    app.run(debug=True)
