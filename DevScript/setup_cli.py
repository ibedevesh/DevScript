import os
import json
import appdirs
import getpass
import sys
import argparse

def clean_api_key(api_key):
    """Clean the API key by removing whitespace, quotes, etc."""
    if not api_key:
        return api_key
    # Only strip whitespace but preserve the key exactly as entered
    return api_key.strip()

def create_env_file(api_key, model, location=None):
    """Create a .env file with the API key and model"""
    # Determine the location for the .env file
    if location is None:
        location = os.getcwd()
    
    env_path = os.path.join(location, '.env')
    
    # Create the .env file using the most basic file writing possible
    with open(env_path, 'w') as f:
        # Write each line separately with no formatting
        f.write("GOOGLE_API_KEY=" + api_key + "\n")
        f.write("GOOGLE_MODEL=" + model + "\n")
    
    return env_path

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="DevScript Setup Utility")
    parser.add_argument("--update-key", action="store_true", help="Update only the API key")
    parser.add_argument("--update-model", action="store_true", help="Update only the model name")
    parser.add_argument("--show-config", action="store_true", help="Show current configuration")
    parser.add_argument("--debug", action="store_true", help="Show debug information")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Config directory
    config_dir = appdirs.user_config_dir("devscript")
    config_file = os.path.join(config_dir, "config.json")
    
    # Show current configuration
    if args.show_config:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    print("Current configuration:")
                    print(f"Model: {config.get('model', 'Not set')}")
                    if 'api_key' in config and config['api_key']:
                        # Show first 4 chars and last 4 chars with stars in between
                        key = config['api_key']
                        masked_key = key[:4] + '*' * (len(key) - 8) + key[-4:] if len(key) > 8 else '****'
                        print(f"API key: {masked_key}")
                    else:
                        print("API key: Not set")
                    print(f"Config file: {config_file}")
                    
                    # Check if .env exists
                    env_path = os.path.join(os.getcwd(), '.env')
                    if os.path.exists(env_path):
                        print(f".env file: {env_path} (exists)")
                    else:
                        print(f".env file: Not found in current directory")
                return 0
            except:
                print(f"⚠️ Error reading config file: {config_file}")
                return 1
        else:
            print("⚠️ No configuration found. Run 'devscript-setup' to configure.")
            return 1
    
    # Load existing config if it exists
    existing_config = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                existing_config = json.load(f)
        except:
            pass
    
    # If updating only API key
    if args.update_key:
        print("🔑 Update API Key")
        print("--------------")
        api_key = getpass.getpass("Enter your new Google AI Studio API key: ")
        if not api_key:
            print("⚠️ API key is required. Update aborted.")
            return 1
        
        # Clean the API key
        api_key = clean_api_key(api_key)
        
        # Update only the API key
        existing_config['api_key'] = api_key
        
        # Save config
        os.makedirs(config_dir, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(existing_config, f)
        
        # Update .env file if it exists
        env_path = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_path):
            model = existing_config.get('model', 'gemini-2.0-flash')
            create_env_file(api_key, model)
            print(f"✅ Updated .env file with new API key at: {env_path}")
        else:
            # Create new .env file
            model = existing_config.get('model', 'gemini-2.0-flash')
            env_path = create_env_file(api_key, model)
            print(f"✅ Created .env file at: {env_path}")
        
        print("✅ API key updated successfully!")
        return 0
    
    # If updating only model
    if args.update_model:
        print("🤖 Update Model")
        print("------------")
        model = input("Enter new model name (default: gemini-2.0-flash): ")
        if not model:
            model = "gemini-2.0-flash"
        
        # Update only the model
        existing_config['model'] = model
        
        # Save config
        os.makedirs(config_dir, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(existing_config, f)
        
        # Update .env file if it exists
        env_path = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_path):
            api_key = existing_config.get('api_key', '')
            create_env_file(api_key, model)
            print(f"✅ Updated .env file with new model at: {env_path}")
        else:
            # Create new .env file
            api_key = existing_config.get('api_key', '')
            if api_key:
                env_path = create_env_file(api_key, model)
                print(f"✅ Created .env file at: {env_path}")
        
        print(f"✅ Model updated to: {model}")
        return 0
    
    # Full setup
    print("🔧 DevScript Setup")
    print("-----------------")
    print("This utility will help you set up DevScript with your API key.")
    print("You need a Google AI Studio API key to use DevScript.")
    print("Get your API key from: https://aistudio.google.com/app/apikey")
    print()
    
    # Get API key
    print("Enter your Google AI Studio API key:")
    api_key = getpass.getpass()
    if not api_key:
        print("⚠️ API key is required. Setup aborted.")
        return 1

    # Clean the API key (just trim whitespace)
    api_key = api_key.strip()

    # Show confirmation
    print(f"API key received (length: {len(api_key)}, first 4 chars: {api_key[:4]}...)")

    # Add this after getting the API key
    print("API Key Diagnostics:")
    print(f"- Length: {len(api_key)}")
    print(f"- First 4 chars: {api_key[:4]}")
    print(f"- Last 4 chars: {api_key[-4:]}")
    print(f"- ASCII values of first 5 chars: {[ord(c) for c in api_key[:5]]}")

    # Create .env file first to ensure it works
    env_path = os.path.join(os.getcwd(), '.env')
    try:
        # Write directly to the file without using a function
        with open(env_path, 'w') as f:
            f.write("GOOGLE_API_KEY=" + api_key + "\n")
            f.write("GOOGLE_MODEL=gemini-2.0-flash\n")
        
        # Verify it was written correctly
        with open(env_path, 'r') as f:
            content = f.read()
            if "GOOGLE_API_KEY=" + api_key not in content:
                print("⚠️ Warning: API key may not have been written correctly.")
            else:
                print("✅ API key written correctly to .env file")
    except Exception as e:
        print(f"⚠️ Error creating .env file: {str(e)}")

    # Get model name (optional)
    model = input("Enter model name (default: gemini-2.0-flash): ")
    if not model:
        model = "gemini-2.0-flash"
    
    # Save config
    os.makedirs(config_dir, exist_ok=True)
    config = {
        "api_key": api_key,
        "model": model
    }
    
    with open(config_file, 'w') as f:
        json.dump(config, f)
    
    # Also create a .env file in the current directory
    env_path = create_env_file(api_key, model)
    
    print(f"✅ Setup complete!")
    print(f"✅ Configuration saved to: {config_file}")
    print(f"✅ Created .env file at: {env_path}")
    print(f"   You can edit this file directly to update your API key.")
    print("You can now run DevScript with 'devscript your_file.ds'")
    
    if args.debug:
        print("Debug Information:")
        print("-----------------")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    if 'api_key' in config:
                        key = config['api_key']
                        print(f"Config API key: {key[:4]}...{key[-4:]} (length: {len(key)})")
            except Exception as e:
                print(f"Error reading config: {str(e)}")
        
        env_path = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_path):
            try:
                with open(env_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith('GOOGLE_API_KEY='):
                            key_part = line.split('=', 1)[1].strip()
                            print(f".env API key: {key_part[:4]}...{key_part[-4:]} (length: {len(key_part)})")
            except Exception as e:
                print(f"Error reading .env: {str(e)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
