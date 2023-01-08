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
#   - srt redirectLabelText
# * IterationNode : Node
#   - arr<Node> children
# * ForkNode : Node
#   - arr<Branch> branches
# * Branch
#   - str labelText
#   - arr<Node> children

class Sketch:
    def __init__(self):
        self.roots = []
        pass

class Node:
    def __init__(self, labelText):
        self.labelText = labelText;

class FunctionNode(Node):
    def __init__(self, labelText):
        __super__().__init__(labelText)
        self.children = []
        self.redirectLabelText = ''

class IterationNode(Node):
    def __init__(self, labelText):
        __super__().__init__(labelText)
        self.children = []

class ForkNode(Node):
    def __init__(self, labelText):
        __super__().__init__(labelText)
        self.branches = []

class Branch:
    def __init__(self, labelText):
        self.labelText = labelText
        self.children = []

# Sketch Reader
class SketchReader:
    def __init__(self):
        pass
    def __getIndentCount(self, line):
        indentCount = 0
        i = 0
        while i < len(line) and (line[i] == ' ' or line[i] == '\t'):
            if line[i] == ' ':
                indentCount += 1
            elif line[i] == '\t':
                indentCount += 4
            i += 1
        return indentCount
    def __Exception(self, linenum, line, message):
        return Exception("Line {}: {}\n=> {}".format(linenum, message, line))
    def __StartsWith(self, line, keywords):
        for keyword in keywords:
            if line.stratswith(keyword + " "):
                return True
        return False
    def read(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            try:
                sketch = Sketch()
                stack = [sketch]
                expectedIndentCount = 0
                for idx, line in enumerate(lines):
                    linenum = idx + 1
                    line = line.rstrip()
                    indentCount = self.__getIndentCount(line)
                    if indentCount != expectedIndentCount:
                        raise self.__Exception(linenum, line, "Unexpected indent")

                    if isinstance(stack[-1], Sketch):
                        # Accept FunctionNode
                        if self.__StartsWith(line, ["if", "elif", "else", "for", "while"]):
                            raise self.__Exception(linenum, line, "Invalid keyword")
                        elif line[-1] != ":":
                            raise self.__Exception(linenum, line, "Invalid function")
                        labelText = line.lstrip()[:-1]
                        newNode = FunctionNode(labelText)
                        stack[-1].roots.append(newNode)
                        stack.append(newNode)
                    elif isinstance(stack[-1], FunctionNode):
                        # Accept FunctionNode, IterationNode, ForkNode
                        if self.__StartsWith(line, ["elif", "else"]):
                            raise self.__Exception(linenum, line, "Invalid keyword")
                        elif self.__StartsWith(line, ["if"]):
                            # ForkNode
                            pass
                        elif self.__StartsWith(line, ["for", "while"]):
                            # IteraitonNode
                            pass
                        else:
                            # FunctionNode
                            pass
                        pass # TODO:
                    elif isinstance(stack[-1], IterationNode):
                        # Accept FunctionNode, IterationNode, ForkNode
                        pass
                    elif isinstance(stack[-1], ForkNode):
                        # Accept Branch
                        pass
                    elif isinstance(stack[-1], Branch):
                        # Accept FunctionNode, IterationNode, ForkNode
                        pass
            except Exception as e:
                print(e)
                return False
        return True

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
