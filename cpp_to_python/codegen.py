from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0

    def indent(self):
        return "    " * self.indent_level  # 4 spaces per level

    def generate(self, node):
        if isinstance(node, ProgramNode):
            return "\n".join(self.generate(stmt) for stmt in node.statements)

        elif isinstance(node, BlockNode):
            self.indent_level += 1
            code = "\n".join(self.indent() + self.generate(stmt) for stmt in node.statements)
            self.indent_level -= 1
            return code

        elif isinstance(node, AssignNode):
            return f"{node.name} = {self.generate(node.value)}"

        elif isinstance(node, PrintNode):
            return f"print({self.generate(node.expr)})"

        elif isinstance(node, IfNode):
            code = f"if {self.generate(node.cond)}:\n" + self.generate(node.then)
            if node.else_:
                code += f"\nelse:\n" + self.generate(node.else_)
            return code

        elif isinstance(node, WhileNode):
            code = f"while {self.generate(node.cond)}:\n" + self.generate(node.body)
            return code

        elif isinstance(node, ForNode):
            # Only handles standard numeric for-loops like: for(int i=0; i<x; i=i+1)
            init = node.init
            cond = node.cond
            incr = node.incr

            start = self.generate(init.value)

            if isinstance(cond, BinOpNode) and cond.op == "<":
                stop = self.generate(cond.right)
            else:
                stop = "??"  # fallback if condition not supported

            step = 1
            if isinstance(incr.value, BinOpNode) and incr.value.op == "+":
                step = self.generate(incr.value.right)

            code = f"for {init.name} in range({start}, {stop}, {step}):\n"
            code += self.generate(node.body)
            return code

        elif isinstance(node, BinOpNode):
            return f"({self.generate(node.left)} {node.op} {self.generate(node.right)})"

        elif isinstance(node, NumNode):
            return str(node.value)

        elif isinstance(node, VarNode):
            return node.name

        elif isinstance(node, StringNode):
            return f"\"{node.value}\""

        else:
            return f"# Unsupported node: {node}"

# ------------------------------
# Main for testing
# ------------------------------
if __name__ == "__main__":
    from parser import parser
    with open("test.cpp", "r") as f:
        data = f.read()
    ast = parser.parse(data)
    print("AST:", ast)

    gen = CodeGenerator()
    py_code = gen.generate(ast)
    print("\nGenerated Python code:\n")
    print(py_code)
