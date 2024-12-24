import subprocess
import sys
import logging
import os
import click
import google.generativeai as genai

def save_api_key(key):
    key_file = os.path.expanduser("~/.gemini_api_key")
    try:
        with open(key_file, "w") as f:
            f.write(key)
        print("API key saved successfully.")
    except IOError as e:
        print(f"Error saving API key: {e}")

def load_api_key():
    key_file = os.path.expanduser("~/.gemini_api_key")
    try:
        with open(key_file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_show_code_state():
    show_code_state_file = os.path.expanduser("~/.code_preview")
    try:
        preview_state = None
        if os.path.exists(show_code_state_file):
            with open(show_code_state_file, 'r') as f:
                preview_state = f.read().strip()
        with open(show_code_state_file, 'w') as f:
            new_state = "disabled" if preview_state == "enabled" else "enabled"
            f.write(new_state)
    except IOError as e:
        print(f"Error toggling code preview state: {e}")

def load_show_code_state():
    show_code_state_file = os.path.expanduser("~/.code_preview")
    if os.path.exists(show_code_state_file):
        try:
            with open(show_code_state_file, "r") as f:
                return f.read().strip()
        except IOError as e:
            print(f"Error reading code preview state: {e}")
            return "enabled"
    else:
        print("Config file does not exist. Creating config file with 'Code Preview' enabled.")
        save_show_code_state()
        return 'enabled'

def install_missing_packages(packages, api_key):
    install_packages = []
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            if load_show_code_state() == "enabled":
                print(f"Package {package} is missing. Adding to the missing packages list...")
            install_packages.append(package)
    if install_packages:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        try:
            package_names = model.generate_content(
                f"You are an AI designed to map Python package names to their corresponding installation package names. For each package, provide the exact package name that can be used with pip for installation. Example: Input: cv2, qrcode. Output: opencv-python, qrcode. Now, process the following list: {install_packages}."
            ).text.replace('\n', '').strip()
            subprocess.check_call([sys.executable, "-m", "pip", "install", *package_names.split()])
        except Exception as e:
            print(f"Error installing packages: {e}")

@click.command()
@click.option("-p", "--prompt", required=False, help="User prompt to generate code.")
@click.option("-config", "--configure", required=False, help="Configure the Gemini API key.")
@click.option("-debug", "--switch_debug", is_flag=True, help="Switch 'Code Preview' function On/Off.")
def main(prompt, configure, switch_debug):
    if configure:
        save_api_key(configure)
        return

    if switch_debug:
        print("Switching 'Code Preview' state")
        save_show_code_state()
        print(f"New 'Code Preview' state is: {load_show_code_state()}")
        return

    api_key = load_api_key()
    if not api_key:
        print("API key not found. Please configure it using the -conf (or --configure) option.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    if prompt:
        try:
            code = model.generate_content(
                f"Generate Python code for the task: {prompt}. The code should be presented without comments, explanations, or formatting markers like `python`. Example of incorrect formatting: ```python CODE``` Correct formatting: CODE If debugging is necessary, include `print()` statements to show the state of the code. Do not include commands to install packages (e.g., 'pip install package_name')."
            ).text.strip().replace('```python','').replace('```','')

            if load_show_code_state() == "enabled":
                print("Generated Code:")
                print(code)

            safe_check = model.generate_content(
                f"Assess the safety of the following code for execution on my PC: {code}. Reply with 'safe' if the code is safe to execute. If it is not safe, reply with 'not safe'."
            ).text.strip()

            if load_show_code_state() == "enabled":
                print(safe_check)
            
            if safe_check == "safe":
                if load_show_code_state() == "enabled":
                    print("Code is safe to execute.")
                    print("Checking for missing packages...")

                required_packages = []
                for line in code.splitlines():
                    if line.startswith("import") or line.startswith("from"):
                        parts = line.split()
                        if "import" in parts:
                            required_packages.append(parts[1].split('.')[0])

                install_missing_packages(required_packages, api_key)

                if load_show_code_state() == "enabled":
                    print("Executing code...")
                try:
                    exec(code)
                except Exception as e:
                    print(f"Error while executing code: {e}")
            else:
                if load_show_code_state() == "enabled":
                    print("Code might not be safe to execute.")
        except Exception as e:
            print(f"Error generating or processing code: {e}")

if __name__ == "__main__":
    main()
