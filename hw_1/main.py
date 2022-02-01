import ast
import inspect
import networkx


def fibonacci(n):
    fib1 = fib2 = 1
    result = [fib1, fib2]
    n = n - 2
    for i in range(n):
        fib1, fib2 = fib2, fib1 + fib2
        result.append(fib2)
    return result


def fibonacci_series(n):

    fib1 = fib2 = 1
    n = n - 2
    for i in range(n):
        fib1, fib2 = fib2, fib1 + fib2
    return fib2


class ASTVisitor(ast.NodeVisitor):

    def __init__(self):
        self.names = {"BODY": 0, "TARGETS": 0, "VALUE": 0, "TARGET": 0, "TUPLE": 0}
        self.graph = networkx.DiGraph()

    def visit_Module(self, node):
        self.visit(node.body[0])

    def visit_args(self, arguments):
        self.graph.add_node("arguments", label="Arguments", fillcolor='#AAF0C8', style='filled')
        for arg in arguments:
            self.graph.add_node(str(arg), label=f'name: {arg.arg}', shape='s', fillcolor='#80E7EA', style='filled')
            self.graph.add_edge("arguments", str(arg))
        return "arguments"

    def visit_targets(self, node):
        targets = f'TARGETS {self.names["TARGETS"]}'
        self.names["TARGETS"] += 1
        self.graph.add_node(targets, label="Targets", fillcolor='#7C81F0', style='filled')
        for tar in node.targets:
            self.graph.add_edge(targets, self.visit(tar))
        return targets

    def visit_value(self, node):
        value = f'VALUE {self.names["VALUE"]}'
        self.names["VALUE"] += 1
        # F0BB7F
        self.graph.add_node(value, label="Value", fillcolor='#B470F5', style='filled')
        self.graph.add_edge(value, self.visit(node.value))
        return value

    def visit_body(self, node):
        body = f'BODY {self.names["BODY"]}'
        self.names["BODY"] += 1
        self.graph.add_node(body, label="body", fillcolor='#E54E2A', style='filled')
        for item in node.body:
            self.graph.add_edge(body, self.visit(item))
        return body

    def visit_target(self, node):
        target = f'TARGET {self.names["TARGET"]}'
        self.graph.add_node(target, label="Target", fillcolor='#F8EB90', style='filled')
        self.graph.add_edge(target, self.visit(node.target))
        return target

    def visit_Assign(self, node):
        self.graph.add_node(str(node), label="Assign", shape='s', fillcolor='#EF7D58', style='filled')
        self.graph.add_edge(str(node), self.visit_targets(node))
        self.graph.add_edge(str(node), self.visit_value(node))
        return str(node)

    def visit_Name(self, node):
        self.graph.add_node(str(node), label=f'name: {node.id}', shape='s', fillcolor='#80E7EA', style='filled')
        return str(node)

    def visit_Num(self, node):
        self.graph.add_node(str(node), label=f'number \n value: {str(node.n)}', shape='s', fillcolor='#F7D8F4', style='filled')
        return str(node)

    def visit_BinOp(self, node):
        self.graph.add_node(str(node), label=f'BinaryOperation: \n {node.op.__class__.__name__}', shape='s', fillcolor='#C0B6F0', style='filled')
        self.graph.add_edge(str(node), self.visit(node.left))
        self.graph.add_edge(str(node), self.visit(node.right))
        return str(node)

    def visit_For(self, node):
        self.graph.add_node(str(node), label="For", shape='s', fillcolor='#F5A845', style='filled')
        self.graph.add_node("iteration", label="iteration", fillcolor='#D6F5A7', style='filled')
        self.graph.add_edge(str(node), "iteration")
        self.graph.add_edge("iteration", self.visit_target(node))
        self.graph.add_edge("iteration", self.visit(node.iter))
        self.graph.add_edge(str(node), self.visit_body(node))
        return str(node)

    def visit_Call(self, node):
        self.graph.add_node(str(node), label="Call", fillcolor='#F37BD4', style='filled')
        self.graph.add_edge(str(node), self.visit(node.func), label="function")
        for item in node.args:
            self.graph.add_edge(str(node), self.visit(item), label="argument")
        return str(node)

    def visit_Tuple(self, node):
        tuple = f'TUPLE {self.names["TUPLE"]}'
        self.names["TUPLE"] += 1
        self.graph.add_node(tuple, label="Tuple", fillcolor='#87F38B', style='filled')
        for num, item in enumerate(node.elts):
            self.graph.add_edge(tuple, self.visit(item), label=f'{num + 1} arg')
        return tuple

    def visit_Expr(self, node):
        self.graph.add_node(str(node), label="Expression", shape='s', fillcolor='#F9A354', style='filled')
        self.graph.add_edge(str(node), self.visit(node.value))
        return str(node)

    def visit_Attribute(self, node):
        self.graph.add_node(str(node), label=f'Attribute \n name: {node.attr}', shape='s', fillcolor='#F7FC5C', style='filled')
        self.graph.add_edge(str(node), self.visit(node.value))
        return str(node)

    def visit_List(self, node):
        self.graph.add_node(str(node), label="List", fillcolor='#87F38B', style='filled')
        for num, item in enumerate(node.elts):
            self.graph.add_edge(str(node), self.visit(item), label=f'elem {num + 1}')
        return str(node)


    def visit_FunctionDef(self, node):
        self.graph.add_node(str(node), label=f'function name: {node.name}', shape='s', fillcolor='#E2A8F0', style='filled')
        self.graph.add_edge(str(node), self.visit_args(node.args.args))
        self.graph.add_edge(str(node), self.visit_body(node))
        return str(node)

    def visit_Return(self, node):
        self.graph.add_node(str(node), label="Return", shape='s', fillcolor='#F85A62', style='filled')
        self.graph.add_edge(str(node), self.visit(node.value))
        return str(node)


if __name__ == '__main__':
    ast_object = ast.parse(inspect.getsource(fibonacci))
    print(ast.dump(ast_object))
    p = ASTVisitor()
    p.visit(ast_object)
    networkx.drawing.nx_pydot.to_pydot(p.graph).write_png("artifacts/ast.png")

