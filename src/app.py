def hello(name: str) -> str:
    return f"Hello, {name}!"

# ❗ INTENTIONAL VULNERABILITY (for training/demo only)
def insecure_eval(user_input: str):
    """
    DO NOT USE IN PRODUCTION.
    This function intentionally uses eval() to demonstrate how SAST (Semgrep) can catch unsafe patterns.
    """
    return eval(user_input)  # unsafe by design


if __name__ == "__main__":
    print(hello("World"))
