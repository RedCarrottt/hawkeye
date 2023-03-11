from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os
import SketchParser
from Canvas import Canvas

app = Flask(__name__)
CORS(app)
recent_svg_filename = ""
i = 0

@app.route('/sketcher', methods=['POST'])
def post_sketcher():
    text = request.json.get('text')
    sketch = SketchParser.parse(text)
    svg = Canvas().draw(sketch)
    return {"svg": svg}

@app.route('/results/<path:path>')
def get_results_file(path):
    return send_from_directory("results", path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
