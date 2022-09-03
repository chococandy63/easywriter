#!/usr/bin/env python
# encoding: utf-8
import string
import random
import os
from flask import Flask, send_from_directory, request, render_template
app = Flask(__name__, static_folder="static/")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/read/<id>')
def load_file(id):
    return render_template('index.html', message=open(f"./uploads/{id}", 'r').read())


@app.route('/render', methods=['POST'])
def render_md_to_pdf():
    num = random.random()
    md_data = request.data.decode('ascii')
    with open(f"/tmp/{num}.md", 'w') as f:
        f.write(md_data)

    os.system(f"/usr/bin/pandoc -o /tmp/{num}.pdf /tmp/{num}.md")
    return send_from_directory('/', f"tmp/{num}.pdf")


@app.route('/upload', methods=['POST'])
def upload():
    filename = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=4))
    with open(f"./uploads/{filename}", 'w') as f:
        f.write(request.data.decode('ascii'))

    return f"http://app.snehit.dev/read/{filename}"



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
