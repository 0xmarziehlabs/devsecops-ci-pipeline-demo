# tests/test_app.py
from src.app import hello, safe_eval_literal

def test_hello():
    assert hello("Tester") == "Hello, Tester!"

def test_safe_eval_literal_demo():
    # For demo purposes only. Using a benign expression:
    assert safe_eval_literal("2") == 2    ## literal number
    assert safe_eval_literal("[1,2]") ==[1,2]  ## literal list

if __name__ == "__main__":
    test_hello()
    test_safe_eval_literal_demo()
    print("Tests passed!")