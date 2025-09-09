# src/app.py
import ast

def hello(name: str) -> str:
    return f"Hello, {name}!"

def safe_eval_literal(expr: str):
    """
    Safe alternative for demo:
    Only evalutes python *literals* (numbers, strings, tuples, lists, dicts, booleans, None).
    This avoids executing arbitary code (no expressions, no function calls).
    """
    return ast.literal_eval(expr)


if __name__ == "__main__":
    print(hello("World"))
