# HawkEye
import HawkeyeCore as hc
#.SketchCompiler as SketchCompiler
#from HawkeyeCore.Canvas import Canvas

input_filename='example/example_sketch.he'

output_filename=input_filename.replace(".he", ".svg")
with open(input_filename, 'r') as f:
    text = f.read()
sketch = hc.SketchCompiler().compile(text)
hc.Canvas().draw(sketch, output_filename)
print("Output: {}".format(output_filename))

output_filename=input_filename.replace(".he", ".png")
with open(input_filename, 'r') as f:
    text = f.read()
sketch = hc.SketchCompiler().compile(text)
hc.Canvas().draw(sketch, output_filename)
print("Output: {}".format(output_filename))
