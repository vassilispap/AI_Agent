from functions.run_python_file import run_python_file
import os

def test():

    result = run_python_file("calculator", "main.py")
    print("************************************************")
    print("Checking 'calculator', 'main.py' should print the calculator's usage instructions")
    print("************************************************")
    print(result)
    print("************************************************")
    
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("************************************************")
    print("Checking 'calculator', 'main.py', ['3 + 5'] should run the calculator... which gives a kinda nasty rendered result")
    print("************************************************")
    print(result)
    print("************************************************")
    
    result = run_python_file("calculator", "tests.py")
    print("************************************************")
    print("Checking 'calculator', 'tests.py' should run the calculator's tests successfully)")
    print("************************************************")
    print(result)
    print("************************************************")
    
    result = run_python_file("calculator", "../main.py")
    print("************************************************")
    print("Checking 'calculator', '../main.py' this should return an error")
    print("************************************************")
    print(result)
    print("************************************************")
    
    result = run_python_file("calculator", "nonexistent.py")
    print("************************************************")
    print("Checking 'calculator', 'nonexistent.py' this should return an error")
    print("************************************************")
    print(result)
    print("************************************************")
    
    result = run_python_file("calculator", "lorem.txt")
    print("************************************************")
    print("Checking 'calculator', 'lorem.txt' this should return an error")
    print("************************************************")
    print(result)
    print("************************************************")
    
if __name__ == "__main__":
    test()
