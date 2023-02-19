# HawkEye
import drawSvg as draw
from SketchParser import Sketch, Node, FunctionNode, IterationNode, ForkNode, BranchNode
import utils

DEBUG = False
MIN_HEIGHT = 30

class Diag:
    def __init__(self, diagType):
        self.type = diagType
        pass

class Rectangle(Diag):
    def __init__(self, node, left, bottom):
        super().__init__('rectangle')
        MIN_WIDTH = 120
        MARGIN = 10

        self.node = node
        self.textSize = 16
        self.labelText = node.labelText

        self.left  = left
        self.bottom = bottom
        self.labelText = self.labelText if not DEBUG else \
            (self.labelText + " ({},{})".format(self.left, self.bottom))
        self.width = utils.textwidth(self.labelText, 16) + MARGIN
        self.width = self.width if self.width > MIN_WIDTH else MIN_WIDTH
        self.height = MIN_HEIGHT

        self.maxRight = self.left + self.width
        self.maxTop = self.bottom + self.height

        self.marginLeft = MARGIN
        self.marginBottom = MARGIN

        if isinstance(node, IterationNode) or isinstance(node, BranchNode):
            self.stroke_width = 4
        else:
            self.stroke_width = 2

class Line(Diag):
    def __init__(self, parentDiag, nodeDiag):
        super().__init__('line')
        start_pos = None
        end_pos = None
        self.isAvailable = False

        if parentDiag.type == 'rectangle':
            start_pos = self.__fromRectangle(parentDiag)
        elif parentDiag.type == 'circle':
            start_pos = self.__fromCircle(parentDiag)

        if nodeDiag.type == 'rectangle':
            end_pos = self.__toRectangle(nodeDiag)
        elif nodeDiag.type == 'circle':
            end_pos = self.__toCircle(nodeDiag)

        if start_pos and end_pos:
            self.maxRight = start_pos[0] if start_pos[0] > end_pos[0] else end_pos[0]
            self.maxTop = start_pos[1] if start_pos[1] > end_pos[1] else end_pos[1]
            self.path = [start_pos[0], start_pos[1],
                         start_pos[0], end_pos[1],
                         end_pos[0], end_pos[1]]
            self.scale = 6
            self.isAvailable = True

    def __fromRectangle(self, parentDiag):
        X_RATIO = 0.1
        return (parentDiag.width * X_RATIO + parentDiag.left,
                parentDiag.bottom)

    def __toRectangle(self, nodeDiag):
        Y_RATIO = -0.5
        return (nodeDiag.left,
                nodeDiag.bottom + nodeDiag.height * Y_RATIO)

    def __fromCircle(self, parentDiag):
        X_RATIO = 0
        Y_RATIO = 1
        return (parentDiag.left + parentDiag.radius * X_RATIO,
                parentDiag.bottom + parentDiag.radius * Y_RATIO)

    def __toCircle(self, nodeDiag):
        X_RATIO = -0.5
        Y_RATIO = 0
        return (nodeDiag.left + nodeDiag.radius * X_RATIO,
                nodeDiag.bottom + nodeDiag.radius * Y_RATIO)

class Circle(Diag):
    def __init__(self, node, left, bottom):
        super().__init__('circle')
        RADIUS = 5
        MARGIN_LEFT = 15
        MARGIN_BOTTOM = -5

        self.node = node
        self.textSize = 16
        self.labelText = node.labelText

        self.left = left + RADIUS
        self.bottom = bottom + RADIUS
        self.radius = RADIUS
        self.labelText = self.labelText if not DEBUG else \
            (self.labelText + " ({},{},{})".format(self.left, self.bottom, self.radius))

        self.maxRight = self.left + self.radius
        self.maxTop = self.bottom + self.radius

        self.marginLeft = MARGIN_LEFT
        self.marginBottom = MARGIN_BOTTOM

