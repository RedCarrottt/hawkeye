# HwakEye
import drawSvg as draw
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer

# * Sketch
#   - arr<FunctionNode> roots
# * Node
#   - str labelText
# * FunctionNode : Node
#   - arr<Node> children
# * SeriesNode : Node
#   - arr<Node> children
# * IterationNode : Node
#   - arr<Node> children
# * ForkNode : Node
#   - arr<Branch> branches
# * Branch
#   - str labelText
#   - Node node
# * RedirectNode : Node
#   - str targetLabelText
class Sketch:
    pass

# Sketch Reader
class SketchReader:
    def __init__(self):
        pass

# Diagram Drawer
class DiagramDrawer:
    def __init__(self, filename):
        self.filename = filename

    def calculate(self):
        pass

    def draw(self):
        d = draw.Drawing(1024, 768, origin='center', displayInline=False)
        
        r = draw.Rectangle(-80, 0, 150, 50, fill='white', stroke_width=2, stroke='black')
        d.append(r)
        d.append(draw.Text('node_reclaim', 16, -70, 10, fill='black'))
        
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

sr = SketchReader()
filename='diagram.svg'
dd = DiagramDrawer(filename)
dd.calculate()
dd.draw()
dv = DiagramViewer('HawkEye', filename)
dv.show()
