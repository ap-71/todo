import os
from flask import Flask


app = Flask(__name__)
app.template_folder = 'templates'
app.secret_key = os.urandom(24)