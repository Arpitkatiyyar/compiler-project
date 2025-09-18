from parser import parser
from ast_visualizer import ASTVisualizer

with open("test.cpp", "r") as f:
    data = f.read()

ast = parser.parse(data)
print("AST:", ast)

viz = ASTVisualizer()
viz.render(ast, "ast_output")
