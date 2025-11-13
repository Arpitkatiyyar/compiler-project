# class ProgramNode:
#     def __init__(self, statements): self.statements = statements
#     def __repr__(self): return f"Program({self.statements})"

# class BlockNode:
#     def __init__(self, statements): self.statements = statements
#     def __repr__(self): return f"Block({self.statements})"

# class AssignNode:
#     def __init__(self, name, value): self.name, self.value = name, value
#     def __repr__(self): return f"Assign({self.name}={self.value})"

# class PrintNode:
#     def __init__(self, expr): self.expr = expr
#     def __repr__(self): return f"Print({self.expr})"

# class IfNode:
#     def __init__(self, cond, then, else_): self.cond, self.then, self.else_ = cond, then, else_
#     def __repr__(self): return f"If({self.cond}, {self.then}, else={self.else_})"

# class WhileNode:
#     def __init__(self, cond, body): self.cond, self.body = cond, body
#     def __repr__(self): return f"While({self.cond}, {self.body})"

# class ForNode:
#     def __init__(self, init, cond, incr, body): self.init, self.cond, self.incr, self.body = init, cond, incr, body
#     def __repr__(self): return f"For({self.init}, {self.cond}, {self.incr}, {self.body})"

# class BinOpNode:
#     def __init__(self, op, left, right): self.op, self.left, self.right = op, left, right
#     def __repr__(self): return f"BinOp({self.left} {self.op} {self.right})"

# class NumNode:
#     def __init__(self, value): self.value = value
#     def __repr__(self): return f"Num({self.value})"

# class VarNode:
#     def __init__(self, name): self.name = name
#     def __repr__(self): return f"Var({self.name})"

# class StringNode:
#     def __init__(self, value): self.value = value
#     def __repr__(self): return f"String('{self.value}')"


class ProgramNode:
    def __init__(self, declarations):
        self.declarations = declarations
    def __repr__(self):
        return f"Program({self.declarations})"


class BlockNode:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Block({self.statements})"


class DeclarationNode:
    def __init__(self, type_name, name, value):
        self.type_name = type_name
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Decl({self.type_name} {self.name} = {self.value})"


class AssignNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Assign({self.name}={self.value})"


class PrintNode:
    def __init__(self, expr_list):
        self.expr = expr_list
    def __repr__(self):
        return f"Print({self.expr})"


class InputNode:
    def __init__(self, targets):
        self.targets = targets
    def __repr__(self):
        return f"Input({self.targets})"


class IfNode:
    def __init__(self, cond, then, else_):
        self.cond = cond
        self.then = then
        self.else_ = else_
    def __repr__(self):
        return f"If({self.cond}, {self.then}, else={self.else_})"


class WhileNode:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    def __repr__(self):
        return f"While({self.cond}, {self.body})"


class ForNode:
    def __init__(self, init, cond, incr, body):
        self.init = init
        self.cond = cond
        self.incr = incr
        self.body = body
    def __repr__(self):
        return f"For({self.init}, {self.cond}, {self.incr}, {self.body})"


class ReturnNode:
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"Return({self.expr})"


class FunctionNode:
    def __init__(self, ret_type, name, params, body):
        self.ret_type = ret_type
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self):
        return f"Function({self.ret_type} {self.name}({self.params}) {self.body})"


class ParamNode:
    def __init__(self, type_name, name):
        self.type_name = type_name
        self.name = name
    def __repr__(self):
        return f"Param({self.type_name} {self.name})"


class CallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __repr__(self):
        return f"Call({self.name}, {self.args})"


class BinOpNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    def __repr__(self):
        return f"BinOp({self.left} {self.op} {self.right})"


class UnaryOpNode:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    def __repr__(self):
        return f"Unary({self.op} {self.expr})"


class NumNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Num({self.value})"


class BoolNode:
    def __init__(self, value):
        self.value = bool(value)
    def __repr__(self):
        return f"Bool({self.value})"


class VarNode:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Var({self.name})"


class StringNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"String({self.value!r})"
