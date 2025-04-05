import ast
import subprocess
import sys
import importlib

def get_imports_from_code(code):
    """
    Parse Python code and extract all imported modules.
    
    Args:
        code (str): Python code to analyze
        
    Returns:
        list: List of top-level package names
    """
    try:
        tree = ast.parse(code)
        modules = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    # Get the top-level package name (before any dots)
                    modules.add(n.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Get the top-level package name (before any dots)
                    modules.add(node.module.split('.')[0])

        # Filter out standard library modules
        non_stdlib_modules = [
            module for module in modules 
            if module not in sys.builtin_module_names and module != 'builtins'
        ]
        
        return list(non_stdlib_modules)
    except SyntaxError:
        # If code can't be parsed, return empty list
        return []

def is_package_installed(package_name):
    """Check if a package is already installed."""
    try:
        importlib.import_module(package_name)
        return True
    except (ImportError, ValueError):
        # ValueError can occur with binary incompatibility issues
        return False

def install_missing_packages(packages):
    """
    Install missing packages using pip.
    
    Args:
        packages (list): List of package names to install if missing
        
    Returns:
        list: List of packages that were installed
    """
    installed = []
    
    # Define compatible versions for common packages
    package_versions = {
        'pandas': 'pandas==2.0.3',
        'numpy': 'numpy==1.24.3',
        'matplotlib': 'matplotlib==3.7.2',
        'seaborn': 'seaborn==0.12.2',
        'scikit-learn': 'scikit-learn==1.3.0',
        'tensorflow': 'tensorflow==2.13.0',
        'torch': 'torch==2.0.1',
    }
    
    for package in packages:
        if not is_package_installed(package):
            print(f"📦 Installing {package}...")
            try:
                # Use specific version if available, otherwise use latest
                install_target = package_versions.get(package, package)
                subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", install_target], 
                              check=True, capture_output=True)
                installed.append(package)
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Failed to install {package}: {e}")
    
    return installed