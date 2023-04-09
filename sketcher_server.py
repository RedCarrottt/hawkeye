from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask.helpers import send_file
import os
import SketchParser
from Canvas import Canvas

app = Flask(__name__)
CORS(app)
files_dir = './workspace'

@app.route('/sketcher', methods=['POST'])
def post_sketcher():
    text = request.json.get('text')
    sketch = SketchParser.parse(text)
    svg = Canvas().draw(sketch)
    return {"svg": svg}

@app.route('/results/<path:path>')
def get_results_file(path):
    return send_from_directory("results", path)

@app.route('/workspace', methods=['GET'])
def get_workspace_files():
    global files_dir
    if not os.path.exists(files_dir):
        os.mkdir(files_dir)
    elif not os.path.isdir(files_dir):
        return {'isSuccess': False, 'files': [],
            'message': '{} is not a directory!'.format(files_dir)}
    files = os.listdir(files_dir)
    ret_files = []
    for file in files:
        if file.startswith('.'):
            continue
        ret_files.append(file)
    return {'isSuccess': True, 'files': ret_files}

@app.route('/workspace/<file_name>', methods=['GET'])
def get_workspace_file(file_name):
    global files_dir
    return send_file('{}/{}'.format(files_dir, file_name))

@app.route('/workspace/<file_name>', methods=['POST'])
def post_workspace_file(file_name):
    global files_dir
    try:
        with open('{}/{}'.format(files_dir, file_name), 'w') as f:
            f.write(request.json.get('text'))
        return {'isSuccess': True}
    except Exception as e:
        return {'isSuccess': False, 'message': str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
