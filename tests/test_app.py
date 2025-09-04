from src.app import hello

def test_hello():
    assert hello("Tester") == "Hello, Tester!"

if __name__ == "__main__":
    test_hello()
    print("Test passed!")