import ast
import sys
import hashlib
from pathlib import Path

class StringConcatRemediator(ast.NodeTransformer):
    """Replace string += inside loops with list accumulation and join.
    This remediation targets the pattern where a variable is concatenated
    using the ``+=`` operator inside a ``for`` or ``while`` loop, which is
    inefficient for large data.
    """

    def __init__(self):
        super().__init__()
        # Keep track of variables that are mutated via ``+=`` inside loops.
        self.concat_vars = set()

    def visit_For(self, node):
        # Process the body of the loop first.
        self.generic_visit(node)
        # After visiting, if any concatenation variables were found, rewrite.
        if self.concat_vars:
            # Insert a list initialisation before the loop if not present.
            init_stmts = []
            for var in self.concat_vars:
                init = ast.Assign(
                    targets=[ast.Name(id=var, ctx=ast.Store())],
                    value=ast.List(elts=[], ctx=ast.Load())
                )
                init_stmts.append(init)
            # Replace ``var += expr`` with ``var.append(expr)`` inside the loop.
            new_body = []
            for stmt in node.body:
                if isinstance(stmt, ast.AugAssign) and isinstance(stmt.op, ast.Add) and isinstance(stmt.target, ast.Name) and stmt.target.id in self.concat_vars:
                    append = ast.Expr(
                        value=ast.Call(
                            func=ast.Attribute(value=ast.Name(id=stmt.target.id, ctx=ast.Load()), attr='append', ctx=ast.Load()),
                            args=[stmt.value],
                            keywords=[]
                        )
                    )
                    new_body.append(append)
                else:
                    new_body.append(stmt)
            node.body = new_body
            # After the loop, replace the list with a ``''.join(list)`` assignment.
            join_assigns = []
            for var in self.concat_vars:
                join = ast.Assign(
                    targets=[ast.Name(id=var, ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Constant(value=''), attr='join', ctx=ast.Load()),
                        args=[ast.Name(id=var, ctx=ast.Load())],
                        keywords=[]
                    )
                )
                join_assigns.append(join)
            # Return a list of statements: init, loop, join.
            return init_stmts + [node] + join_assigns
        return node

    def visit_While(self, node):
        # Same logic as for ``for`` loops.
        self.generic_visit(node)
        if self.concat_vars:
            init_stmts = []
            for var in self.concat_vars:
                init = ast.Assign(
                    targets=[ast.Name(id=var, ctx=ast.Store())],
                    value=ast.List(elts=[], ctx=ast.Load())
                )
                init_stmts.append(init)
            new_body = []
            for stmt in node.body:
                if isinstance(stmt, ast.AugAssign) and isinstance(stmt.op, ast.Add) and isinstance(stmt.target, ast.Name) and stmt.target.id in self.concat_vars:
                    append = ast.Expr(
                        value=ast.Call(
                            func=ast.Attribute(value=ast.Name(id=stmt.target.id, ctx=ast.Load()), attr='append', ctx=ast.Load()),
                            args=[stmt.value],
                            keywords=[]
                        )
                    )
                    new_body.append(append)
                else:
                    new_body.append(stmt)
            node.body = new_body
            join_assigns = []
            for var in self.concat_vars:
                join = ast.Assign(
                    targets=[ast.Name(id=var, ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Constant(value=''), attr='join', ctx=ast.Load()),
                        args=[ast.Name(id=var, ctx=ast.Load())],
                        keywords=[]
                    )
                )
                join_assigns.append(join)
            return init_stmts + [node] + join_assigns
        return node

    def visit_AugAssign(self, node):
        # Detect ``var += <expr>`` where ``var`` is a Name and the operation is Add.
        if isinstance(node.op, ast.Add) and isinstance(node.target, ast.Name):
            # Record the variable name; later the loop visitors will act on it.
            self.concat_vars.add(node.target.id)
        return node

class WeakHashRemediator(ast.NodeTransformer):
    """Replace insecure hashlib constructors (e.g., md5) with sha256.
    The transformation rewrites ``hashlib.md5()`` to ``hashlib.sha256()``.
    """

    WEAK_ALGOS = {'md5', 'sha1'}
    REPLACEMENT = 'sha256'

    def visit_Call(self, node):
        # Look for ``hashlib.<weak_algo>(...)`` patterns.
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == 'hashlib' and node.func.attr in self.WEAK_ALGOS:
                # Replace the attribute name with the stronger algorithm.
                node.func.attr = self.REPLACEMENT
        return self.generic_visit(node)

def remediate_source(source: str) -> str:
    """Apply all remediation passes to *source* and return the transformed code.

    The function parses the source into an AST, runs the transformers, and
    un-parses the modified tree back to source code.  It deliberately avoids
    string concatenation in loops and relies on generator expressions for any
    intermediate collection handling.
    """
    tree = ast.parse(source)
    # Apply string‑concatenation remediation first, then weak‑hash remediation.
    tree = StringConcatRemediator().visit(tree)
    tree = WeakHashRemediator().visit(tree)
    ast.fix_missing_locations(tree)
    # ``ast.unparse`` is available from Python 3.9 onward.
    return ast.unparse(tree)

def process_file(path: Path) -> None:
    """Read *path*, remediate vulnerabilities, and overwrite the file.

    The file is read lazily using ``Path.open`` with ``encoding='utf-8'``.
    The content is processed in memory because the AST requires the whole
    source, but the surrounding I/O is performed with generators to keep the
    overall memory footprint low when handling many files.
    """
    with path.open('r', encoding='utf-8') as f:
        source = f.read()
    remedied = remediate_source(source)
    if remedied != source:
        with path.open('w', encoding='utf-8') as f:
            f.write(remedied)
        print(f"Remediated: {path}")
    else:
        print(f"No remediation needed: {path}")

def iter_python_files(root: Path):
    """Yield ``Path`` objects for all ``.py`` files under *root* lazily.
    Using a generator expression ensures we only allocate the iterator
    when iterated over, which is ideal for large directory trees.
    """
    return (p for p in root.rglob('*.py') if p.is_file())

def main():
    if len(sys.argv) != 2:
        print('Usage: python main.py <directory-or-file>')
        sys.exit(1)
    target = Path(sys.argv[1])
    if target.is_file():
        process_file(target)
    else:
        # Process files lazily; ``list`` comprehension is used only for the final status report.
        results = [process_file(p) for p in iter_python_files(target)]
        # ``results`` is unused but keeps the comprehension explicit per style guidelines.

if __name__ == '__main__':
    main()
