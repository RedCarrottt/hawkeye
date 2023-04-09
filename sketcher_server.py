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

@app.route('/workspace/<file_name>', methods=['GET', 'POST', 'DELETE'])
def do_workspace_file(file_name):
    global files_dir
    if request.method == 'GET':
        filepath = '{}/{}'.format(files_dir, file_name)
        return send_file(filepath)
    elif request.method == 'POST':
        try:
            filepath = '{}/{}'.format(files_dir, file_name)
            with open(filepath, 'w') as f:
                f.write(request.json.get('text'))
            return {'isSuccess': True}
        except Exception as e:
            return {'isSuccess': False, 'message': str(e)}
    elif request.method == 'DELETE':
        try:
            filepath = '{}/{}'.format(files_dir, file_name)
            if not os.path.exists(filepath):
                return {'isSuccess': False, 'message': "File {} does not exist".format(file_name)}
            os.remove(filepath)
            return {'isSuccess': True}
        except Exception as e:
            return {'isSuccess': False, 'message': str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
