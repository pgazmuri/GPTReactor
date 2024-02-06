from openai import AzureOpenAI
import os
import sys
import base64
from build_prompt import build_system_prompt, build_compare_prompt, build_instruct_prompt
from cg_utilities import call_gpt, display_response, encode_image, strip_content, take_and_encode_screenshot, take_screenshot
import argparse
import re
import os
from codegen import validate_complete, merge_contents

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--user_request", default="Your default user request")
parser.add_argument("--screenshot_url", required=True, help="URL for taking the screenshot")
parser.add_argument("--comp_path", required=True, help="Path to the composite image")
parser.add_argument("--code_path", required=True, help="Path to the code file")
parser.add_argument("--skip_instruct", required=False, help="Skip the instruct step and run code generation based on user_response alone")

args = parser.parse_args()

# Check if the code file exists
if not os.path.isfile(args.code_path):
  print("Error: The specified code file does not exist.")
  sys.exit(1)

# Check if the environment variables are set
if not os.getenv("AZURE_OPENAI_KEY") or not os.getenv("AZURE_OPENAI_ENDPOINT"):
  print("Error: The AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT environment variables must be set.")
  sys.exit(1)
  
# Usage:

base64_screen = take_and_encode_screenshot(args.screenshot_url)

if base64_screen == None:
  print("Error: screenshot failed")
  sys.exit(1)

# Getting the base64 string for the comp
base64_comp = encode_image(args.comp_path)

# Get the code contents
with open(args.code_path, "r") as file:
  code_contents = file.read()


if not args.skip_instruct:
  taskmaker_system_prompt = build_system_prompt("prompt_taskmaker.txt", args.user_request)
  taskmaker_code_contents = code_contents if code_contents not in taskmaker_system_prompt else None # If the code is already in the prompt, don't send it again, also
  instruct_prompt = build_instruct_prompt(base64_screen, base64_comp, args.code_path, taskmaker_code_contents, args.user_request)
  print(f"\nInstruct prompt: {strip_content(instruct_prompt)}")
  print("Calling GPT4 Vision for instructions...")
  response = call_gpt(taskmaker_system_prompt, instruct_prompt)
  display_response(response)
  instructions = response.choices[0].message.content
else:
  instructions = args.user_request



system_prompt = build_system_prompt("prompt_coder.txt", instructions) 
code_contents = code_contents if code_contents not in system_prompt else None
user_prompt = build_compare_prompt(base64_screen, base64_comp, args.code_path, code_contents, instructions)


print("Calling GPT4 Vision for code...")
print(f"\nCode prompt: {strip_content(user_prompt)}")

response = call_gpt(system_prompt, user_prompt, max_tokens=4092, temperature=0.2, top_p=.5)

display_response(response)

response_content = response.choices[0].message.content

# Find the writefile command
writefile_command = re.search(r'WRITEFILE \'(.*?)\'', response_content)

if writefile_command:
  # Get the file path from the writefile command
  file_path = writefile_command.group(1)


  # Find the content between the ticks
  file_content = re.search(r'```[a-z]+\n(.*?)\n```', response_content, re.DOTALL).group(1)

  if file_content:

    print(f"Parsed File from GPT output:\n\n{file_content}\n\n")

    if(validate_complete(file_content).lower() == "no"):
      print("GPT4 Response Suboptimal: The file is not complete. merging with existing file\n\n")
      file_content = merge_contents(file_content, file_path, instructions)
      file_content = re.search(r'```[a-z]+\n(.*?)\n```', file_content, re.DOTALL).group(1)
      print(f"Merged File:\n\n{file_content}\n\n")

    #continue_prompt = input(f"Replace file {file_path}? (y/n): ")
    #if continue_prompt.lower() != 'y':
    #  exit()

    # Write the file
    with open(file_path, 'w', encoding='utf-8') as file:
      file.write(file_content)