import copy

# * Sketch
#   - arr<FunctionNode> children
# * Node
#   - str labelText
# * FunctionNode : Node
#   - arr<Node> children
#   - srt redirectLabelText
# * IterationNode : Node
#   - arr<Node> children
# * ForkNode : Node
#   - arr<BranchNode> children
# * BranchNode
#   - str labelText
#   - arr<Node> children

class Sketch:
    def __init__(self):
        self.children = []
    def __str__(self):
        s = "# Sketch:0"
        for child in self.children:
            s += '\n' + str(child)
        return s

class Node:
    def __init__(self, indent, labelText):
        self.indent = indent
        self.child_indent = -1
        self.labelText = labelText
        self.children = []

class FunctionNode(Node):
    def __init__(self, indent, labelText, redirectLabelText):
        super().__init__(indent, labelText)
        self.redirectLabelText = redirectLabelText
    def __str__(self):
        s = (' ' * self.indent) + self.labelText
        if len(self.redirectLabelText) > 0:
            s += ' => ' + self.redirectLabelText
        if len(self.children) > 0:
            s += ':'
        s += " # Function:{}".format(self.indent)
        for child in self.children:
            s += '\n' + str(child)
        return s

class IterationNode(Node):
    def __init__(self, indent, labelText):
        super().__init__(indent, labelText)
    def __str__(self):
        s = (' ' * self.indent) + self.labelText
        if len(self.children) > 0:
            s += ':'
        s += " # Iteration:{}".format(self.indent)
        for child in self.children:
            s += '\n' + str(child)
        return s

class ForkNode(Node):
    def __init__(self, indent):
        super().__init__(indent, "")
    def __str__(self):
        s = (' ' * self.indent) + self.labelText
        s += "# Fork:{}".format(self.indent)
        for child in self.children:
            s += '\n' + str(child)
        return s

class BranchNode(Node):
    def __init__(self, indent, labelText):
        super().__init__(indent, labelText) 
        self.indent = indent
        self.labelText = labelText
    def __str__(self):
        s = (' ' * self.indent) + self.labelText
        if len(self.children) > 0:
            s += ':'
        s += " # Branch:{}".format(self.indent)
        for child in self.children:
            s += '\n' + str(child)
        return s

def preprocess(orig_lines):
    strip_lines = []
    for line in orig_lines:
        # remove comments
        strip_line = line
        range_start = 0
        range_end = len(line)
        while True:
            comment_idx = strip_line.rfind('#', range_start, range_end)
            range_end = comment_idx - 1 if comment_idx > 0 else 0
            if comment_idx < 0:
                break
            if comment_idx > 0 and strip_line[comment_idx - 1] == '\\':
                # \# => #
                strip_line = strip_line[:comment_idx - 1] + strip_line[comment_idx:]
            else:
                # # => comment out
                strip_line = strip_line[:comment_idx]

        # strip right spaces
        strip_line = strip_line.rstrip()

        strip_lines.append(strip_line)
    return strip_lines
    
def raise_exception(linenum, line, message):
    return Exception("Line {}: {}\n=> {}".format(linenum, message, line))

def raise_exception2(linenum, message):
    return Exception("Line {}: {}".format(linenum, message))

def parse(strip_lines):
    tokens = []
    for linenum, line in enumerate(strip_lines):
        word_start_idx = 0

        # INDENT_T or INDENT_S
        while word_start_idx < len(line):
            if line[word_start_idx] == '\t':
                tokens.append(["INDENT_T"])
            elif line[word_start_idx] == ' ':
                tokens.append(["INDENT_S"])
            else:
                break
            word_start_idx += 1

        if len(line) <= 0:
            continue

        # filter END_COLON
        end_colon_found = (line[-1] == ':')
        if end_colon_found:
            line = line[:-1]

        # WORDs or REDIRECT
        words = line[word_start_idx:].split()
        if len(words) > 0:
            redirect_found = False
            word_found = False
            word_after_redirect_found = False
            for word in words:
                if word == '=>':
                    if not word_found:
                        raise_exception(linenum, line, "Redirection sign must not be used at the start")
                    elif end_colon_found:
                        raise_exception(linenum, line, "Redirection sign must be used without colon at the end")
                    elif redirect_found:
                        raise_exception(linenum, line, "Redirection sign must be used once")
                    redirect_found = True
                    tokens.append(["REDIRECT"])
                else:
                    word_found = True
                    if redirect_found:
                        word_after_redirect_found = True
                    tokens.append(["WORD", word])
                if redirect_found and not word_after_redirect_found:
                    raise_exception(linenum, line, "At least a word must follow the redirection sign")

        # END_COLON
        if end_colon_found:
            tokens.append(["END_COLON"])

        # NEWLINE
        tokens.append(["NEWLINE"])
    return tokens

