import subprocess
import tempfile
import os
import re

def contains_input_function(code):
    """Check if the code contains input() function calls"""
    return 'input(' in code

def run_python_code(py_code):
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w') as temp:
        temp.write(py_code)
        temp.flush()
        temp_name = temp.name
    
    try:
        # Check if the code contains input() functions
        is_interactive = contains_input_function(py_code)
        
        if is_interactive:
            # For interactive code, run without capturing output
            # This allows the user to interact with the program
            print("⚠️ This program requires user input. Running in interactive mode...\n")
            subprocess.run(["python", temp_name], check=False)
        else:
            # For non-interactive code, capture the output
            result = subprocess.run(["python", temp_name], 
                                  capture_output=True, 
                                  text=True, 
                                  check=False)
            
            # Print stdout if there is any
            if result.stdout:
                print(result.stdout)
            
            # Print stderr if there is any
            if result.stderr:
                print("Error:", result.stderr)
            
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_name):
            os.unlink(temp_name)