def __layoutRecursively(node, layoutState, parentDiag):
    diags = []
    nodeDiag = None

    nodeDiagType = ''
    if isinstance(node, Sketch) or isinstance(node, ForkNode):
        pass
    elif isinstance(node, BranchNode):
        nodeDiagType = 'circle'
    else:
        nodeDiagType = 'rectangle'

    # Add diagram for the node
    if nodeDiagType != '':
        INDENT_WIDTH = 40
        ROW_HEIGHT = MIN_HEIGHT + 15
        left = layoutState['left'] + INDENT_WIDTH * layoutState['indent']
        bottom = layoutState['bottom'] + ROW_HEIGHT
        if nodeDiagType == 'rectangle':
            nodeDiag = Rectangle(node, left, bottom)
            diags.append(nodeDiag)
        elif nodeDiagType == 'circle':
            nodeDiag = Circle(node, left, bottom)
            diags.append(nodeDiag)
        layoutState['bottom'] = bottom

    # Add lines from the parent node to this node
    if parentDiag and nodeDiag:
        lineDiag = Line(parentDiag, nodeDiag)
        if lineDiag.isAvailable:
            diags.append(lineDiag)

    if node.children:
        parentDiag = nodeDiag if nodeDiag else parentDiag
        if not isinstance(node, Sketch):
            layoutState['indent'] += 1
        for childNode in node.children:
            childDiags = __layoutRecursively(childNode, layoutState, parentDiag)
            diags += childDiags
        if not isinstance(node, Sketch):
            layoutState['indent'] -= 1
    return diags

def __layout(node):
    WIDTH = 100
    HEIGHT = 100
    CANVAS_MARGIN_X = 10
    CANVAS_MARGIN_Y = 10
    layoutState = {'width': WIDTH, 'height': HEIGHT,
                   'left': CANVAS_MARGIN_X, 'bottom': CANVAS_MARGIN_Y,
                   'indent': 0}

    diags = __layoutRecursively(node, layoutState, None)

    for diag in diags:
        layoutState['width'] = diag.maxRight if diag.maxRight > layoutState['width'] else layoutState['width']
        layoutState['height'] = diag.maxTop if diag.maxTop > layoutState['height'] else layoutState['height']
    layoutState['width'] += CANVAS_MARGIN_X * 2
    layoutState['height'] += CANVAS_MARGIN_Y * 2

    layout = {'width': layoutState['width'], 'height': layoutState['height'], 'diags': diags}
    return layout

def layout_and_draw(sketch, filename):
    # Layout
    layout = __layout(sketch)

    # Draw
    d = draw.Drawing(layout['width'], layout['height'], displayInline=False)
    
    for diag in layout['diags']:
        if diag.type == 'rectangle':
            rect = draw.Rectangle(
                    diag.left, layout['height'] - diag.bottom,
                    diag.width, diag.height,
                    fill='white', stroke_width=diag.stroke_width, stroke='black')
            d.append(rect)

            textLeft = diag.left + diag.marginLeft
            textBottom = layout['height'] - diag.bottom + diag.marginBottom
            d.append(draw.Text(diag.labelText, diag.textSize, textLeft, textBottom, fill='black'))
        elif diag.type == 'line':
            arrow = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=diag.scale, orient='auto')
            arrow.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='black', close=True))
            path = draw.Path(stroke='black', stroke_width=2, fill='none', marker_end=arrow)
            path.M(diag.path[0], layout['height'] - diag.path[1]) \
                .L(diag.path[2], layout['height'] - diag.path[3]) \
                .L(diag.path[4] - diag.scale*2, layout['height'] - diag.path[5])
            d.append(path)
        elif diag.type == 'circle':
            circle = draw.Circle(diag.left, layout['height'] - diag.bottom, diag.radius,
                                 fill='white', stroke_width=2, stroke='black')
            d.append(circle)
            textLeft = diag.left + diag.marginLeft
            textBottom = layout['height'] - diag.bottom + diag.marginBottom
            d.append(draw.Text(diag.labelText, diag.textSize, textLeft, textBottom, fill='black'))
    d.saveSvg(filename)
