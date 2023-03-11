# HawkEye
import drawSvg as DrawSVG
from SketchParser import Sketch, Node, FunctionNode, IterationNode, ForkNode, BranchNode
import utils

DEBUG = False

class Diagram:
    def __init__(self, diagType):
        self.type = diagType
        pass

class Rectangle(Diagram):
    def __init__(self, node, left, top):
        super().__init__('rectangle')
        MIN_WIDTH = 120
        HEIGHT = 30
        MARGIN = 10

        self.node = node
        self.textSize = 16
        self.labelText = node.labelText

        self.left  = left
        self.bottom = top + HEIGHT
        self.labelText = self.labelText if not DEBUG else \
            (self.labelText + " ({},{})".format(self.left, self.bottom))
        self.width = utils.textwidth(self.labelText, 16) + MARGIN
        self.width = self.width if self.width > MIN_WIDTH else MIN_WIDTH
        self.height = HEIGHT

        self.maxRight = self.left + self.width
        self.maxTop = self.bottom + self.height

        self.marginLeft = MARGIN
        self.marginBottom = MARGIN

        if isinstance(node, IterationNode) or isinstance(node, BranchNode):
            self.stroke_width = 4
        else:
            self.stroke_width = 2

    def getStartLinePos(self):
        X_RATIO = 0.1
        return (self.width * X_RATIO + self.left,
                self.bottom)

    def getEndLinePos(self):
        Y_RATIO = -0.5
        return (self.left,
                self.bottom + self.height * Y_RATIO)

    def draw(self, layout, canvasElem):
        rectangleElem = DrawSVG.Rectangle(
                self.left, layout.height - self.bottom,
                self.width, self.height,
                fill='white', stroke_width=self.stroke_width, stroke='black')
        canvasElem.append(rectangleElem)

        textLeft = self.left + self.marginLeft
        textBottom = layout.height - self.bottom + self.marginBottom
        textElem = DrawSVG.Text(self.labelText, self.textSize, textLeft, textBottom, fill='black')
        canvasElem.append(textElem)

class Circle(Diagram):
    def __init__(self, node, left, top):
        super().__init__('circle')
        RADIUS = 5
        MARGIN_LEFT = 15
        MARGIN_BOTTOM = -5

        self.node = node
        self.textSize = 16
        self.labelText = node.labelText

        self.left = left + RADIUS
        self.bottom = top + RADIUS
        self.radius = RADIUS
        self.labelText = self.labelText if not DEBUG else \
            (self.labelText + " ({},{},{})".format(self.left, self.bottom, self.radius))

        self.maxRight = self.left + self.radius
        self.maxTop = self.bottom + self.radius

        self.marginLeft = MARGIN_LEFT
        self.marginBottom = MARGIN_BOTTOM

    def getStartLinePos(self):
        X_RATIO = 0
        Y_RATIO = 1
        return (self.left + self.radius * X_RATIO,
                self.bottom + self.radius * Y_RATIO)

    def getEndLinePos(self):
        X_RATIO = -0.5
        Y_RATIO = 0
        return (self.left + self.radius * X_RATIO,
                self.bottom + self.radius * Y_RATIO)

    def draw(self, layout, canvasElem):
        circleElem = DrawSVG.Circle(self.left, layout.height - self.bottom, self.radius,
                             fill='white', stroke_width=2, stroke='black')
        canvasElem.append(circleElem)

        textLeft = self.left + self.marginLeft
        textBottom = layout.height - self.bottom + self.marginBottom
        textElem = DrawSVG.Text(self.labelText, self.textSize, textLeft, textBottom, fill='black')
        canvasElem.append(textElem)

class Diamond(Diagram):
    def __init__(self, node, left, top):
        super().__init__('diamond')
        RADIUS = 10
        MARGIN_LEFT = 15
        MARGIN_BOTTOM = -5

        self.node = node
        self.textSize = 16
        self.labelText = node.labelText

        self.left = left + RADIUS
        self.bottom = top + RADIUS
        self.radius = RADIUS
        self.labelText = self.labelText if not DEBUG else \
            (self.labelText + " ({},{},{})".format(self.left, self.bottom, self.radius))

        self.maxRight = self.left + self.radius
        self.maxTop = self.bottom + self.radius

        self.marginLeft = MARGIN_LEFT
        self.marginBottom = MARGIN_BOTTOM

        self.stroke_width = 2

    def getStartLinePos(self):
        X_RATIO = 0
        Y_RATIO = 0.5
        return (self.left + self.radius * X_RATIO,
                self.bottom + self.radius * Y_RATIO)

    def getEndLinePos(self):
        X_RATIO = -0.7
        Y_RATIO = 0
        return (self.left + self.radius * X_RATIO,
                self.bottom + self.radius * Y_RATIO)

    def draw(self, layout, canvasElem):
        diamondElem = DrawSVG.Lines(self.left, layout.height - (self.bottom + 0.5 * self.radius),
            self.left + self.radius, layout.height - self.bottom,
            self.left, layout.height - (self.bottom - 0.5 * self.radius),
            self.left - self.radius, layout.height - self.bottom,
            fill='white', stroke_width=self.stroke_width, stroke='black', close=True)
        canvasElem.append(diamondElem)

        textLeft = self.left + self.marginLeft
        textBottom = layout.height - self.bottom + self.marginBottom
        textElem = DrawSVG.Text(self.labelText, self.textSize, textLeft, textBottom, fill='black')
        canvasElem.append(textElem)

