import os

import click

from flask_api_template import create_app, db
from flask_api_template.models.token_blacklist import BlacklistedToken
from flask_api_template.models.user import User
from flask_api_template.models.widget import Widget

app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.cli.command('add-user', short_help='Add a new user')
@click.argument('email')
@click.option(
    '--admin',
    is_flag=True,
    default=False,
    help='Add administrator rights to new user'
)
@click.password_option(help='Do not set password on the command line!')
def add_user(email, admin, password):
    if User.find_by_email(email):
        error = f'Error: {email} has already been taken'
        click.secho(f'{error}\n', fg='red', bold=True)
        return 1

    new_user = User(email=email, password=password, admin=admin)
    db.session.add(new_user)
    db.session.commit()

    user_type = 'admin user' if admin else 'user'
    message = f'Successfully added new {user_type}: {new_user}'
    click.secho(message, fg='blue', bold=True)

    return 0


@app.shell_context_processor
def shell():
    return {
        'db': db,
        'User': User,
        'Widget': Widget,
        'BlacklistedToken': BlacklistedToken
    }
