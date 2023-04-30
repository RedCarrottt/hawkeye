import HawkeyeCore as hc

with open('example_sketch.txt', 'r') as f:
    text = f.read()
sketch = hc.SketchCompiler().compile(text)
print(sketch)
