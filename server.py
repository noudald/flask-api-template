from flask import Flask, request
from flask_restx import Resource, Api, fields

app = Flask(__name__)
api = Api(app)

# TODO: Rewrite, use List with {'task_id': 1, 'msg': 'Do the laundary'} instead.
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


ns_task = api.namespace('Task', descript='Task description')

model_task_put = api.model('Task', {
    'task_id': fields.Integer(
        default=1,
        title='Task identification number',
        description='Task unique identification number',
        required=True,
        example=1,
    ),
    'task': fields.String(
        default='Task message',
        title='Task message string',
        description='Task message',
        required=True,
        example='Do the laundry',
    ),
})

model_task_output = api.model('TaskOutput', {
    'task': fields.String(
        default='Task message',
        title='Task message string',
        description='Task message',
        required=True,
        example='Do the laundry',
    ),
})

@ns_task.route('/<int:task_id>')
@ns_task.response(404, 'Task not found')
@ns_task.param('task_id', 'Task unique identification number', example=1)
class Task(Resource):
    @ns_task.marshal_with(model_task_output)
    def get(self, task_id):
        '''Get a specific task'''
        if f'task{task_id}' not in TASKS:
            api.abort(404, f'Task id {task_id} does not exist')
        return TASKS[f'task{task_id}'], 200

    @ns_task.marshal_with(model_task_output)
    def delete(self, task_id):
        '''Delete a specific task'''
        if f'task{task_id}' not in TASKS:
            api.abort(404, f'Task id {task_id} does not exist')
        del TASKS[f'task{task_id}']
        return '', 204

    @ns_task.expect(model_task_put)
    @ns_task.marshal_with(model_task_output)
    def put(self, task_id):
        '''Update a specific task'''
        TASKS[f'task{task_id}'] = api.payload
        return TASKS[f'task{task_id}'], 201


ns_tasks = api.namespace('Tasks', descript='Tasks list')

model_tasks_output = api.model('Tasks', {
    'tasks': fields.List(fields.Nested(model_task_output))
})

@ns_tasks.route('/tasks')
class Tasks(Resource):
    @ns_tasks.marshal_with(model_tasks_output)
    def get(self):
        '''Get list of tasks'''
        return {'tasks': [task for _, task in TASKS.items()]}


if __name__ == '__main__':
    app.run(debug=True)
