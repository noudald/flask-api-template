import os

from flask_api_template import create_app, db

app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def shell():
    return {'db': db}
