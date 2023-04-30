# HawkEye
import HawkeyeCore as hc
#.SketchCompiler as SketchCompiler
#from HawkeyeCore.Canvas import Canvas

input_filename='example_sketch.txt'

output_filename=input_filename.replace(".txt", ".svg")
with open(input_filename, 'r') as f:
    text = f.read()
sketch = hc.SketchCompiler().compile(text)
hc.Canvas().draw(sketch, output_filename)
print("Output: {}".format(output_filename))

output_filename=input_filename.replace(".txt", ".png")
with open(input_filename, 'r') as f:
    text = f.read()
sketch = hc.SketchCompiler().compile(text)
hc.Canvas().draw(sketch, output_filename)
print("Output: {}".format(output_filename))
