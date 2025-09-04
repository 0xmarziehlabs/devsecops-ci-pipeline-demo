from src.app import hello, insecure_eval

def test_hello():
    assert hello("Tester") == "Hello, Tester!"

def test_insecure_eval_demo():
    # For demo purposes only. Using a benign expression:
    assert insecure_eval("1 + 1") == 2

if __name__ == "__main__":
    test_hello()
    test_insecure_eval_demo()
    print("Tests passed!")