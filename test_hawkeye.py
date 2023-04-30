# HawkEye
import HawkeyeCore as hc
#.SketchParser as SketchParser
#from HawkeyeCore.Canvas import Canvas

input_filename='example_sketch.txt'

output_filename=input_filename.replace(".txt", ".svg")
sketch = hc.SketchParser().read_and_parse(input_filename)
hc.Canvas().draw(sketch, output_filename)
print("Output: {}".format(output_filename))

output_filename=input_filename.replace(".txt", ".png")
sketch = hc.SketchParser().read_and_parse(input_filename)
ret = hc.Canvas().draw(sketch, output_filename)
print("Output: {} {}".format(ret, output_filename))
