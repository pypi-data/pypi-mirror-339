import os
import subprocess

def execute_c_code(algorithm_code, args):
    """
    Generate, compile, and execute C code.

    Args:
        algorithm_code (str): The C code for the algorithm.
        args (any): The arguments to pass to the algorithm.

    Returns:
        The result of the algorithm execution.
    """
    c_code_template = """
    #include <stdio.h>

    int main() {{
        {args_declaration}
        double result = 0;
        {algorithm_code}
        printf("%.0f\\n", result);  // Format output to remove unnecessary decimals
        return 0;
    }}
    """

    # Generate the C declaration for args
    if isinstance(args, list) and len(args) > 0:
        args_declaration = f"double args = {float(args[0])};"
        # Replace "args" in the algorithm code with "args[0]" only if it's used as a scalar
        algorithm_code = algorithm_code
    elif isinstance(args, (int, float)):
        args_declaration = f"double args = {args};"
    else:
        raise ValueError("The args must be a number or a non-empty list of numbers.")

    # Generate the C code
    c_code = c_code_template.format(args_declaration=args_declaration, algorithm_code=algorithm_code)

    # Create a temporary directory for the C file and executable
    temp_dir = os.path.join(os.getcwd(), ".temp_c")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    c_file = os.path.join(temp_dir, "algorithm.c")
    exe_file = os.path.join(temp_dir, "algorithm.exe")

    try:
        # Write the C code to a temporary file
        with open(c_file, 'w') as f:
            f.write(c_code)

        # Compile the C code into an executable
        subprocess.run(
            ["gcc", c_file, "-o", exe_file],
            capture_output=True,
            text=True,
            check=True
        )

        # Execute the compiled executable
        execute_process = subprocess.run(
            [exe_file],
            capture_output=True,
            text=True,
            check=True
        )

        # Return the result from the executable
        return execute_process.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"C execution failed: {e.stderr.strip()}")
    finally:
        # Clean up temporary files
        if os.path.exists(c_file):
            os.remove(c_file)
        if os.path.exists(exe_file):
            os.remove(exe_file)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
