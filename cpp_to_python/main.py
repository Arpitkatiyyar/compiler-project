import os
import re
from parser import parser
from codegen import CodeGenerator

# Natural sort key (so test10 comes after test9, not after test1)
def natural_key(filename):
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r'(\d+)', filename)
    ]

def convert_cpp_to_python(input_path, output_path):
    """Convert a single C++ file into a Python file."""
    with open(input_path, "r", encoding="utf-8") as f:
        cpp_code = f.read()

    # Parse C++ to AST
    ast = parser.parse(cpp_code)

    # Generate Python code
    gen = CodeGenerator()
    py_code = gen.generate(ast)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(py_code)

    print(f"[OK] Converted: {input_path} -> {output_path}")


def main():
    test_folder = "tests"
    output_folder = "output"

    # Create output directory if needed
    os.makedirs(output_folder, exist_ok=True)

    # Get only .cpp files and sort them naturally
    cpp_files = sorted(
        (f for f in os.listdir(test_folder) if f.endswith(".cpp")),
        key=natural_key
    )

    if not cpp_files:
        print("No .cpp files found in 'tests/' folder.")
        return

    # Convert each file in correct order
    for index, filename in enumerate(cpp_files, start=1):
        input_path = os.path.join(test_folder, filename)
        output_path = os.path.join(output_folder, f"output{index}.py")

        convert_cpp_to_python(input_path, output_path)

    print("\nAll files converted successfully!")
    print("Check the 'output/' folder.")


if __name__ == "__main__":
    main()
