import sys
import argparse
import os
import pathlib
from .core.converter import convert_ds_to_python
from .core.executor import run_python_code
from .core.dependency_manager import get_imports_from_code, install_missing_packages

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="DevScript - AI-powered coding language")
    parser.add_argument("file", help="Path to the .ds file to execute")
    parser.add_argument("--show-python", action="store_true", help="Show the generated Python code")
    parser.add_argument("--dry-run", action="store_true", help="Don't execute the code, just convert it")
    parser.add_argument("--no-save", action="store_true", help="Don't save the generated Python code")
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        with open(args.file, "r") as f:
            ds_code = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{args.file}' not found")
        return 1
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 1

    print("🔁 Converting DevScript to Python...")
    py_code = convert_ds_to_python(ds_code)

    # Save the generated Python code
    if not args.no_save:
        # Create the generated_py directory if it doesn't exist
        os.makedirs("generated_py", exist_ok=True)
        
        # Get the filename without path and extension
        ds_filename = os.path.basename(args.file)
        py_filename = os.path.splitext(ds_filename)[0] + ".py"
        py_filepath = os.path.join("generated_py", py_filename)
        
        # Save the Python code
        with open(py_filepath, "w") as f:
            f.write(py_code)
        
        print(f"💾 Saved Python code to: {py_filepath}")

    if args.show_python or args.dry_run:
        print("\n✅ Generated Python:\n")
        print(py_code)
    
    # Detect and install required packages
    required_packages = get_imports_from_code(py_code)
    if required_packages:
        print(f"\n📦 Required packages: {', '.join(required_packages)}")
        if not args.dry_run:
            installed_packages = install_missing_packages(required_packages)
            if installed_packages:
                print(f"✅ Installed packages: {', '.join(installed_packages)}")
            else:
                print("✅ All required packages already installed.")

    if not args.dry_run:
        print("\n🚀 Running Python Code:\n")
        run_python_code(py_code)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
