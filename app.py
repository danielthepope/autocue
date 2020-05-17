import os
import random
import time

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

database_file = os.getenv('DATABASE', 'sqlite:///data/data.db')

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)


class Script(db.Model):
    script_id = db.Column(db.String(40), unique=True, nullable=False, primary_key=True)
    text = db.Column(db.String(1048576), nullable=False)
    created = db.Column(db.Integer())

    def __repr__(self):
        return f'Script(script_id="{self.script_id}", text="{self.text}", created="{self.created}")'


def new_id():
    chars = 'BCDFGHJKLMNPQRSTVWXYZ'

    def generate_id():
        return ''.join(random.choices(chars, k=5))

    return generate_id()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/script')
def view_script_by_param():
    script_id = request.args.get('id')
    return view_script(script_id.upper())


@app.route('/script/<script_id>')
def view_script(script_id):
    script = Script.query.get(script_id.upper())
    lines = script.text.split('\n')
    return render_template('autocue.html', script_id=script_id.upper(), text=lines)


@app.route('/script/', methods=['POST'])
def add_script():
    if request.form and 'text' in request.form:
        script_id = new_id()
        script = Script(script_id=script_id, text=request.form.get('text'), created=int(time.time()))
        db.session.add(script)
        db.session.commit()
    return redirect(f'/script/{script_id}')


@app.route('/script/<script_id>', methods=['POST'])
def update_script(script_id):
    if request.form and 'text' in request.form:
        script = Script.query.get(script_id)
        script.text = request.form.get('text')
        script.created = int(time.time())
        db.session.add(script)
        db.session.commit()
    return redirect(f'/script/{script_id}')


@app.route('/new-script')
def new_script():
    return render_template('editor.html')


@app.route('/edit-script/<script_id>')
def edit_script(script_id):
    script = Script.query.get(script_id)
    return render_template('editor.html', script_id=script_id, text=script.text)


if __name__ == '__main__':
    app.run(debug=True)