def analyze_syntax(tokens):
    sketch = Sketch()
    nodeStack = [sketch]

    initial_line = {
        'indent': 0,
        'words_before_redirect': [],
        'words_after_redirect': [],
        'keyword': None,
        'end_colon': False,

        'keyword_check': False,
        'redirect_found': False
    }
    line = copy.deepcopy(initial_line)
    i = 0
    linenum = 1
    while i < len(tokens):
        token = tokens[i]
        tokenType = token[0]
        if tokenType != 'NEWLINE':
            if tokenType == 'INDENT_S':
                line['indent'] += 1
            elif tokenType == 'INDENT_T':
                line['indent'] += 4
            elif tokenType == 'END_COLON':
                line['end_colon'] = True
            elif tokenType == 'REDIRECT':
                line['redirect_found'] = True
            elif tokenType == 'WORD':
                tokenText = token[1]
                if not line['keyword_check']:
                    line['keyword_check'] = True
                    if tokenText in ['if', 'elif', 'else', 'for', 'while']:
                        line['keyword'] = tokenText
                        continue
                if not line['redirect_found']:
                    line['words_before_redirect'].append(tokenText)
                else:
                    line['words_after_redirect'].append(tokenText)
        else:
            # NEWLINE
            keyword = line['keyword']
            indent = line['indent']
            topNode = nodeStack[-1]
            newNode = None

            # Check indent
            if isinstance(topNode, Sketch):
                # Sketch's indent should be 0
                if indent != 0:
                    raise_exception2(linenum, "Invalid indent")
            else:
                if topNode.child_indent < 0:
                    # Determine top node's child indent
                    if indent <= topNode.indent:
                        raise_exception2(linenum, "Invalid indent")
                    topNode.child_indent = indent
                else:
                    while len(nodeStack) > 1 and indent <= topNode.indent:
                        # pop
                        if indent == topNode.indent:
                            if isinstance(topNode, ForkNode) and keyword in ['elif', 'else']:
                                break
                        nodeStack = nodeStack[:-1]
                        topNode = nodeStack[-1]

            # Check keyword
            text = ' '.join(line['words_before_redirect'])
            redirect_text = ' '.join(line['words_after_redirect'])
            if keyword is None:
                # FunctionNode
                newNode = FunctionNode(indent, text, redirect_text)
                topNode.children.append(newNode)
            elif keyword == 'if':
                # ForkNode + BranchNode
                if len(redirect_text) > 0:
                    raise_exception2(linenum, "Invalid redirection sign")
                forkNode = ForkNode(indent)
                nodeStack.append(forkNode)
                newNode = BranchNode(indent, text)
                topNode.children.append(forkNode)
                forkNode.children.append(newNode)
            elif keyword in ['elif', 'else']:
                # BranchNode
                if len(redirect_text) > 0:
                    raise_exception2(linenum, "Invalid redirection sign")
                newNode = BranchNode(indent, text)
                topNode.children.append(newNode)
            elif keyword in ['for', 'while']:
                # IterationNode
                if len(redirect_text) > 0:
                    raise_exception2(linenum, "Invalid redirection sign")
                newNode = IterationNode(indent, text)
                topNode.children.append(newNode)
            else:
                raise_exception2(linenum, "Invalid keyword {}".format(keyword))

            # Push the new node if child is expected
            if newNode and line['end_colon']:
                nodeStack.append(newNode)
            line = copy.deepcopy(initial_line)
            linenum += 1
        i += 1
    return sketch

class SketchCompiler:
    def compile(self, text):
        orig_lines = text.splitlines()
    
        # 1. Pre-processing: remove comments and strip right spaces
        strip_lines = preprocess(orig_lines)
    
        # 2. Parsing: indent, word, colon, redirect_sign
        tokens = parse(strip_lines)
    
        # 3. Syntax analysis
        sketch = analyze_syntax(tokens)
        return sketch
