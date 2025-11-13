# from ast_nodes import *

# class CodeGenerator:
#     def __init__(self):
#         self.indent_level = 0
#         # simple symbol table: var_name -> declared type token (e.g. 'INT', 'FLOAT', 'STRING')
#         self.symtab = {}
#         # collect top-level function definitions to emit later (to control main wrapper)
#         self.functions = []

#     def indent(self):
#         return "    " * self.indent_level

#     def generate(self, node):
#         if node is None:
#             return ""

#         if isinstance(node, ProgramNode):
#             parts = []
#             for d in node.declarations:
#                 if d is None:
#                     continue
#                 if isinstance(d, FunctionNode):
#                     parts.append(self.generate(d))
#                 else:
#                     # global declarations (rare) - emit assignments
#                     parts.append(self.generate(d))
#             # add main invocation if there is a main function
#             if any(isinstance(d, FunctionNode) and d.name == 'main' for d in node.declarations if d):
#                 parts.append("\nif __name__ == \"__main__\":\n    main()")
#             return "\n\n".join(parts)

#         elif isinstance(node, FunctionNode):
#             # register function
#             params_names = [p.name for p in node.params]
#             header = f"def {node.name}({', '.join(params_names)}):"
#             self.indent_level += 1
#             # populate a new frame symtab for function parameters
#             saved_symtab = self.symtab.copy()
#             for p in node.params:
#                 # record param types if available
#                 self.symtab[p.name] = p.type_name
#             body_code = self.generate(node.body)
#             # restore symtab
#             self.symtab = saved_symtab
#             self.indent_level -= 1
#             return header + "\n" + body_code

#         elif isinstance(node, BlockNode):
#             self.indent_level += 1
#             lines = []
#             for stmt in node.statements:
#                 gen = self.generate(stmt)
#                 if gen is None:
#                     continue
#                 # indent each non-empty line of gen
#                 for line in gen.splitlines():
#                     if line.strip() == "":
#                         lines.append("")
#                     else:
#                         lines.append(self.indent() + line)
#             self.indent_level -= 1
#             # if block empty, add a pass to keep Python valid
#             if not lines:
#                 return self.indent() + "pass" if self.indent_level >= 0 else "pass"
#             return "\n".join(lines)

#         elif isinstance(node, DeclarationNode):
#             # store type in symbol table
#             self.symtab[node.name] = node.type_name
#             if node.value is not None:
#                 return f"{node.name} = {self.generate(node.value)}"
#             else:
#                 # default initialize to None for now
#                 return f"{node.name} = None"

#         elif isinstance(node, AssignNode):
#             return f"{node.name} = {self.generate(node.value)}"

#         elif isinstance(node, PrintNode):
#             parts = []
#             had_endl = False
#             for expr in node.expr:
#                 if isinstance(expr, VarNode) and expr.name == "endl":
#                     had_endl = True
#                 else:
#                     parts.append(self.generate(expr))
#             if not parts and had_endl:
#                 return "print()"
#             if had_endl:
#                 return f"print({', '.join(parts)})"
#             else:
#                 # emulate cout without newline
#                 if parts:
#                     return f"print({', '.join(parts)}, end='')"
#                 else:
#                     return "print(end='')"

#         elif isinstance(node, InputNode):
#             # produce assignments for each target using symtab to cast
#             lines = []
#             for name in node.targets:
#                 typ = self.symtab.get(name)
#                 if typ in ('INT',):
#                     lines.append(f"{name} = int(input())")
#                 elif typ in ('FLOAT', 'DOUBLE'):
#                     lines.append(f"{name} = float(input())")
#                 else:
#                     lines.append(f"{name} = input()")
#             return "\n".join(lines)

#         elif isinstance(node, IfNode):
#             code = f"if {self.generate(node.cond)}:\n" + self.generate(node.then)
#             if node.else_:
#                 code += f"\nelse:\n" + self.generate(node.else_)
#             return code

#         elif isinstance(node, WhileNode):
#             return f"while {self.generate(node.cond)}:\n" + self.generate(node.body)

#         elif isinstance(node, ForNode):
#             return self.generate_for(node)

