# Grammar of hawkeye
It describes how to process hawkeye file.

## How to process hawkeye
1. Pre-processor
    1. Remove comments (all the texts after #)
    2. Strip right-side of each lines
2. Parsing the output of the pre-processor
3. Output will come out as a "Sketch" object

## Lexer grammar
TODO: it will be written after parser is completed
```
FUNCTION_TEXT : r'[a-zA-Z0-9\_](([a-zA-Z0-9\_\(\)\.])*)'
TAB : r'\t'
SPACE ; r'\s'
NEWLINES : r'(\n)*'
```

## Example
```
FunctionA(): # FunctionNode
    if a == 1: #ForkNode # Branch
        ClassC.FunctionB() # FunctionNode
    elif a == 2: # Branch
        for i = [0:10] by 1: # IterationNode
            FunctionC() # FunctionNode
            FunctionD(): # FunctionNode
                 to FunctionD
        FunctionG # FunctionNode
FunctionD:
    FunctionE
    FunctionF
```

## Parser grammar

```
SKETCH : FUNCTION_BLOCK NEWLINES FUNCTION_BLOCKS

FUNCTION_BLOCKS : ROOT_FUNCTION_BLOCK NEWLINES FUNCTION_BLOCKS
                | ROOT_FUNCTION_BLOCK
FUNCTION_BLOCK : FUNCTION_HEAD_LINE BODY_BLOCK
               | FUNCTION_LINE
FUNCTION_LINE : INDENTS FUNCTION_TEXT
FUNCTION_HEAD_LINE : INDENTS FUNCTION_TEXT COLON
BODY_BLOCK : FUNCTION_BLOCK BODY_BLOCK
           | ITERATION_BLOCK BODY_BLOCK
           | FORK_BLOCK BODY_BLOCK
           | FUNCTION_BLOCK
           | ITERATION_BLOCK
           | FORK_BLOCK

ITERATION_BLOCK : ITERATION_HEAD_LINE BODY_BLOCK
ITERATION_HEAD_LINE : INDENTS ITERATION_ INDENTS 

FORK_BLOCK : FORK_HEAD_LINE BODY_B

INDENTS : TAB INDENTS
        | SPACE INDENTS
        | TAB
        | SPACE
```
