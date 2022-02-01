import ast
import inspect
import networkx
import fibonacci
from visitor import ASTVisitor

if __name__ == '__main__':
    ast_object = ast.parse(inspect.getsource(fibonacci))
    visitor = ASTVisitor()
    visitor.visit(ast_object)
    networkx.drawing.nx_pydot.to_pydot(visitor.graph).write_png("artifacts/ast.png")

