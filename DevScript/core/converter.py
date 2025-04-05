import os
import google.generativeai as genai
import re
import appdirs
import json

def _get_api_key():
    # Look for API key in different locations in this order:
    # 1. Environment variable
    # 2. User config directory
    # 3. If not found, guide the user to set it up
    
    # Check environment variable
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        return api_key
    
    # Check config file
    config_dir = appdirs.user_config_dir("devscript")
    config_file = os.path.join(config_dir, "config.json")
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                if 'api_key' in config:
                    return config['api_key']
        except:
            pass
    
    # If we get here, no API key was found
    print("⚠️ API key not found. Please set up DevScript with 'devscript-setup' command")
    return None

def _get_model_name():
    # Get model name from environment or config, default to gemini-2.0-flash
    model = os.getenv("GOOGLE_MODEL")
    
    if not model:
        # Check config file
        config_dir = appdirs.user_config_dir("devscript")
        config_file = os.path.join(config_dir, "config.json")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    if 'model' in config:
                        model = config['model']
            except:
                pass
    
    return model or "gemini-2.0-flash"

def convert_ds_to_python(ds_code):
    # Get API key securely
    api_key = _get_api_key()
    if not api_key:
        raise ValueError("API key not configured. Run 'devscript-setup' to configure.")
        
    # Configure the API
    genai.configure(api_key=api_key)
    
    prompt = f"""
You are a DevScript-to-Python converter. Your ONLY job is to translate DevScript code to valid Python code.

IMPORTANT RULES:
1. ONLY output valid Python code, nothing else
2. NO explanations, comments, markdown formatting, or additional text
3. DO NOT include ```python or ``` markers
4. DO NOT say things like "Here's the Python code:" or "The Python equivalent is:"
5. Just output clean, executable Python code

DevScript:
{ds_code}

Python (ONLY CODE, NO OTHER TEXT):
"""
    model = genai.GenerativeModel(_get_model_name())
    response = model.generate_content(prompt)
    
    # Get the response text
    code = response.text.strip()
    
    # Remove markdown code blocks if present
    code = re.sub(r'^```python\s*', '', code, flags=re.MULTILINE)
    code = re.sub(r'^```\s*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'^```\s*', '', code, flags=re.MULTILINE)
    
    # Remove explanatory text that might appear at the beginning
    lines = code.split('\n')
    clean_lines = []
    started_code = False
    
    for line in lines:
        # Skip explanatory text at the beginning
        if not started_code:
            # Skip lines that look like explanations
            if line.startswith('Here') or line.startswith('This') or line.startswith('The Python') or line.startswith('I') or line.startswith('Okay'):
                continue
            # Skip empty lines at the beginning
            if not line.strip():
                continue
            # We've found the start of the code
            started_code = True
        
        # Once we've started collecting code, stop if we hit explanatory text
        if started_code and (line.startswith('This code') or line.startswith('The above') or line.startswith('This Python')):
            break
            
        if started_code:
            clean_lines.append(line)
    
    # If we have clean lines, join them
    if clean_lines:
        return '\n'.join(clean_lines)
    
    # If our cleaning failed, return the original but with some basic cleanup
    return code