class Line(Diagram):
    def __init__(self, parentDiagram, nodeDiagram):
        super().__init__('line')
        start_pos = None
        end_pos = None
        self.isAvailable = False

        if parentDiagram.type in ['rectangle', 'circle', 'diamond']:
            start_pos = parentDiagram.getStartLinePos()

        if nodeDiagram.type in ['rectangle', 'circle', 'diamond']:
            end_pos = nodeDiagram.getEndLinePos()

        if start_pos and end_pos:
            self.maxRight = start_pos[0] if start_pos[0] > end_pos[0] else end_pos[0]
            self.maxTop = start_pos[1] if start_pos[1] > end_pos[1] else end_pos[1]
            self.path = [start_pos[0], start_pos[1],
                         start_pos[0], end_pos[1],
                         end_pos[0], end_pos[1]]
            self.scale = 6
            self.isAvailable = True

    def draw(self, layout, canvasElem):
        arrow = DrawSVG.Marker(-0.1, -0.5, 0.9, 0.5, scale=self.scale, orient='auto')
        arrow.append(DrawSVG.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='black', close=True))
        pathElem = DrawSVG.Path(stroke='black', stroke_width=2, fill='none', marker_end=arrow)
        pathElem.M(self.path[0], layout.height - self.path[1]) \
                .L(self.path[2], layout.height - self.path[3]) \
                .L(self.path[4] - self.scale*2, layout.height - self.path[5])
        canvasElem.append(pathElem)

class Layout:
    def __init__(self):
        self.INITIAL_WIDTH = 100
        self.INITIAL_HEIGHT = 100
        self.CANVAS_MARGIN_X = 10
        self.CANVAS_MARGIN_Y = 10

        self.width = self.INITIAL_WIDTH
        self.height = self.INITIAL_HEIGHT

        self.leftState = self.CANVAS_MARGIN_X
        self.topState = self.CANVAS_MARGIN_Y
        self.indentState = 0

        self.diagrams = []

    def addEndMargins(self):
        self.width += self.CANVAS_MARGIN_X * 2
        self.height += self.CANVAS_MARGIN_Y * 2

    def layout(self, sketch):
        self.diagrams = self.__layoutNode(sketch, None)

        for diagram in self.diagrams:
            self.width = diagram.maxRight if diagram.maxRight > self.width else self.width
            self.height = diagram.maxTop if diagram.maxTop > self.height else self.height
        self.addEndMargins()
        return self

    def __layoutNode(self, node, parentDiagram):
        diagrams = []
        nodeDiagram = None

        nodeDiagramType = ''
        if isinstance(node, Sketch):
            pass
        elif isinstance(node, BranchNode):
            nodeDiagramType = 'circle'
        elif isinstance(node, ForkNode):
            nodeDiagramType = 'diamond'
        else:
            nodeDiagramType = 'rectangle'

        # Add diagram for the node
        if nodeDiagramType != '':
            INDENT_WIDTH = 40
            ROW_HEIGHT = 45
            left = self.leftState + INDENT_WIDTH * self.indentState
            top = self.topState
            DIAGRAM_MARGIN_Y = 15
            if nodeDiagramType == 'rectangle':
                nodeDiagram = Rectangle(node, left, top)
                diagrams.append(nodeDiagram)
            elif nodeDiagramType == 'circle':
                nodeDiagram = Circle(node, left, top)
                diagrams.append(nodeDiagram)
            elif nodeDiagramType == 'diamond':
                nodeDiagram = Diamond(node, left, top)
                diagrams.append(nodeDiagram)
            if nodeDiagram != None:
                self.topState = nodeDiagram.bottom + DIAGRAM_MARGIN_Y

        # Add lines from the parent node to this node
        if parentDiagram and nodeDiagram:
            lineDiag = Line(parentDiagram, nodeDiagram)
            if lineDiag.isAvailable:
                diagrams.append(lineDiag)

        if node.children:
            parentDiagram = nodeDiagram if nodeDiagram else parentDiagram
            if not isinstance(node, Sketch):
                self.indentState += 1
            for childNode in node.children:
                childDiags = self.__layoutNode(childNode, parentDiagram)
                diagrams += childDiags
            if not isinstance(node, Sketch):
                self.indentState -= 1
        return diagrams

    def draw(self):
        # convert diagram to svgElement -> canvasElem.append(svgElement)
        self.canvasElem = DrawSVG.Drawing(self.width, self.height, displayInline=False)
        for diagram in self.diagrams:
            diagram.draw(self, canvasElem)
        return canvasElem

def layout_and_draw(sketch, filename=None):
    layout = Layout()
    layout.layout(sketch)
    canvasElem = layout.draw()
    if filename is None:
        return canvasElem.asSvg()
    else:
        canvasElem.saveSvg(filename)
