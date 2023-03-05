from flask import Flask, request, send_from_directory
from flask_cors import CORS
import SketchParser
import DiagramDrawer

app = Flask(__name__)
CORS(app)

recent_svg = ""

@app.route('/sketcher', methods=['POST'])
def post_sketcher():
    text = request.json.get('text')
    sketch = SketchParser.parse(text)
    recent_svg = DiagramDrawer.layout_and_draw(sketch, "./results/results.svg")
    recent_svg_url = "http://localhost:3001/results/results.svg"
    return {"url": recent_svg_url}

@app.route('/results/<path:path>')
def get_results_file(path):
    return send_from_directory("results", path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
