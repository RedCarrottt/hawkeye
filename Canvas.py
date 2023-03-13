# HawkEye
import drawSvg as DrawSVG
from SketchParser import Sketch, Node, FunctionNode, IterationNode, ForkNode, BranchNode
import utils

# Coordination system
# 1) Diagrams: LU (origin at left-up)
# 2) SVG: LD (origin at left-down)

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

    def render(self, canvas):
        rectanglePos = canvas.LUtoLD((self.left, self.bottom))
        rectangleElem = DrawSVG.Rectangle(
                rectanglePos[0], rectanglePos[1],
                self.width, self.height,
                fill='white', stroke_width=self.stroke_width, stroke='black')
        canvas.appendSVG(rectangleElem)

        textPos = canvas.LUtoLD((self.left + self.marginLeft,
                                 self.bottom - self.marginBottom))
        textElem = DrawSVG.Text(self.labelText, self.textSize,
                                textPos[0], textPos[1],
                                fill='black')
        canvas.appendSVG(textElem)

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

    def render(self, canvas):
        circlePos = canvas.LUtoLD((self.left, self.bottom))
        circleElem = DrawSVG.Circle(
                             circlePos[0], circlePos[1], self.radius,
                             fill='white', stroke_width=2, stroke='black')
        canvas.appendSVG(circleElem)

        textPos = canvas.LUtoLD((self.left + self.marginLeft,
                                 self.bottom - self.marginBottom))
        textElem = DrawSVG.Text(self.labelText, self.textSize,
                                textPos[0], textPos[1], fill='black')
        canvas.appendSVG(textElem)

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

    def render(self, canvas):
        diamondPos = ( 
            canvas.LUtoLD((self.left, self.bottom + 0.5 * self.radius)),
            canvas.LUtoLD((self.left + self.radius, self.bottom)),
            canvas.LUtoLD((self.left, self.bottom - 0.5 * self.radius)),
            canvas.LUtoLD((self.left - self.radius, self.bottom)),
        )
        diamondElem = DrawSVG.Lines(
            diamondPos[0][0], diamondPos[0][1],
            diamondPos[1][0], diamondPos[1][1],
            diamondPos[2][0], diamondPos[2][1],
            diamondPos[3][0], diamondPos[3][1],
            fill='white', stroke_width=self.stroke_width, stroke='black', close=True)
        canvas.appendSVG(diamondElem)

        textPos = canvas.LUtoLD(self.left + self.marginLeft,
                                self.bottom - self.marginBottom)
        textElem = DrawSVG.Text(self.labelText, self.textSize,
                                textPos[0], textPos[1],
                                fill='black')
        canvas.appendSVG(textElem)

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

    def render(self, canvas):
        arrow = DrawSVG.Marker(-0.1, -0.5, 0.9, 0.5, scale=self.scale, orient='auto')
        arrow.append(DrawSVG.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='black', close=True))

        pathPos = (
            canvas.LUtoLD(self.path[0:2]),
            canvas.LUtoLD(self.path[2:4]),
            canvas.LUtoLD((self.path[4] - self.scale*2, self.path[5]))
        )
        pathElem = DrawSVG.Path(stroke='black', stroke_width=2, fill='none', marker_end=arrow)
        pathElem.M(pathPos[0][0], pathPos[0][1]) \
                .L(pathPos[1][0], pathPos[1][1]) \
                .L(pathPos[2][0], pathPos[2][1])
        canvas.appendSVG(pathElem)

class Canvas:
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

    def draw(self, sketch, filename = None):
        diagrams = self.__layout(sketch)
        canvasElem = self.__render(diagrams)
        if filename is None:
            return canvasElem.asSvg()
        else:
            canvasElem.saveSvg(filename)
            return None

    def __addEndMargins(self):
        self.width += self.CANVAS_MARGIN_X * 2
        self.height += self.CANVAS_MARGIN_Y * 2

    def __layout(self, sketch):
        diagrams = self.__layoutNode(sketch, None)

        for diagram in diagrams:
            self.width = diagram.maxRight if diagram.maxRight > self.width else self.width
            self.height = diagram.maxTop if diagram.maxTop > self.height else self.height
        self.__addEndMargins()
        return diagrams

    def __layoutNode(self, node, parentDiagram):
        diagrams = []

        # Add diagram for the node
        nodeDiagram = None
        if not isinstance(node, Sketch):
            INDENT_WIDTH = 40
            ROW_HEIGHT = 45
            left = self.leftState + INDENT_WIDTH * self.indentState
            top = self.topState
            DIAGRAM_MARGIN_Y = 15
            if isinstance(node, BranchNode):
                nodeDiagram = Circle(node, left, top)
            elif isinstance(node, ForkNode):
                nodeDiagram = Diamond(node, left, top)
            else:
                nodeDiagram = Rectangle(node, left, top)
            diagrams.append(nodeDiagram)
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

    def __render(self, diagrams):
        # convert diagram to svgElement -> canvasElem.append(svgElement)
        self.canvasElem = DrawSVG.Drawing(self.width, self.height, displayInline=False)
        for diagram in diagrams:
            diagram.render(self)
        return self.canvasElem

    def appendSVG(self, child):
        self.canvasElem.append(child)

    def LUtoLD(self, pos):
        return (pos[0], self.height - pos[1])
