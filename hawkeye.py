# HawkEye
import SketchParser
import DiagramDrawer

input_filename='example_sketch.txt'

output_filename=input_filename.replace(".txt", ".svg")
sketch = SketchParser.read_and_parse(input_filename)
DiagramDrawer.layout_and_draw(sketch, output_filename)
print("Output: {}".format(output_filename))
