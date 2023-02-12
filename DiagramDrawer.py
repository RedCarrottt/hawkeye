# HawkEye
import drawSvg as draw
from SketchParser import Sketch, Node, FunctionNode, IterationNode, ForkNode, BranchNode

MIN_HEIGHT = 30

class Diag:
    def __init__(self, diagType):
        self.type = diagType
        pass

class Rectangle(Diag):
    def __init__(self, node, left, bottom):
        super().__init__('rectangle')
        MIN_WIDTH = 150
        MARGIN = 10

        width = MIN_WIDTH
        height = MIN_HEIGHT

        self.node = node
        self.pos = [left, bottom, width, height]
        self.margin = [MARGIN, MARGIN]
        self.textSize = 16
        self.labelText = node.labelText

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

        if nodeDiag.type == 'rectangle':
            end_pos = self.__toRectangle(nodeDiag)

        if start_pos and end_pos:
            self.path = [start_pos[0], start_pos[1],
                         start_pos[0], end_pos[1],
                         end_pos[0], end_pos[1]]
            self.scale = 6
            self.isAvailable = True

    def __fromRectangle(self, parentDiag):
        LINE_START_X_RATIO = 0.1
        childLeft = parentDiag.pos[0]
        childBottom = parentDiag.pos[1]
        childWidth = parentDiag.pos[2]
        childHeight = parentDiag.pos[3]
        return (childWidth * LINE_START_X_RATIO + childLeft, childBottom)

    def __toRectangle(self, nodeDiag):
        LINE_END_Y_RATIO = 0.5
        left = nodeDiag.pos[0]
        bottom = nodeDiag.pos[1]
        width = nodeDiag.pos[2]
        height = nodeDiag.pos[3]
        return (left, height * LINE_END_Y_RATIO + bottom)

def __layoutRecursively(node, layoutState, parentDiag):
    diags = []
    nodeDiag = None

    nodeDiagType = ''
    if not isinstance(node, Sketch) and not isinstance(node, ForkNode):
        nodeDiagType = 'rectangle'

    # Add diagram for the node
    INDENT_WIDTH = 10
    ROW_HEIGHT = MIN_HEIGHT + 15
    if nodeDiagType == 'rectangle':
        left = layoutState['left'] + INDENT_WIDTH * node.indent
        bottom = layoutState['bottom'] - ROW_HEIGHT
        nodeDiag = Rectangle(node, left, bottom)
        diags.append(nodeDiag)
        layoutState['bottom'] = bottom

    # Add lines from the parent node to this node
    if parentDiag and nodeDiag:
        lineDiag = Line(parentDiag, nodeDiag)
        if lineDiag.isAvailable:
            diags.append(lineDiag)

    if node.children:
        parentDiag = nodeDiag if nodeDiag else parentDiag
        for childNode in node.children:
            childDiags = __layoutRecursively(childNode, layoutState, parentDiag)
            diags += childDiags
    return diags

def __layout(node):
    WIDTH = 1024
    HEIGHT = 768
    layoutState = {'width': WIDTH, 'height': HEIGHT, 'left': 10, 'bottom': HEIGHT}

    diags = __layoutRecursively(node, layoutState, None)
    layout = {'width': WIDTH, 'height': HEIGHT, 'diags': diags}
    return layout

def layout_and_draw(sketch, filename):
    # Layout
    layout = __layout(sketch)

    # Draw
    d = draw.Drawing(layout['width'], layout['height'], displayInline=False)
    
    for diag in layout['diags']:
        if diag.type == 'rectangle':
            r = draw.Rectangle(diag.pos[0], diag.pos[1], diag.pos[2], diag.pos[3],
                fill='white', stroke_width=diag.stroke_width, stroke='black')
            d.append(r)

            textLeft = diag.pos[0] + diag.margin[0]
            textBottom = diag.pos[1] + diag.margin[1]
            d.append(draw.Text(diag.labelText, diag.textSize, textLeft, textBottom, fill='black'))
        elif diag.type == 'line':
            arrow = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=diag.scale, orient='auto')
            arrow.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='black', close=True))
            p = draw.Path(stroke='black', stroke_width=2, fill='none', marker_end=arrow)
            p.M(diag.path[0], diag.path[1]).L(diag.path[2], diag.path[3]).L(diag.path[4]-diag.scale*2, diag.path[5])
            d.append(p)
    d.saveSvg(filename)
