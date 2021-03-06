import ast
import inspect
import networkx
import fibonacci
from visitor import ASTVisitor


def vizualize_ast(result_file):
    ast_object = ast.parse(inspect.getsource(fibonacci))
    visitor = ASTVisitor()
    visitor.visit(ast_object)
    networkx.drawing.nx_pydot.to_pydot(visitor.graph).write_png(result_file)


if __name__ == '__main__':
    vizualize_ast("artifacts/ast.png")
