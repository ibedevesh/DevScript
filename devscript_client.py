#!/usr/bin/env python3
import argparse
import os
import requests
import json
import sys

CONFIG_DIR = os.path.expanduser("~/.devscript")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
# Remove trailing slash to ensure consistent URL construction
API_URL = os.environ.get("DEVSCRIPT_API_URL", "https://5ff7d937-f336-474e-8eef-0d124eb164d6-00-27jjzeunl02rz.pike.replit.dev").rstrip('/')

def setup_api_key():
    """Setup or update the user's API key"""
    print("🔧 DevScript API Setup")
    print("-----------------")
    print("Please enter your DevScript API key.")
    print("You can get your key at https://devscript.com/dashboard")
    print()
    
    api_key = input("Enter your DevScript API key: ")
    if not api_key:
        print("⚠️ API key is required.")
        return False
    
    # Verify the key is valid by making a test call
    try:
        print(f"Connecting to API at: {API_URL}/user/usage")
        response = requests.get(
            f"{API_URL}/user/usage",
            headers={"X-API-Key": api_key}
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code != 200:
            error_detail = "Invalid API key"
            try:
                error_detail = response.json().get('detail', error_detail)
            except:
                # In case the response is not valid JSON
                error_detail = response.text if response.text else error_detail
                
            print(f"⚠️ Error: {error_detail}")
            return False
            
        # Key is valid, save it
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump({"api_key": api_key}, f)
        
        try:    
            usage_data = response.json()
            print("✅ API key verified and saved!")
            print(f"Email: {usage_data.get('email', 'Not available')}")
            print(f"Subscription: {usage_data.get('subscription_type', 'Free')}")
            print(f"API calls: {usage_data.get('api_calls', 0)}")
            if 'renewal_date' in usage_data and usage_data['renewal_date']:
                print(f"Renewal date: {usage_data['renewal_date']}")
            return True
        except json.JSONDecodeError:
            print("Warning: Couldn't parse API response, but the API key was accepted.")
            print("Response:", response.text[:100] + "..." if len(response.text) > 100 else response.text)
            print("✅ API key saved!")
            return True
    
    except Exception as e:
        print(f"⚠️ Error connecting to DevScript API: {str(e)}")
        return False

def get_api_key():
    """Get the API key from config file"""
    if not os.path.exists(CONFIG_FILE):
        print("⚠️ No API key found. Please run 'devscript setup' first.")
        return None
        
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("api_key")
    except:
        print("⚠️ Error reading config file.")
        return None

def convert_devscript(file_path, options=None):
    """Convert a DevScript file to Python using the API"""
    api_key = get_api_key()
    if not api_key:
        return False
        
    try:
        # Verify file exists
        if not os.path.exists(file_path):
            print(f"⚠️ File not found: {file_path}")
            return False
            
        with open(file_path, "r") as f:
            code = f.read()
            
        print("🔄 Converting DevScript to Python...")
        
        # Call the API
        response = requests.post(
            f"{API_URL}/convert",
            headers={"X-API-Key": api_key},
            json={"code": code}  # Removed options parameter to match server's expectations
        )
        
        if response.status_code != 200:
            try:
                error = response.json().get('detail', 'API error')
            except:
                error = response.text or 'API error'
            print(f"⚠️ Error: {error}")
            return False
            
        try:
            result = response.json()
            
            # Save the Python code
            output_dir = os.path.join(os.getcwd(), "generated_py")
            os.makedirs(output_dir, exist_ok=True)
            
            py_filename = os.path.splitext(os.path.basename(file_path))[0] + ".py"
            py_filepath = os.path.join(output_dir, py_filename)
            
            python_code = result.get("python_code", "# No code generated")
            
            with open(py_filepath, "w") as f:
                f.write(python_code)
                
            print(f"✅ Converted DevScript to Python: {py_filepath}")
            
            # These fields might not exist in the current API response
            if "tokens_used" in result:
                print(f"Tokens used: {result['tokens_used']}")
            if "remaining_quota" in result:
                print(f"Remaining quota: {result['remaining_quota']}")
            
            return py_filepath
        except json.JSONDecodeError:
            print(f"⚠️ Error: Invalid JSON response from API")
            print(f"Response: {response.text[:200]}...")
            return False
    
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
        return False

def run_python_file(file_path):
    """Run a Python file"""
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return False
        
    print(f"🚀 Running Python code: {file_path}")
    print("-" * 40)
    os.system(f"python {file_path}")
    return True

def show_usage():
    """Show current usage statistics"""
    api_key = get_api_key()
    if not api_key:
        return False
        
    try:
        response = requests.get(
            f"{API_URL}/user/usage",
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code != 200:
            try:
                error = response.json().get('detail', 'API error')
            except:
                error = response.text or 'API error'
            print(f"⚠️ Error: {error}")
            return False
            
        try:
            usage = response.json()
            print("DevScript Usage Statistics:")
            print("--------------------------")
            print(f"Email: {usage.get('email', 'Not available')}")
            print(f"Subscription: {usage.get('subscription_type', 'Free')}")
            print(f"API calls: {usage.get('api_calls', 0)}")
            if 'renewal_date' in usage and usage['renewal_date']:
                print(f"Renewal date: {usage['renewal_date']}")
            print(f"Account status: {'Active' if usage.get('is_active', True) else 'Inactive'}")
            return True
        except json.JSONDecodeError:
            print(f"⚠️ Error: Invalid JSON response from API")
            print(f"Response: {response.text[:200]}...")
            return False
    
    except Exception as e:
        print(f"⚠️ Error connecting to DevScript API: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="DevScript Client")
    subparsers = parser.add_subparsers(dest="command")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup API key")
    
    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert DevScript to Python")
    convert_parser.add_argument("file", help="DevScript file to convert")
    convert_parser.add_argument("--run", action="store_true", help="Run the converted Python code")
    convert_parser.add_argument("--model", help="Specify the model to use (e.g., gemini-2.0-flash)")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Convert and run DevScript file")
    run_parser.add_argument("file", help="DevScript file to convert and run")
    
    # Usage command
    usage_parser = subparsers.add_parser("usage", help="Show API usage statistics")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_api_key()
    elif args.command == "convert":
        options = {}
        if args.model:
            options["model"] = args.model
            
        py_file = convert_devscript(args.file, options)
        if py_file and args.run:
            run_python_file(py_file)
    elif args.command == "run":
        py_file = convert_devscript(args.file)
        if py_file:
            run_python_file(py_file)
    elif args.command == "usage":
        show_usage()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()