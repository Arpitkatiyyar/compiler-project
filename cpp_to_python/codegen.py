from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.symtab = {}           
        self.functions = []        

    def indent(self):
        return "    " * self.indent_level

    # Top Level Dispatcher
    def generate(self, node):
        if node is None:
            return ""

        # ------------------ PROGRAM ------------------
        if isinstance(node, ProgramNode):
            parts = []
            for d in node.declarations:
                if d:
                    parts.append(self.generate(d))

            # auto-add main() runner
            if any(isinstance(d, FunctionNode) and d.name == "main"
                   for d in node.declarations):
                parts.append('\nif __name__ == "__main__":\n    main()')

            return "\n\n".join(parts)

        # ------------------ FUNCTION ------------------
        elif isinstance(node, FunctionNode):
            params = ", ".join(p.name for p in node.params)
            header = f"def {node.name}({params}):"

            self.indent_level += 1
            saved = self.symtab.copy()

            for p in node.params:
                self.symtab[p.name] = p.type_name

            body = self.generate(node.body)

            self.symtab = saved
            self.indent_level -= 1
            return header + "\n" + body

        # ------------------ BLOCK ------------------
        elif isinstance(node, BlockNode):
            self.indent_level += 1
            lines = []

            for stmt in node.statements:
                g = self.generate(stmt)
                if not g:
                    continue

                for line in g.splitlines():
                    if line.strip() == "":
                        lines.append("")
                    else:
                        lines.append(self.indent() + line)

            self.indent_level -= 1

            if not lines:
                return self.indent() + "pass"
            return "\n".join(lines)

        # ------------------ DECLARATION ------------------
        elif isinstance(node, DeclarationNode):
            self.symtab[node.name] = node.type_name
            if node.value:
                return f"{node.name} = {self.generate(node.value)}"
            else:
                return f"{node.name} = None"

        # ------------------ ASSIGNMENT ------------------
        elif isinstance(node, AssignNode):
            return f"{node.name} = {self.generate(node.value)}"

        # ------------------ PRINT ------------------
        elif isinstance(node, PrintNode):
            parts = []
            had_endl = False

            for expr in node.expr:
                if isinstance(expr, VarNode) and expr.name == "endl":
                    had_endl = True
                else:
                    parts.append(self.generate(expr))

            if had_endl:
                return f"print({', '.join(parts)})"

            if parts:
                return f"print({', '.join(parts)}, end='')"
            else:
                return "print(end='')"

        # ------------------ INPUT ------------------
        elif isinstance(node, InputNode):
            lines = []
            for name in node.targets:
                t = self.symtab.get(name)
                if t == "INT":
                    lines.append(f"{name} = int(input())")
                elif t in ("FLOAT", "DOUBLE"):
                    lines.append(f"{name} = float(input())")
                else:
                    lines.append(f"{name} = input()")
            return "\n".join(lines)

        # ------------------ IF ------------------
        elif isinstance(node, IfNode):
            code = f"if {self.generate(node.cond)}:\n" + self.generate(node.then)
            if node.else_:
                code += f"\nelse:\n" + self.generate(node.else_)
            return code

        # ------------------ WHILE ------------------
        elif isinstance(node, WhileNode):
            return f"while {self.generate(node.cond)}:\n{self.generate(node.body)}"

        # ------------------ FOR ------------------
        elif isinstance(node, ForNode):
            return self.generate_for(node)

        # ------------------ RETURN ------------------
        elif isinstance(node, ReturnNode):
            if node.expr is None:
                return "return"
            return f"return {self.generate(node.expr)}"

        # ------------------ FUNCTION CALL ------------------
        elif isinstance(node, CallNode):
            args = ", ".join(self.generate(a) for a in node.args)
            return f"{node.name}({args})"

        # ------------------ BINARY OP ------------------
        elif isinstance(node, BinOpNode):
            op = node.op
            if op == "&&": op = "and"
            if op == "||": op = "or"
            return f"({self.generate(node.left)} {op} {self.generate(node.right)})"

        # ------------------ UNARY OP ------------------
        elif isinstance(node, UnaryOpNode):
            if node.op == "!":
                return f"(not {self.generate(node.expr)})"
            if node.op == "-":
                return f"(-{self.generate(node.expr)})"
            return f"({node.op}{self.generate(node.expr)})"

        # ------------------ LITERALS ------------------
        elif isinstance(node, NumNode):
            return str(node.value)

        elif isinstance(node, BoolNode):
            return "True" if node.value else "False"

        elif isinstance(node, VarNode):
            return node.name

        elif isinstance(node, StringNode):
            esc = node.value.replace('"', '\\"')
            return f"\"{esc}\""

        return f"# Unsupported node {node}"

    #           FULLY UPDATED FOR LOOP GENERATOR
    def generate_for(self, node):
        init = node.init
        cond = node.cond
        incr = node.incr
        body = node.body

        # ----------- init -----------
        if isinstance(init, DeclarationNode):
            var = init.name
            start = self.generate(init.value)
        elif isinstance(init, AssignNode):
            var = init.name
            start = self.generate(init.value)
        else:
            return self.generate_fallback_for(node)

        # ----------- condition -----------
        if not isinstance(cond, BinOpNode):
            return self.generate_fallback_for(node)

        if not isinstance(cond.left, VarNode) or cond.left.name != var:
            return self.generate_fallback_for(node)

        op = cond.op
        stop = self.generate(cond.right)  

        # adjust <= and >=
        if op == "<=":
            stop = f"({stop} + 1)"
        elif op == ">=":
            stop = f"({stop} - 1)"

        # ----------- step detection -----------
        step = "1"

        if isinstance(incr, AssignNode) and isinstance(incr.value, BinOpNode):
            incop = incr.value.op
            val = self.generate(incr.value.right)

            if incop == "+":
                step = val
            elif incop == "-":
                step = f"-{val}"

        # If loop is descending
        if op in (">", ">=") and not step.startswith("-"):
            step = "-" + step

        # ----------- Build final Python loop -----------
        loop = f"for {var} in range({start}, {stop}, {step}):\n"
        loop += self.generate(body)
        return loop

    # fallback → while loop 
    def generate_fallback_for(self, node):
        init_code = self.generate(node.init)
        cond_code = self.generate(node.cond)
        incr_code = self.generate(node.incr)
        body_code = self.generate(node.body)

        result = init_code + "\n"
        result += f"while {cond_code}:\n"

        self.indent_level += 1
        for line in body_code.splitlines():
            result += self.indent() + line + "\n"
        result += self.indent() + incr_code + "\n"
        self.indent_level -= 1

        return result


# Manual tester
if __name__ == "__main__":
    from parser import parser
    with open(input("File location: "), "r", encoding="utf-8") as f:
        data = f.read()

    ast = parser.parse(data)
    print("AST:", ast)

    gen = CodeGenerator()
    py_code = gen.generate(ast)
    print("\nGenerated Python code:\n")
    print(py_code)
