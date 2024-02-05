import base64
import os
import time
import socket
import argparse
from openai import AzureOpenAI, OpenAI, RateLimitError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import subprocess
import re
import json
import time
import tiktoken
from openai import BadRequestError


import json
import os

config_file = 'config.json'
if not os.path.exists(config_file):
    mode = input("Which mode do you want to use? (OpenAI/Azure/Local): ")
    if mode.lower() == "openai":
        OPENAI_API_KEY = input("Enter your OpenAI API Key: ")
        config = {
            "MODE": "OpenAI",
            "OPENAI_API_KEY": OPENAI_API_KEY,
            "MODEL": "gpt4-turbo-preview",
            "VISION_MODEL": "gpt4-vision-preview"
        }
    elif mode.lower() == "local":
        OPENAI_BASE_URL = input("Enter your local http endpoint: ")
        config = {
            "MODE": "Local",
            "BASE_URL": OPENAI_BASE_URL,
            "MODEL": "doesnt-matter",
            "VISION_MODEL": "doesnt-matter",
            "MAX_TEMP": 0.7,
            "USE_INSTRUCT": 1,
        }
    else:
        AZURE_OPENAI_KEY = input("Enter your Azure OpenAI Key: ")
        AZURE_OPENAI_VERSION = input("Enter your Azure OpenAI Version: ")
        AZURE_OPENAI_ENDPOINT = input("Enter your Azure OpenAI Endpoint: ")
        AZURE_OPENAI_MODEL = input("Enter your Azure OpenAI Model: ")
        AZURE_OPENAI_VISION_MODEL = input("Enter your Azure OpenAI Vision Model: ")
        config = {
            "MODE": "Azure",
            "AZURE_OPENAI_KEY": AZURE_OPENAI_KEY,
            "AZURE_OPENAI_VERSION": AZURE_OPENAI_VERSION,
            "AZURE_OPENAI_ENDPOINT": AZURE_OPENAI_ENDPOINT,
            "MODEL": AZURE_OPENAI_MODEL,
            "VISION_MODEL": AZURE_OPENAI_VISION_MODEL
        }
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
else:
    with open(config_file, 'r') as f:
        config = json.load(f)

if config["MODE"] == "OpenAI":
    client = OpenAI(
        api_key=config["OPENAI_API_KEY"]
    )
elif config["MODE"] == "Local":
    client = OpenAI(
        base_url=config["BASE_URL"],
        api_key="doesntmatter"
    )
else:
    client = AzureOpenAI(
        api_key=config["AZURE_OPENAI_KEY"],
        api_version=config["AZURE_OPENAI_VERSION"],
        azure_endpoint=config["AZURE_OPENAI_ENDPOINT"]
    )

def call_gpt(system_prompt, user_prompt, max_tokens=4092, temperature=0.9, top_p=0.9, frequency_penalty=0.0, presence_penalty=0.0):
  #if user prompt contains an object with "type" "image_url", set use_vision to True
  use_vision = False
  if any(item["type"] == "image_url" for item in user_prompt):
        use_vision = True
  enc = tiktoken.encoding_for_model("gpt-4")
  encoded = enc.encode(system_prompt + get_content_from_text_object_array(user_prompt))
  total_tokens = len(encoded)


  if config.get("MAX_TEMP") and temperature > config["MAX_TEMP"]:
    temperature = config["MAX_TEMP"]

  compiled_messages = [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": system_prompt}
                    ],
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]

  if config["MODE"] == "Local":
    
    prompt_text = user_prompt if isinstance(user_prompt, str) else get_content_from_text_object_array(user_prompt)
    
    if config.get("USE_INSTRUCT") and config["USE_INSTRUCT"] == 1:
        prompt_text = "[INST] " + prompt_text + " [/INST]"

    compiled_messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt_text,
                }
            ]

  print(f"Calling GPT {"with vision" if use_vision else "without vision"} with total (text) tokens: {total_tokens}")
  max_retries = 5
  for i in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=config["VISION_MODEL"] if use_vision else config["MODEL"],
                messages=compiled_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
            )
            return response
        except RateLimitError:
            time.sleep(61)
        except BadRequestError:
            if i < max_retries - 1:  # no need to sleep for the last iteration
                print(f"Error: Bad Request. Retrying in {2 ** i} seconds...")
                sleep_time = 2 ** i  # exponential backoff
                time.sleep(sleep_time)
            else:
                raise

  return response

