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

@app.route('/to_png/<filename>', methods=['GET'])
def get_png_files(filename):
    global files_dir
    he_filepath = os.path.join(files_dir, filename)
    with open(he_filepath, 'r') as f:
        text = f.read()
    out_filename = filename
    if not out_filename.endswith('.png'):
        if not out_filename.endswith('.he'):
            out_filename += '.png'
        else:
            out_filename = out_filename.replace('.he', '.png')

    sketch = SketchParser.parse(text)
    out_filepath = os.path.join(files_dir, out_filename)
    Canvas().draw(sketch, out_filepath)
    return send_file(out_filepath)

@app.route('/to_svg/<filename>', methods=['GET'])
def get_svg_files(filename):
    global files_dir
    he_filepath = os.path.join(files_dir, filename)
    with open(he_filepath, 'r') as f:
        text = f.read()
    out_filename = filename
    if not out_filename.endswith('.svg'):
        if not out_filename.endswith('.he'):
            out_filename += '.svg'
        else:
            out_filename = out_filename.replace('.he', '.svg')

    sketch = SketchParser.parse(text)
    out_filepath = os.path.join(files_dir, out_filename)
    Canvas().draw(sketch, out_filepath)
    return send_file(out_filepath)

@app.route('/workspace', methods=['GET', 'POST'])
def get_workspace_files():
    global files_dir
    if request.method == 'GET':
        if not os.path.exists(files_dir):
            os.mkdir(files_dir)
        elif not os.path.isdir(files_dir):
            return {'isSuccess': False, 'files': [],
                'message': '{} is not a directory!'.format(files_dir)}
        files = os.listdir(files_dir)
        ret_files = []
        for file in files:
            if file.startswith('.') or not file.endswith('.he'):
                continue
            ret_files.append(file)
        return {'isSuccess': True, 'files': ret_files}
    elif request.method == 'POST':
        # Get the new file
        count = 0
        new_filename = None
        while True:
            if count == 0:
                new_filename = "new_file.he"
            else:
                new_filename = "new_file_{}.he".format(count)
            new_filepath = os.path.join(files_dir, new_filename)
            if not os.path.exists(new_filepath):
                break
            count += 1

        initial_code = "{}:\n    hello".format(new_filename)
        with open(new_filepath, 'w+') as f:
            f.write(initial_code)
        return {'isSuccess': True, 'filename': new_filename}

@app.route('/workspace/<filename>', methods=['GET', 'POST', 'DELETE'])
def do_workspace_file(filename):
    global files_dir
    if request.method == 'GET':
        filepath = os.path.join(files_dir, filename)
        return send_file(filepath)
    elif request.method == 'POST':
        try:
            filepath = os.path.join(files_dir, filename)
            with open(filepath, 'w') as f:
                f.write(request.json.get('text'))
            return {'isSuccess': True}
        except Exception as e:
            return {'isSuccess': False, 'message': str(e)}
    elif request.method == 'DELETE':
        try:
            filepath = os.path.join(files_dir, filename)
            if not os.path.exists(filepath):
                return {'isSuccess': False, 'message': "File {} does not exist".format(filename)}
            os.remove(filepath)
            return {'isSuccess': True}
        except Exception as e:
            return {'isSuccess': False, 'message': str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
