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

    def __addRectangle(self, node, layoutState, parentDiag):
        MIN_WIDTH = 150
        MIN_HEIGHT = 30
        INDENT_WIDTH = 10
        ROW_HEIGHT = MIN_HEIGHT + 15
        MARGIN = 10

        left = layoutState['left'] + INDENT_WIDTH * node.indent
        bottom = layoutState['bottom'] - ROW_HEIGHT
        width = MIN_WIDTH
        height = MIN_HEIGHT
        layoutState['bottom'] = bottom
        
        nodeDiag = {
            'type': 'rectangle',
            'pos': [left, bottom, width, height],
            'margin': [MARGIN, MARGIN],
            'textSize': 16,
            'labelText': node.labelText
        }
        if isinstance(node, IterationNode) or isinstance(node, BranchNode):
            nodeDiag['stroke_width'] = 4
        else:
            nodeDiag['stroke_width'] = 2
        return nodeDiag

    def __addLineToRectangle(self, nodeDiag, layoutState, parentDiag):
        # To this rectangle (child)
        PARENT_LINE_START_X_RATIO = 0.1
        PARENT_LINE_END_Y_RATIO = 0.5

        left = nodeDiag['pos'][0]
        bottom = nodeDiag['pos'][1]
        width = nodeDiag['pos'][2]
        height = nodeDiag['pos'][3]
        child_line_end_x = left
        child_line_end_y = height * PARENT_LINE_END_Y_RATIO + bottom
        
        parentDiagType = parentDiag['type']
        if parentDiagType == 'rectangle':
            # From a rectangle (parent)
            childLeft = parentDiag['pos'][0]
            childBottom = parentDiag['pos'][1]
            childWidth = parentDiag['pos'][2]
            childHeight = parentDiag['pos'][3]

            child_line_start_x = childWidth * PARENT_LINE_START_X_RATIO + childLeft
            child_line_start_y = childBottom

            lineDiag = {
                'type': 'line',
                'path': [child_line_start_x, child_line_start_y,
                         child_line_start_x, child_line_end_y,
                         child_line_end_x, child_line_end_y],
                'scale': 6
            }
            return lineDiag
        return None

    def __layoutRecursively(self, node, layoutState, parentDiag):
        diags = []
        nodeDiag = None

        nodeDiagType = ''
        if not isinstance(node, Sketch) and not isinstance(node, ForkNode):
            nodeDiagType = 'rectangle'

        # Add diagram for the node
        if nodeDiagType == 'rectangle':
            nodeDiag = self.__addRectangle(node, layoutState, parentDiag)
            diags.append(nodeDiag)

        # Add lines from the parent node to this node
        if parentDiag and nodeDiag:
            lineDiag = None
            if nodeDiagType == 'rectangle':
                lineDiag = self.__addLineToRectangle(nodeDiag, layoutState, parentDiag)
            diags.append(lineDiag)

        if node.children:
            parentDiag = nodeDiag if nodeDiag else parentDiag
            for childNode in node.children:
                childDiags = self.__layoutRecursively(childNode, layoutState, parentDiag)
                diags += childDiags
        return diags

    def layout(self, node):
        WIDTH = 1024
        HEIGHT = 768
        layoutState = {'width': WIDTH, 'height': HEIGHT, 'left': 10, 'bottom': HEIGHT}

        diags = self.__layoutRecursively(node, layoutState, None)
        layout = {'width': WIDTH, 'height': HEIGHT, 'diags': diags}
        return layout

    def layout_and_draw(self, sketch):
        # Layout
        layout = self.layout(sketch)

        # Draw
        d = draw.Drawing(layout['width'], layout['height'], displayInline=False)
        
        for diag in layout['diags']:
            if diag['type'] == 'rectangle':
                r = draw.Rectangle(diag['pos'][0], diag['pos'][1], diag['pos'][2], diag['pos'][3],
                    fill='white', stroke_width=diag['stroke_width'], stroke='black')
                d.append(r)
    
                textLeft = diag['pos'][0] + diag['margin'][0]
                textBottom = diag['pos'][1] + diag['margin'][1]
                d.append(draw.Text(diag['labelText'], diag['textSize'], textLeft, textBottom, fill='black'))
            elif diag['type'] == 'line':
                arrow = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=diag['scale'], orient='auto')
                arrow.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='black', close=True))
                p = draw.Path(stroke='black', stroke_width=2, fill='none', marker_end=arrow)
                p.M(diag['path'][0], diag['path'][1]).L(diag['path'][2], diag['path'][3]).L(diag['path'][4]-diag['scale']*2, diag['path'][5])
                d.append(p)
        d.saveSvg(self.filename)

input_filename='example_sketch.txt'

output_filename=input_filename.replace(".txt", ".svg")
sketch = sp.read_and_parse(input_filename)
dd = DiagramDrawer(output_filename)
dd.layout_and_draw(sketch)
print("Output: {}".format(output_filename))
