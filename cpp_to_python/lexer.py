# import ply.lex as lex
# import ast as _ast

# # ------------------------------
# # Tokens list
# # ------------------------------
# tokens = [
#     'ID', 'NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
#     'EQ', 'NEQ', 'LE', 'GE', 'LT', 'GT',
#     'ASSIGN', 'PLUSEQ', 'MINUSEQ',
#     'INC', 'DEC',
#     'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
#     'STRING_LITERAL',
#     'SHL', 'SHR',           # << >>
#     'INCLUDE', 'COMMA',
#     # logical
#     'LAND', 'LOR', 'NOT'
# ]

# # Keywords mapping
# reserved = {
#     'int': 'INT',
#     'float': 'FLOAT',
#     'double': 'DOUBLE',
#     'char': 'CHAR',
#     'bool': 'BOOL',
#     'true': 'TRUE',
#     'false': 'FALSE',
#     'string': 'STRING',
#     'cout': 'COUT',
#     'cin': 'CIN',
#     'if': 'IF',
#     'else': 'ELSE',
#     'while': 'WHILE',
#     'for': 'FOR',
#     'using': 'USING',
#     'namespace': 'NAMESPACE',
#     'std': 'STD',
#     'main': 'MAIN',
#     'return': 'RETURN',
#     'void': 'VOID'
# }

# # Ensure reserved tokens present
# for name in set(reserved.values()):
#     if name not in tokens:
#         tokens.append(name)

# # ------------------------------
# # Token regex (order matters)
# # ------------------------------
# t_SHL = r'<<'
# t_SHR = r'>>'
# t_PLUSEQ = r'\+\='
# t_MINUSEQ = r'\-\='
# t_INC = r'\+\+'
# t_DEC = r'\-\-'
# t_PLUS = r'\+'
# t_MINUS = r'-'
# t_MULT = r'\*'
# t_DIV = r'/'
# t_MOD = r'%'
# t_EQ = r'=='
# t_NEQ = r'!='
# t_LE = r'<='
# t_GE = r'>='
# t_LT = r'<'
# t_GT = r'>'
# t_ASSIGN = r'='
# t_SEMICOLON = r';'
# t_COMMA = r','
# t_LPAREN = r'\('
# t_RPAREN = r'\)'
# t_LBRACE = r'\{'
# t_RBRACE = r'\}'
# t_LAND = r'&&'
# t_LOR = r'\|\|'
# t_NOT = r'!'

# # Match #include <...>
# def t_INCLUDE(t):
#     r'\#include\s*<[^>]+>'
#     val = t.value
#     start = val.find('<') + 1
#     end = val.rfind('>')
#     t.value = val[start:end]
#     return t

# # String literal using python literal evaluation for escapes
# def t_STRING_LITERAL(t):
#     r'\"([^\\\n]|(\\.))*?\"'
#     try:
#         # ast.literal_eval safely evaluates the quoted string literal
#         t.value = _ast.literal_eval(t.value)
#     except Exception:
#         # fallback: strip quotes
#         t.value = t.value[1:-1]
#     return t

# # Number literal: integer or float
# def t_NUMBER(t):
#     r'(\d+\.\d+|\d+)'
#     if '.' in t.value:
#         t.value = float(t.value)
#     else:
#         t.value = int(t.value)
#     return t

# # Identifier or keyword
# def t_ID(t):
#     r'[a-zA-Z_][a-zA-Z0-9_]*'
#     t.type = reserved.get(t.value, 'ID')
#     return t

# # Single-line comment
# def t_comment_singleline(t):
#     r'//.*'
#     pass

# # Multi-line comment
# def t_comment_multiline(t):
#     r'/\*([^*]|\*+[^*/])*\*+/'
#     pass

# # Ignored characters (include CR for Windows)
# t_ignore = ' \t\r'

# # Newlines
# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += len(t.value)

# # Error handling
# def t_error(t):
#     print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
#     t.lexer.skip(1)

# # Build lexer
# lexer = lex.lex()

# if __name__ == "__main__":
#     with open("test.cpp", "r", encoding="utf-8") as f:
#         data = f.read()
#     lexer.input(data)
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break
#         print(tok)
import ply.lex as lex
import ast as _ast

# ------------------------------
# Tokens list
# ------------------------------
tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
    'EQ', 'NEQ', 'LE', 'GE', 'LT', 'GT',
    'ASSIGN', 'PLUSEQ', 'MINUSEQ',
    'INC', 'DEC',
    'SEMICOLON', 'COMMA',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'STRING_LITERAL',
    'SHL', 'SHR',           # << >>
    'INCLUDE',
    'LAND', 'LOR', 'NOT'
]

# C++ keywords → token types
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'double': 'DOUBLE',
    'char': 'CHAR',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'string': 'STRING',
    'void': 'VOID',

    'cout': 'COUT',
    'cin': 'CIN',

    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',

    'using': 'USING',
    'namespace': 'NAMESPACE',
    'std': 'STD',

    'main': 'MAIN',
    'return': 'RETURN'
}

for name in reserved.values():
    if name not in tokens:
        tokens.append(name)

# ------------------------------
# Token regex (order matters!)
# ------------------------------
t_SHL = r'<<'
t_SHR = r'>>'
t_PLUSEQ = r'\+\='
t_MINUSEQ = r'\-\='
t_INC = r'\+\+'
t_DEC = r'\-\-'

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'%'

t_EQ = r'=='
t_NEQ = r'!='
t_LE = r'<='
t_GE = r'>='
t_LT = r'<'
t_GT = r'>'

t_ASSIGN = r'='
t_SEMICOLON = r';'
t_COMMA = r','

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_LAND = r'&&'
t_LOR = r'\|\|'
t_NOT = r'!'

# includes
def t_INCLUDE(t):
    r'\#include\s*<[^>]+>'
    text = t.value
    t.value = text[text.find('<') + 1 : text.rfind('>')]
    return t

# string literal
def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    try:
        t.value = _ast.literal_eval(t.value)
    except:
        t.value = t.value[1:-1]
    return t

# number (integer or float)
def t_NUMBER(t):
    r'\d+\.\d+|\d+'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# identifier / keyword
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, "ID")
    return t

# comments
def t_comment_singleline(t):
    r'//.*'
    pass

def t_comment_multiline(t):
    r'/\*([^*]|\*+[^*/])*\*+/'
    pass

# ignore
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal char '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