#         elif isinstance(node, ReturnNode):
#             if node.expr is None:
#                 return "return"
#             return f"return {self.generate(node.expr)}"

#         elif isinstance(node, BinOpNode):
#             op = node.op
#             if op == '&&': op = 'and'
#             if op == '||': op = 'or'
#             return f"({self.generate(node.left)} {op} {self.generate(node.right)})"

#         elif isinstance(node, UnaryOpNode):
#             if node.op == '!':
#                 return f"(not {self.generate(node.expr)})"
#             if node.op == '-':
#                 return f"(-{self.generate(node.expr)})"
#             return f"({node.op}{self.generate(node.expr)})"

#         elif isinstance(node, NumNode):
#             return str(node.value)

#         elif isinstance(node, BoolNode):
#             return "True" if node.value else "False"

#         elif isinstance(node, VarNode):
#             return node.name

#         elif isinstance(node, StringNode):
#             esc = node.value.replace('"', '\\"')
#             return f"\"{esc}\""

#         else:
#             return f"# Unsupported node: {node}"

#     def generate_for(self, node):
#         """
#         More aggressive detection:
#         - init can be DeclarationNode or AssignNode
#         - incr can be AssignNode representing x = x + k (including x++ or x +=)
#         - cond is BinOpNode var < stop (or <=, >, >=)
#         When detection succeeds produce Python for-range; else fallback to while form.
#         """
#         init = node.init
#         cond = node.cond
#         incr = node.incr
#         body = node.body

#         # gather var, start
#         try:
#             if isinstance(init, DeclarationNode):
#                 var = init.name
#                 start_val = init.value.value if isinstance(init.value, NumNode) else None
#             elif isinstance(init, AssignNode):
#                 var = init.name
#                 start_val = init.value.value if isinstance(init.value, NumNode) else None
#             else:
#                 var = None
#                 start_val = None

#             # cond: var < stop or var <= stop etc.
#             if isinstance(cond, BinOpNode) and isinstance(cond.left, VarNode) and cond.left.name == var and cond.op in ("<", "<=", ">", ">="):
#                 # detect step from incr
#                 step = None
#                 if isinstance(incr, AssignNode):
#                     val = incr.value
#                     # pattern x = x + N
#                     if isinstance(val, BinOpNode) and isinstance(val.left, VarNode) and val.left.name == var and isinstance(val.right, NumNode):
#                         step = val.right.value if val.op == '+' else -val.right.value if val.op == '-' else None
#                     # pattern x = x + 1 may come from INC/DEC expansion
#                 if step is None:
#                     # maybe incr was produced from ID INC / DEC -> we converted to x = x + 1 (BinOp)
#                     if isinstance(incr, AssignNode) and isinstance(incr.value, BinOpNode) and isinstance(incr.value.right, NumNode):
#                         if isinstance(incr.value.left, VarNode) and incr.value.left.name == var:
#                             step = incr.value.right.value if incr.value.op == '+' else -incr.value.right.value
#                 if step is not None and start_val is not None:
#                     # determine stop_expr
#                     if isinstance(cond.right, NumNode):
#                         stop_val = cond.right.value
#                         if cond.op == '<=':
#                             stop_val = stop_val + (1 if step > 0 else -1)
#                         return f"for {var} in range({start_val}, {stop_val}, {step}):\n" + self.generate(body)
#                     else:
#                         # cond.right is expression -> produce range(start, cond_right, step) but careful with <= adjustment (we skip)
#                         stop_expr = self.generate(cond.right)
#                         return f"for {var} in range({start_val}, {stop_expr}, {step}):\n" + self.generate(body)
#         except Exception:
#             pass

#         # fallback: init; while cond: body; incr (ensure incr is inside the loop)
#         lines = []
#         lines.append(self.generate(init))
#         lines.append(f"while {self.generate(cond)}:")
#         self.indent_level += 1
#         # body
#         body_code = self.generate(body)
#         for line in body_code.splitlines():
#             lines.append(self.indent() + line)
#         # incr appended inside loop
#         incr_code = self.generate(incr)
#         lines.append(self.indent() + incr_code)
#         self.indent_level -= 1
#         return "\n".join(lines)


