from openai import AzureOpenAI
import os
import sys
import base64
from build_prompt import build_orchestrator_prompt, build_system_prompt
from cg_utilities import call_gpt, display_response, encode_image, filter_command_output, get_npm_errors, strip_content, take_and_encode_screenshot
import argparse
import re
import json
from codegen import validate_complete, merge_contents

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--user_request", default="Your default user request")
parser.add_argument("--comp_path", required=False, help="Path to the composite image")
parser.add_argument("--screenshot_url", required=False, help="URL for taking the screenshot")
parser.add_argument("--skip_confirm", action='store_true', help="Skip confirmation before executing the orchestrated commands")
args = parser.parse_args()

with open('cgconfig.json') as config_file:
    config = json.load(config_file)

npm_build_output = get_npm_errors()
taskmaker_system_prompt = build_system_prompt("prompt_orchestrator.txt", args.user_request, npm_build_output)

# Getting the base64 string for the comp
base64_comp = encode_image(args.comp_path) if args.comp_path else None

# Take the screenshot if screenshot_url is provided
if args.screenshot_url:
  base64_screen = take_and_encode_screenshot(args.screenshot_url)
else:
  base64_screen = None

#user_prompt = build_compare_prompt(base64_screen, base64_comp, args.code_path, code_contents, args.user_request)
instruct_prompt = build_orchestrator_prompt(base64_screen, args.screenshot_url, base64_comp, args.comp_path, args.user_request, npm_build_output)

print(f"\nInstruct prompt: {strip_content(instruct_prompt)}")

print("Calling GPT4 Vision for instructions...")

response = call_gpt(taskmaker_system_prompt, instruct_prompt)

display_response(response)
response_content = response.choices[0].message.content

extract_regex = r'```(?:[Pp]owershell|[Bb]ash)\n(.*?)\n```'

# Find all the commands
matches = re.findall(extract_regex, response_content, re.DOTALL)

# Get the last match
file_content = matches[-1] if matches else ''

if file_content:
  print(f"Parsed File from GPT output:\n\n{file_content}\n\n")
  file_content = filter_command_output(file_content)
  print(f"Filtered File from GPT output:\n\n{file_content}\n\n")
else:
  print("Error: No file content found in response.")
  sys.exit(1)

# Ensure the directory exists
working_dir_name = './working'
if not os.path.exists(working_dir_name):
  os.makedirs(working_dir_name)

revised_file_content = ""
# Check for "yarn add ..." lines in file_content and cd to the web app directory before running the command
for line in file_content.split("\n"):
    if line.startswith("yarn"):
        revised_file_content += f"cd {config["root_dir"]}\n"
    revised_file_content += line + "\n"
    if line.startswith("yarn"):
        revised_file_content += "cd ../code-gen\n"

# Write the commands to a new PowerShell script
with open(os.path.join(working_dir_name, 'command.ps1'), 'w') as file:
  file.write(revised_file_content)

# Ask user if they wish to execute the orchestration command
if not args.skip_confirm:
  execute_orchestration = input("Do you wish to execute the orchestration command? (y/n): ")
else:
  execute_orchestration = 'y'

if execute_orchestration.lower() == 'y':
  # Run the PowerShell script
  command_output = os.system('powershell.exe -File ./working/command.ps1 > ./working/commandoutput.txt')
  print("Execution completed. Command output written to ./working/commandoutput.txt.")
else:
  print("Orchestration command not executed.")
  print("Location of the command file: ./working/command.ps1")
  sys.exit(0)

# Check for errors, ask for a fix providing the original instructions as guidance for what was being attempted.
errors = get_npm_errors()
# Check errors for the text "error"
if errors and "error" in errors:
  # We have an error
  # Ask for a fix providing the original instructions as guidance for what was being attempted.
  instruct_prompt = build_orchestrator_prompt(base64_screen, args.screenshot_url, base64_comp, args.comp_path, f"Intelligently fix the compilation failures shown in Typescript build output. These failures were the result of the following instructions having been previously executed:\n\n{response_content}\n[END PREVIOUS INSTRUCTIONS] \n\nPlease fix the error in a way that honors the original request and plan. If the plan was flawed to begin with, come up with a better plan by thinking step by step and then generating the necessary commands. ", npm_build_output)
else:
  exit()

print(f"\nErrors found in typescript build...\n\nAttempting to fix remaining errors...")
response = call_gpt(taskmaker_system_prompt, instruct_prompt)

display_response(response)
response_content = response.choices[0].message.content

# Find all the commands
matches = re.findall(extract_regex, response_content, re.DOTALL)

# Get the last match
file_content = matches[-1] if matches else ''

if file_content:
  print(f"Parsed File from GPT output:\n\n{file_content}\n\n")
  file_content = filter_command_output(file_content)
  print(f"Filtered File from GPT output:\n\n{file_content}\n\n")
else:
  print("Error: No file content found in response.")
  sys.exit(1)

revised_file_content = ""
# Check for "yarn add ..." lines in file_content and cd to the web app directory before running the command
for line in file_content.split("\n"):
    if line.startswith("yarn"):
        revised_file_content += f"cd {config["root_dir"]}\n"
    revised_file_content += line + "\n"
    if line.startswith("yarn"):
        revised_file_content += "cd ../code-gen\n"


# Ask user if they wish to execute the orchestration command
if not args.skip_confirm:
  execute_orchestration = input("Do you wish to execute the orchestration commands to fix the errors? (y/n): ")
else:
  execute_orchestration = 'y'

if execute_orchestration.lower() == 'y':
  # Write the commands to a new PowerShell script
  with open('./working/command.ps1', 'w') as file:
    file.write(revised_file_content)

  # Run the PowerShell script
  command_output = os.system('powershell.exe -File ./working/command.ps1 > ./working/error_fix_commandoutput.txt')
  print("Execution completed. Error fixing command output written to ./working/error_fix_commandoutput.txt.")