def check_port_in_use(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return False
    except socket.error:
        return True

def start_npm(web_directory):
    os.chdir(web_directory)
    os.system('npm start')

def take_screenshot(url, screenshot_path):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1024, 768)  # Set the width to 1024 and the height to 768
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    driver.save_screenshot(screenshot_path)
    driver.quit()

def take_and_encode_screenshot(screenshot_url: str) -> str:
    screenshot_directory = "./working"
    screenshot_path = f"{screenshot_directory}/screen.png"

    # Check if the screenshot directory exists, create it if it doesn't
    if not os.path.exists(screenshot_directory):
        os.makedirs(screenshot_directory)

    # Check if screenshot_path already exists and delete it if it does
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)

    # Take the screenshot
    take_screenshot(screenshot_url, screenshot_path)

    # Check if screenshot_path exists before calling encode_image
    if os.path.exists(screenshot_path):
        # Getting the base64 string
        base64_screen = encode_image(screenshot_path)
        return base64_screen
    else:
        print("Error: screenshot failed")
        return None


def get_npm_errors():
    try:
        
        # Load the configuration file
        with open('cgconfig.json') as config_file:
            config = json.load(config_file)
        print(f"Running tsc (typescript compiler) to check for errors in {config["root_dir"]}")
        output = subprocess.check_output(['npm.cmd', 'run', 'checkbuild'], cwd=config["root_dir"], stderr=subprocess.STDOUT, universal_newlines=True)

        if "error" in output.lower():
            return output.strip()
        else:
            return None
    except subprocess.CalledProcessError as e:
        return e.output.strip()

def main(url, port, web_directory, screenshot_path):
    while check_port_in_use(port):
        start_npm(web_directory)
        time.sleep(1)
    
    take_screenshot(url, screenshot_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Take a screenshot of a web page.')
    parser.add_argument('--url', type=str, required=True, help='The URL of the web page.')
    parser.add_argument('--port', type=int, required=True, help='The port to check.')
    parser.add_argument('--web_directory', type=str, required=True, help='The directory of the web application.')
    parser.add_argument('--screenshot_path', type=str, required=True, help='The path to save the screenshot.')
    args = parser.parse_args()

    main(args.url, args.port, args.web_directory, args.screenshot_path)

def display_response(response):
    print(response.choices[0].message.content)
    print(f"\n{response.usage.prompt_tokens} Prompt Tokens used")
    print(f"{response.usage.completion_tokens} Completion Tokens used")
    print(f"{response.usage.total_tokens} Total Tokens used")

    # Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def strip_content(list):
    output = ""
    # Iterate through each list item
    for item in list:
        # Check if the item is of type "text"
        print(item)
        if item["type"] == "text":
            # Strip the string content
            output += strip_string_content(item["text"])
            output += "\n"
    return output

def get_content_from_text_object_array(list):
    output = ""
    # Iterate through each list item
    for item in list:
        # Check if the item is of type "text"
        print(item)
        if item["type"] == "text":
            # Strip the string content
            output += item["text"]
            output += "\n"
    return output


def strip_string_content(string):
    
    # Remove base64 content
    string = re.sub(r'[A-Za-z0-9+/]{100,}', '*** base64 redacted***', string)
    
    # Remove file contents
    string = re.sub(r'Contents:\n.*?\[EOF\]', '*** file contents redacted***', string, flags=re.DOTALL)
    
    return string



def filter_command_output(command_output):
    # Define the patterns to search for
    patterns = [
        r'^python \./cg_update_fix\.py .*',
        r'^python \./cg_error_fix\.py .*',
        r'^python \./cg_new_file\.py .*',
        r'^python \./cg_comparison_fix\.py .*',
        r'^yarn add .*',
    ]

    # Split the command output into lines
    lines = command_output.split('\n')

    # Initialize an empty set to hold the unique matching lines
    unique_lines = set()

    # Check each line for a match with any of the patterns
    for line in lines:
            if any(re.match(pattern, line) for pattern in patterns):
                    unique_lines.add(line)

    # Join the unique lines back into a single string
    filtered_command_output = '\n'.join(unique_lines)

    return filtered_command_output
