class ProgramNode:
    def __init__(self, statements): self.statements = statements
    def __repr__(self): return f"Program({self.statements})"

class BlockNode:
    def __init__(self, statements): self.statements = statements
    def __repr__(self): return f"Block({self.statements})"

class AssignNode:
    def __init__(self, name, value): self.name, self.value = name, value
    def __repr__(self): return f"Assign({self.name}={self.value})"

class PrintNode:
    def __init__(self, expr): self.expr = expr
    def __repr__(self): return f"Print({self.expr})"

class IfNode:
    def __init__(self, cond, then, else_): self.cond, self.then, self.else_ = cond, then, else_
    def __repr__(self): return f"If({self.cond}, {self.then}, else={self.else_})"

class WhileNode:
    def __init__(self, cond, body): self.cond, self.body = cond, body
    def __repr__(self): return f"While({self.cond}, {self.body})"

class ForNode:
    def __init__(self, init, cond, incr, body): self.init, self.cond, self.incr, self.body = init, cond, incr, body
    def __repr__(self): return f"For({self.init}, {self.cond}, {self.incr}, {self.body})"

class BinOpNode:
    def __init__(self, op, left, right): self.op, self.left, self.right = op, left, right
    def __repr__(self): return f"BinOp({self.left} {self.op} {self.right})"

class NumNode:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"Num({self.value})"

class VarNode:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Var({self.name})"

class StringNode:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"String('{self.value}')"
