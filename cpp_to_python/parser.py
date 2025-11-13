import ply.yacc as yacc
from lexer import tokens
from ast_nodes import *

# ------------------------------
# Precedence rules
# ------------------------------
precedence = (
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'NOT'),
    ('right', 'UMINUS'),
)

# ------------------------------
# Program structure
# ------------------------------
def p_program(p):
    '''program : external_list'''
    p[0] = ProgramNode(p[1])

def p_external_list(p):
    '''external_list : external
                     | external_list external'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_external(p):
    '''external : includes
                | using_namespace
                | function_def
                | main_function'''
    p[0] = p[1]

# ------------------------------
# includes / using namespace
# ------------------------------
def p_includes(p):
    '''includes : INCLUDE'''
    p[0] = None

def p_using_namespace(p):
    '''using_namespace : USING NAMESPACE STD SEMICOLON
                       | empty'''
    p[0] = None

# ------------------------------
# Function definitions
# ------------------------------
def p_function_def(p):
    '''function_def : type ID LPAREN param_list RPAREN block'''
    p[0] = FunctionNode(p[1], p[2], p[4], p[6])

def p_main_function(p):
    '''main_function : INT MAIN LPAREN RPAREN block'''
    p[0] = FunctionNode('INT', 'main', [], p[5])

def p_param_list(p):
    '''param_list : empty
                  | params'''
    p[0] = [] if p[1] is None else p[1]

def p_params(p):
    '''params : param
              | params COMMA param'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_param(p):
    '''param : type ID'''
    p[0] = ParamNode(p[1], p[2])

# ------------------------------
# Types
# ------------------------------
def p_type(p):
    '''type : INT
            | FLOAT
            | DOUBLE
            | CHAR
            | BOOL
            | STRING
            | VOID'''
    p[0] = p.slice[1].type

# ------------------------------
# Block / Statement list
# ------------------------------
def p_block(p):
    'block : LBRACE statement_list RBRACE'
    p[0] = BlockNode(p[2])

def p_statement_list(p):
    '''statement_list : empty
                      | statement_list statement'''
    p[0] = [] if p[1] is None else p[1] + [p[2]]

def p_statement(p):
    '''statement : declaration SEMICOLON
                 | assignment SEMICOLON
                 | print_stmt SEMICOLON
                 | input_stmt SEMICOLON
                 | if_stmt
                 | while_stmt
                 | for_stmt
                 | return_stmt SEMICOLON
                 | block'''
    p[0] = p[1]

# ------------------------------
# Variable declaration
# ------------------------------
def p_declaration(p):
    '''declaration : type ID ASSIGN expression
                   | type ID ASSIGN STRING_LITERAL'''
    typ = p[1]
    name = p[2]
    val = p[4]
    if isinstance(val, str):
        val = StringNode(val)
    p[0] = DeclarationNode(typ, name, val)

# ------------------------------
# Assignments
# ------------------------------
def p_assignment_basic(p):
    'assignment : ID ASSIGN expression'
    p[0] = AssignNode(p[1], p[3])

def p_assignment_pluseq(p):
    'assignment : ID PLUSEQ expression'
    p[0] = AssignNode(p[1], BinOpNode('+', VarNode(p[1]), p[3]))

def p_assignment_minuseq(p):
    'assignment : ID MINUSEQ expression'
    p[0] = AssignNode(p[1], BinOpNode('-', VarNode(p[1]), p[3]))

def p_assignment_inc(p):
    'assignment : ID INC'
    p[0] = AssignNode(p[1], BinOpNode('+', VarNode(p[1]), NumNode(1)))

def p_assignment_dec(p):
    'assignment : ID DEC'
    p[0] = AssignNode(p[1], BinOpNode('-', VarNode(p[1]), NumNode(1)))


# ------------------------------
# cout << printing
# ------------------------------
def p_print_stmt(p):
    'print_stmt : COUT print_tail'
    p[0] = PrintNode(p[2])

def p_print_tail_single(p):
    'print_tail : SHL expression'
    p[0] = [p[2]]

def p_print_tail_chain(p):
    'print_tail : print_tail SHL expression'
    p[0] = p[1] + [p[3]]

# ------------------------------
# cin >> input
# ------------------------------
def p_input_stmt(p):
    'input_stmt : CIN input_tail'
    p[0] = InputNode(p[2])

def p_input_tail_single(p):
    'input_tail : SHR ID'
    p[0] = [p[2]]

def p_input_tail_chain(p):
    'input_tail : input_tail SHR ID'
    p[0] = p[1] + [p[3]]

# ------------------------------
# if / while / for
# ------------------------------
def p_if_stmt(p):
    '''if_stmt : IF LPAREN expression RPAREN statement
               | IF LPAREN expression RPAREN statement ELSE statement'''
    p[0] = IfNode(p[3], p[5], None if len(p) == 6 else p[7])

def p_while_stmt(p):
    'while_stmt : WHILE LPAREN expression RPAREN statement'
    p[0] = WhileNode(p[3], p[5])

def p_for_stmt_decl(p):
    '''for_stmt : FOR LPAREN type ID ASSIGN expression SEMICOLON expression SEMICOLON assignment RPAREN statement'''
    init = DeclarationNode(p[3], p[4], p[6])
    p[0] = ForNode(init, p[8], p[10], p[12])

def p_for_stmt_assign(p):
    '''for_stmt : FOR LPAREN assignment SEMICOLON expression SEMICOLON assignment RPAREN statement'''
    p[0] = ForNode(p[3], p[5], p[7], p[9])

# ------------------------------
# return
# ------------------------------
def p_return_stmt_val(p):
    'return_stmt : RETURN expression'
    p[0] = ReturnNode(p[2])

def p_return_stmt_empty(p):
    'return_stmt : RETURN'
    p[0] = ReturnNode(None)

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
                  | expression LE expression
                  | expression GE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LAND expression
                  | expression LOR expression'''
    p[0] = BinOpNode(p[2], p[1], p[3])

def p_expression_unary(p):
    '''expression : NOT expression
                  | MINUS expression %prec UMINUS'''
    p[0] = UnaryOpNode(p[1], p[2])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = NumNode(p[1])

def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = BoolNode(p.slice[1].type == 'TRUE')

def p_expression_string(p):
    'expression : STRING_LITERAL'
    p[0] = StringNode(p[1])

def p_expression_var(p):
    'expression : ID'
    p[0] = VarNode(p[1])

# function call
def p_expression_call(p):
    'expression : ID LPAREN arg_list RPAREN'
    p[0] = CallNode(p[1], p[3])

def p_arg_list_empty(p):
    'arg_list : empty'
    p[0] = []

def p_arg_list_single(p):
    'arg_list : expression'
    p[0] = [p[1]]

def p_arg_list_multi(p):
    'arg_list : arg_list COMMA expression'
    p[0] = p[1] + [p[3]]

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# ------------------------------
# Empty
# ------------------------------
def p_empty(p):
    'empty :'
    pass

# ------------------------------
# Error
# ------------------------------
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()
