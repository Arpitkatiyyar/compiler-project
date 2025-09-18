from graphviz import Digraph
from ast_nodes import *

class ASTVisualizer:
    def __init__(self):
        self.graph = Digraph(comment="Abstract Syntax Tree")
        self.counter = 0

    def new_id(self):
        self.counter += 1
        return f"node{self.counter}"

    def add_node(self, node, parent=None):
        nid = self.new_id()
        label = type(node).__name__

        # Specialize labels
        if isinstance(node, AssignNode):
            label += f"\\n{node.name}"
        elif isinstance(node, VarNode):
            label += f"\\n{node.name}"
        elif isinstance(node, NumNode):
            label += f"\\n{node.value}"
        elif isinstance(node, StringNode):
            label += f"\\n\"{node.value}\""
        elif isinstance(node, BinOpNode):
            label += f"\\n{node.op}"

        self.graph.node(nid, label)

        if parent:
            self.graph.edge(parent, nid)

        # Recurse into children
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.add_node(stmt, nid)
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self.add_node(stmt, nid)
        elif isinstance(node, AssignNode):
            self.add_node(node.value, nid)
        elif isinstance(node, PrintNode):
            self.add_node(node.expr, nid)
        elif isinstance(node, IfNode):
            self.add_node(node.cond, nid)
            self.add_node(node.then, nid)
            if node.else_:
                self.add_node(node.else_, nid)
        elif isinstance(node, WhileNode):
            self.add_node(node.cond, nid)
            self.add_node(node.body, nid)
        elif isinstance(node, ForNode):
            self.add_node(node.init, nid)
            self.add_node(node.cond, nid)
            self.add_node(node.incr, nid)
            self.add_node(node.body, nid)
        elif isinstance(node, BinOpNode):
            self.add_node(node.left, nid)
            self.add_node(node.right, nid)

        return nid

    def render(self, ast, filename="ast"):
        self.add_node(ast)
        self.graph.render(filename, format="png", cleanup=True)
        print(f"AST image saved as {filename}.png")
