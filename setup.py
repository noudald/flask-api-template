from pathlib import Path
from setuptools import setup, find_packages

DESCRIPTION = 'Flask API Template'
APP_ROOT = Path(__file__).parent
AUTHOR = 'Noud Aldenhoven'
AUTHOR_EMAIL = 'noud.aldenhoven@gmail.com'
INSTALL_REQUIRES = [
    'Flask',
    'Flask-Bcrypt',
    'Flask-Cors',
    'Flask-Migrate',
    'Flask-SQLAlchemy',
    'flask-restx',
    'python-dotenv',
    'PyJWT',
    'python-dateutil',
]
EXTRAS_REQUIRE = {
    'dev': [
        'pytest',
        'pytest-flake8',
        'pytest-flask',
        'tox',
    ]
}

setup(
    name="flask-api-template",
    description=DESCRIPTION,
    version="0.1",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="MIT",
    url='https://github.com/noudald/flask-api-template',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)
