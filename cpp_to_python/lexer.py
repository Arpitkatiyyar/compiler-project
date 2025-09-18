import ply.lex as lex

# ------------------------------
# Tokens
# ------------------------------
tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
    'LT', 'GT', 'EQ', 'NEQ',
    'ASSIGN', 'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'STRING_LITERAL',
    # Keywords
    'INT', 'FLOAT', 'STRING', 'COUT', 'IF', 'ELSE', 'WHILE', 'FOR',
    'INCLUDE', 'USING', 'NAMESPACE', 'STD', 'MAIN'
]

# ------------------------------
# Keywords mapping
# ------------------------------
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'cout': 'COUT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'using': 'USING',
    'namespace': 'NAMESPACE',
    'std': 'STD',
    'main': 'MAIN'
}

# ------------------------------
# Token regex
# ------------------------------
t_PLUS  = r'\+'
t_MINUS = r'-'
t_MULT  = r'\*'
t_DIV   = r'/'
t_MOD   = r'%'
t_LT    = r'<'
t_GT    = r'>'
t_EQ    = r'=='
t_NEQ   = r'!='
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Match #include <iostream>
def t_INCLUDE(t):
    r'\#include\s*<iostream>'
    t.value = "iostream"
    return t

# String literal
def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # remove quotes
    return t

# Number literal
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identifier or keyword
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Ignored characters
t_ignore = ' \t'

# Newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)
# Single-line comment (C++ style // ...)
def t_comment_singleline(t):
    r'//.*'
    pass  # ignore comment

# Multi-line comment (C style /* ... */)
def t_comment_multiline(t):
    r'/\*([^*]|\*+[^*/])*\*+/'
    pass  # ignore comment

# Build lexer
lexer = lex.lex()

# ------------------------------
# Main for testing
# ------------------------------
if __name__ == "__main__":
    with open("test.cpp", "r") as f:
        data = f.read()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: 
            break
        print(tok)
