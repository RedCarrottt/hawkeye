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

    def __makeFunctionNode(self, linenum, line):
        text = line.lstrip()
        hasChild = text[-1] == ':'
        text = text[:-1] if hasChild else text
        labelText = text
        newNode = FunctionNode(labelText)
        
        # check redirect
        if "=>" in line:
            if hasChild:
                raise self.__Exception(linenum, line, "Function with redirect cannot has children")
            elif not " => " in line:
                raise self.__Exception(linenum, line, "Redirect sign should be independent word")
            elif line.endswith(" => :") in line:
                raise self.__Exception(linenum, line, "Redirect label should be provided")
            labelTextEndIdx = text.find(" => ")
            newNode.labelText = text[:labelTextEndIdx].strip()
            redirectLabelTextStartIdx = labelTextEndIdx + len(" => ")
            newNode.redirectLabelText = text[redirectLabelTextStartIdx:].strip()

        return (newNode, hasChild)

    def __makeForkNode(self, linenum, line):
        text = line.lstrip()
        hasChild = text[-1] == ':'
        if not hasChild:
            raise self.__Exception(linenum, line, "It should have children")
        text = text[:-1]
        labelText = text
        newNode = ForkNode(labelText)
        
        # check redirect
        if "=>" in line:
            raise self.__Exception(linenum, line, "Invalid redirect sign")

        return newNode

    def __makeBranch(self, linenum, line):
        text = line.lstrip()
        hasChild = text[-1] == ':'
        if not hasChild:
            raise self.__Exception(linenum, line, "It should have children")
        text = text[:-1]
        labelText = text
        newNode = Branch(labelText)
        
        # check redirect
        if "=>" in line:
            raise self.__Exception(linenum, line, "Invalid redirect sign")

        return newNode

    def read(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            try:
                sketch = Sketch()
                nodeStack = [sketch]
                indentStack = [0]
                currentIndent = 0
                for idx, line in enumerate(lines):
                    linenum = idx + 1
                    line = line.rstrip()
                    indent = self.__getIndentCount(line)

                    topIndent = indentStack[-1]
                    topNode = nodeStack[-1]
                    # Check indent
                    if isinstance(topNode, Sketch):
                        if indent != currentIndent:
                            raise self.__Exception(linenum, line, "Invalid indent")
                    else:
                        if currentIndent == -1:
                            currentIndent = indent
                        elif indent < currentIndent:
                            # pop stacks
                            del nodeStack[-1]
                            del indentStack[-1]
                        elif indent > currentIndent:
                            raise self.__Exception(linenum, line, "Invalid indent")
                        indentStack.append(indent)
                    
                    topNode = nodeStack[-1]

                    # Check line
                    if isinstance(topNode, Sketch):
                        # Accept FunctionNode
                        if self.__StartsWith(line, ["if", "elif", "else", "for", "while"]):
                            raise self.__Exception(linenum, line, "Invalid keyword")
                        newNode, needPush = self.__makeFunctionNode(linenum, line)
                        topNode.roots.append(newNode)
                        if needPush:
                            nodeStack.append(newNode)
                            currentIndent = -1
                    else:
                        # in case of topNode in [FunctionNode, IterationNode, Branch]. ForkNode will not reach here
                        # Accept FunctionNode, IterationNode, ForkNode
                        if self.__StartsWith(line, ["elif", "else"]):
                            # TODO:
                            raise self.__Exception(linenum, line, "Invalid keyword")
                        if self.__StartsWith(line, ["if"]):
                            # ForkNode
                            newNode = self.__makeForkNode(linenum, line)
                            topNode.children.append(newNode)
                            nodeStack.append(newNode)

                            newNode = self.__MakeBranch(linenum, line)
                            topNode.children.append(newNode)
                            nodeStack.append(newNode)
                            currentIndent = -1
                            pass
                        elif self.__StartsWith(line, ["for", "while"]):
                            # TODO:
                            # IteraitonNode
                            pass
                        else:
                            # TODO:
                            # FunctionNode
                            newNode, needPush = self.__makeFunctionNode(linenum, line)
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
