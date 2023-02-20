# HawkEye
import drawSvg as draw
from SketchParser import Sketch, Node, FunctionNode, IterationNode, ForkNode, BranchNode
import utils

DEBUG = False

class Diag:
    def __init__(self, diagType):
        self.type = diagType
        pass

class Rectangle(Diag):
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

class Circle(Diag):
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

class Diamond(Diag):
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

class Line(Diag):
    def __init__(self, parentDiag, nodeDiag):
        super().__init__('line')
        start_pos = None
        end_pos = None
        self.isAvailable = False

        if parentDiag.type in ['rectangle', 'circle', 'diamond']:
            start_pos = parentDiag.getStartLinePos()

        if nodeDiag.type in ['rectangle', 'circle', 'diamond']:
            end_pos = nodeDiag.getEndLinePos()

        if start_pos and end_pos:
            self.maxRight = start_pos[0] if start_pos[0] > end_pos[0] else end_pos[0]
            self.maxTop = start_pos[1] if start_pos[1] > end_pos[1] else end_pos[1]
            self.path = [start_pos[0], start_pos[1],
                         start_pos[0], end_pos[1],
                         end_pos[0], end_pos[1]]
            self.scale = 6
            self.isAvailable = True

def __layoutRecursively(node, layout, parentDiag):
    diags = []
    nodeDiag = None

    nodeDiagType = ''
    if isinstance(node, Sketch):
        pass
    elif isinstance(node, BranchNode):
        nodeDiagType = 'circle'
    elif isinstance(node, ForkNode):
        nodeDiagType = 'diamond'
    else:
        nodeDiagType = 'rectangle'

    # Add diagram for the node
    if nodeDiagType != '':
        INDENT_WIDTH = 40
        ROW_HEIGHT = 45
        left = layout.leftState + INDENT_WIDTH * layout.indentState
        top = layout.topState
        DIAGRAM_MARGIN_Y = 15
        if nodeDiagType == 'rectangle':
            nodeDiag = Rectangle(node, left, top)
            diags.append(nodeDiag)
        elif nodeDiagType == 'circle':
            nodeDiag = Circle(node, left, top)
            diags.append(nodeDiag)
        elif nodeDiagType == 'diamond':
            nodeDiag = Diamond(node, left, top)
            diags.append(nodeDiag)
        if nodeDiag != None:
            layout.topState = nodeDiag.bottom + DIAGRAM_MARGIN_Y

    # Add lines from the parent node to this node
    if parentDiag and nodeDiag:
        lineDiag = Line(parentDiag, nodeDiag)
        if lineDiag.isAvailable:
            diags.append(lineDiag)

    if node.children:
        parentDiag = nodeDiag if nodeDiag else parentDiag
        if not isinstance(node, Sketch):
            layout.indentState += 1
        for childNode in node.children:
            childDiags = __layoutRecursively(childNode, layout, parentDiag)
            diags += childDiags
        if not isinstance(node, Sketch):
            layout.indentState -= 1
    return diags

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

        self.diags = []

    def addEndMargins(self):
        self.width += self.CANVAS_MARGIN_X * 2
        self.height += self.CANVAS_MARGIN_Y * 2

def __layout(node):
    layout = Layout()
    layout.diags = __layoutRecursively(node, layout, None)

    for diag in layout.diags:
        layout.width = diag.maxRight if diag.maxRight > layout.width else layout.width
        layout.height = diag.maxTop if diag.maxTop > layout.height else layout.height
    layout.addEndMargins()

    return layout

def layout_and_draw(sketch, filename):
    # Layout
    layout = __layout(sketch)

    # Draw
    d = draw.Drawing(layout.width, layout.height, displayInline=False)
    
    for diag in layout.diags:
        if diag.type == 'rectangle':
            rect = draw.Rectangle(
                    diag.left, layout.height - diag.bottom,
                    diag.width, diag.height,
                    fill='white', stroke_width=diag.stroke_width, stroke='black')
            d.append(rect)

            textLeft = diag.left + diag.marginLeft
            textBottom = layout.height - diag.bottom + diag.marginBottom
            d.append(draw.Text(diag.labelText, diag.textSize, textLeft, textBottom, fill='black'))
        elif diag.type == 'line':
            arrow = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=diag.scale, orient='auto')
            arrow.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='black', close=True))
            path = draw.Path(stroke='black', stroke_width=2, fill='none', marker_end=arrow)
            path.M(diag.path[0], layout.height - diag.path[1]) \
                .L(diag.path[2], layout.height - diag.path[3]) \
                .L(diag.path[4] - diag.scale*2, layout.height - diag.path[5])
            d.append(path)
        elif diag.type == 'circle':
            circle = draw.Circle(diag.left, layout.height - diag.bottom, diag.radius,
                                 fill='white', stroke_width=2, stroke='black')
            d.append(circle)
            textLeft = diag.left + diag.marginLeft
            textBottom = layout.height - diag.bottom + diag.marginBottom
            d.append(draw.Text(diag.labelText, diag.textSize, textLeft, textBottom, fill='black'))
        elif diag.type == 'diamond':
            diamond = draw.Lines(diag.left, layout.height - (diag.bottom + 0.5 * diag.radius),
                diag.left + diag.radius, layout.height - diag.bottom,
                diag.left, layout.height - (diag.bottom - 0.5 * diag.radius),
                diag.left - diag.radius, layout.height - diag.bottom,
                fill='white', stroke_width=diag.stroke_width, stroke='black', close=True)
            d.append(diamond)
            textLeft = diag.left + diag.marginLeft
            textBottom = layout.height - diag.bottom + diag.marginBottom
            d.append(draw.Text(diag.labelText, diag.textSize, textLeft, textBottom, fill='black'))
    d.saveSvg(filename)