# if __name__ == "__main__":
#     from parser import parser
#     with open("test.cpp", "r", encoding="utf-8") as f:
#         data = f.read()
#     ast = parser.parse(data)
#     print("AST:", ast)

#     gen = CodeGenerator()
#     py_code = gen.generate(ast)
#     print("\nGenerated Python code:\n")
#     print(py_code)

from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.symtab = {}           # name -> type (INT/FLOAT/STRING/etc.)
        self.functions = []        # store all function definitions

    def indent(self):
        return "    " * self.indent_level

    # -----------------------------------------
    # Top-level dispatcher
    # -----------------------------------------
    def generate(self, node):
        if node is None:
            return ""

        # ------------------ PROGRAM ------------------
        if isinstance(node, ProgramNode):
            parts = []
            for d in node.declarations:
                if d is None:
                    continue
                parts.append(self.generate(d))

            # auto main() call
            if any(isinstance(d, FunctionNode) and d.name == "main"
                   for d in node.declarations):
                parts.append("\nif __name__ == \"__main__\":\n    main()")

            return "\n\n".join(parts)

        # ------------------ FUNCTION ------------------
        elif isinstance(node, FunctionNode):
            params = ", ".join(p.name for p in node.params)
            header = f"def {node.name}({params}):"
            self.indent_level += 1

            # Save old symtab (function scope)
            saved = self.symtab.copy()

            # parameters must be recorded
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
                if g is None:
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

            # cout without newline
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

        # ------------------ CALL ------------------
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

        else:
            return f"# Unsupported node {node}"

    # -----------------------------------------
    # FOR loop → Python range() or fallback
    # -----------------------------------------
    def generate_for(self, node):
        init = node.init
        cond = node.cond
        incr = node.incr
        body = node.body

        # Detect variable name
        if isinstance(init, DeclarationNode):
            var = init.name
            start = init.value.value if isinstance(init.value, NumNode) else None
        elif isinstance(init, AssignNode):
            var = init.name
            start = init.value.value if isinstance(init.value, NumNode) else None
        else:
            return self.generate_fallback_for(node)

        # Detect condition
        if not isinstance(cond, BinOpNode):
            return self.generate_fallback_for(node)
        if not isinstance(cond.left, VarNode) or cond.left.name != var:
            return self.generate_fallback_for(node)

        # Extract stop value
        if isinstance(cond.right, NumNode):
            stop = cond.right.value
        else:
            return self.generate_fallback_for(node)

        # Detect increment
        step = 1
        if isinstance(incr, AssignNode) and isinstance(incr.value, BinOpNode):
            op = incr.value.op
            if isinstance(incr.value.right, NumNode):
                val = incr.value.right.value
                if op == "+":
                    step = val
                elif op == "-":
                    step = -val

        # Adjust stop for <=
        if cond.op == "<=" and isinstance(stop, int):
            stop = stop + 1

        # For > or >=, ensure step is negative
        if cond.op in (">", ">=") and step > 0:
            step = -step
        if cond.op == ">=" and isinstance(stop, int):
            stop = stop - 1

        # Build range loop
        loop = f"for {var} in range({start}, {stop}, {step}):\n"
        loop += self.generate(body)
        return loop

    # fallback → while loop form
    def generate_fallback_for(self, node):
        init = self.generate(node.init)
        condition = self.generate(node.cond)
        body = self.generate(node.body)
        incr = self.generate(node.incr)

        result = init + "\n"
        result += f"while {condition}:\n"
        self.indent_level += 1
        for line in body.splitlines():
            result += self.indent() + line + "\n"
        result += self.indent() + incr + "\n"
        self.indent_level -= 1
        return result


# -------------------------------------------------
# Manual tester
# -------------------------------------------------
if __name__ == "__main__":
    from parser import parser
    with open("test.cpp", "r", encoding="utf-8") as f:
        data = f.read()

    ast = parser.parse(data)
    print("AST:", ast)

    gen = CodeGenerator()
    py_code = gen.generate(ast)
    print("\nGenerated Python code:\n")
    print(py_code)
