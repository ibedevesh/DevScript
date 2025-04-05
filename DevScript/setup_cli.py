import os
import json
import appdirs
import getpass
import sys

def main():
    print("🔧 DevScript Setup")
    print("-----------------")
    print("This utility will help you set up DevScript with your API key.")
    print("You need a Google AI Studio API key to use DevScript.")
    print("Get your API key from: https://aistudio.google.com/app/apikey")
    print()
    
    # Get API key
    api_key = getpass.getpass("Enter your Google AI Studio API key: ")
    if not api_key:
        print("⚠️ API key is required. Setup aborted.")
        return 1
    
    # Get model name (optional)
    model = input("Enter model name (default: gemini-2.0-flash): ")
    if not model:
        model = "gemini-2.0-flash"
    
    # Create config directory
    config_dir = appdirs.user_config_dir("devscript")
    os.makedirs(config_dir, exist_ok=True)
    
    # Save config
    config_file = os.path.join(config_dir, "config.json")
    config = {
        "api_key": api_key,
        "model": model
    }
    
    with open(config_file, 'w') as f:
        json.dump(config, f)
    
    print(f"✅ Setup complete! Configuration saved to {config_file}")
    print("You can now run DevScript with 'devscript your_file.ds'")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())