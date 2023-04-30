import HawkeyeCore as hc

with open('examples/example_sketch.he', 'r') as f:
    text = f.read()
sketch = hc.SketchCompiler().compile(text)
print(sketch)
