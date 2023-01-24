# HawkEye
import drawSvg as draw
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
import SketchParser as sp
from SketchParser import Sketch, Node, FunctionNode, IterationNode, ForkNode, BranchNode

# Diagram Drawer
class DiagramDrawer:
    def __init__(self, filename):
        self.filename = filename

    def __layout(self, node, state):
        diags = []
        newDiag = {}

        MIN_WIDTH = 150
        MIN_HEIGHT = 30
        INDENT_WIDTH = 20
        ROW_HEIGHT = MIN_HEIGHT + 15
        MARGIN = 10

        if not isinstance(node, Sketch) and not isinstance(node, ForkNode):
            bottom = state['bottom'] - ROW_HEIGHT
            state['bottom'] = bottom
            left = state['left'] + INDENT_WIDTH * node.indent
            
            newDiag = {
                'type': 'rectangle',
                'pos': [left, bottom, MIN_WIDTH, MIN_HEIGHT],
                'margin': [MARGIN, MARGIN],
                'textSize': 16,
                'labelText': node.labelText
            }
            diags.append(newDiag)

        if node.children:
            for childNode in node.children:
                diags += self.__layout(childNode, state)
        return diags

    def layout(self, node):
        WIDTH = 1024
        HEIGHT = 768
        state = {'width': WIDTH, 'height': HEIGHT, 'left': 0, 'bottom': HEIGHT}

        diags = self.__layout(node, state)
        layout = {'width': WIDTH, 'height': HEIGHT, 'diags': diags}
        return layout

    def layout_and_draw(self, sketch):
        # Layout
        layout = self.layout(sketch)

        # Draw
        d = draw.Drawing(layout['width'], layout['height'], displayInline=False)
        
        for diag in layout['diags']:
            print(diag['pos'])
            r = draw.Rectangle(diag['pos'][0], diag['pos'][1], diag['pos'][2], diag['pos'][3],
                fill='white', stroke_width=2, stroke='black')
            d.append(r)

            textLeft = diag['pos'][0] + diag['margin'][0]
            textBottom = diag['pos'][1] + diag['margin'][1]
            d.append(draw.Text(diag['labelText'], diag['textSize'], textLeft, textBottom, fill='black'))
        d.saveSvg(self.filename)

class DiagramViewerWidget(QWidget):
    def __init__(self, windowTitle, filename):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle(windowTitle)
        self.setGeometry(100,100,1024,768)

        svgWidget = QSvgWidget()
        svgWidget.renderer().load(filename)

        vbox = QVBoxLayout()
        vbox.addWidget(svgWidget)
        self.setLayout(vbox)

# Diagram Viewer
class DiagramViewer():
    def __init__(self, windowTitle, filename):
        self.app = QApplication(sys.argv)
        self.windowTitle = windowTitle
        self.filename = filename

    def show(self):
        widget = DiagramViewerWidget(self.windowTitle, self.filename)
        widget.show()
        sys.exit(self.app.exec_())

input_filename='example_sketch.txt'

output_filename=input_filename.replace(".txt", ".svg")
sketch = sp.read_and_parse(input_filename)
dd = DiagramDrawer(output_filename)
dd.layout_and_draw(sketch)
dv = DiagramViewer('HawkEye', output_filename)
dv.show()
