from os import path

from flask import Flask
from flask_mongoengine import MongoEngine

# Initialize app with template path
cur_dir = path.dirname(path.realpath(__file__))
parent_dir = path.dirname(cur_dir)
template_path = path.join(path.dirname(parent_dir), 'client/build')

app = Flask(__name__, template_folder=template_path)

# Create database connection object
db = MongoEngine(app)