import ply.yacc as yacc
from lexer import tokens
from ast_nodes import *

# ------------------------------
# Grammar Rules
# ------------------------------
def p_program(p):
    'program : statement_list'
    p[0] = ProgramNode(p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# ------------------------------
# Statements
# ------------------------------
def p_statement_declaration(p):
    '''statement : INT ID ASSIGN expression SEMICOLON
                 | FLOAT ID ASSIGN expression SEMICOLON
                 | STRING ID ASSIGN STRING_LITERAL SEMICOLON'''
    if p[1] == 'string':
        p[0] = AssignNode(p[2], StringNode(p[4]))
    else:
        p[0] = AssignNode(p[2], p[4])

def p_statement_assignment(p):
    'statement : ID ASSIGN expression SEMICOLON'
    p[0] = AssignNode(p[1], p[3])

def p_statement_print(p):
    'statement : COUT LT LT expression SEMICOLON'
    p[0] = PrintNode(p[4])

def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN statement
                 | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = IfNode(p[3], p[5], None)
    else:
        p[0] = IfNode(p[3], p[5], p[7])

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN statement'
    p[0] = WhileNode(p[3], p[5])

def p_statement_for(p):
    'statement : FOR LPAREN INT ID ASSIGN expression SEMICOLON expression SEMICOLON assignment RPAREN statement'
    init = AssignNode(p[4], p[6])
    cond = p[8]
    incr = p[10]
    body = p[12]
    p[0] = ForNode(init, cond, incr, body)

def p_statement_block(p):
    'statement : LBRACE statement_list RBRACE'
    p[0] = BlockNode(p[2])

# ------------------------------
# Assignments inside for-loop
# ------------------------------
def p_assignment(p):
    'assignment : ID ASSIGN expression'
    p[0] = AssignNode(p[1], p[3])

# ------------------------------
# Expressions
# ------------------------------
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIV expression
                  | expression MOD expression
                  | expression LT expression
                  | expression GT expression
                  | expression EQ expression
                  | expression NEQ expression'''
    p[0] = BinOpNode(p[2], p[1], p[3])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = NumNode(p[1])

def p_expression_var(p):
    'expression : ID'
    p[0] = VarNode(p[1])

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_string(p):
    'expression : STRING_LITERAL'
    p[0] = StringNode(p[1])

# ------------------------------
# Error Handling
# ------------------------------
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

# ------------------------------
# Build parser
# ------------------------------
parser = yacc.yacc()

# ------------------------------
# Main for testing
# ------------------------------
if __name__ == "__main__":
    with open("test.cpp", "r") as f:
        data = f.read()
    ast = parser.parse(data)
    print("AST:", ast)
