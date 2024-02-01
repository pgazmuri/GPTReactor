from openai import AzureOpenAI
import os
import sys
import base64
from build_prompt import build_system_prompt, build_new_instruct_prompt, build_code_prompt
from cg_utilities import call_gpt, display_response, encode_image, strip_content, take_screenshot
import argparse
import re
import os

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--user_request", default="Your default user request")
parser.add_argument("--comp_path", required=False, help="Path to the composite image")
parser.add_argument("--code_path", required=True, help="Path to the code file")
parser.add_argument("--skip_instruct", required=False, help="Skip the instruct step and run code generation based on user_response alone")
args = parser.parse_args()

# Check if the code file exists
if  os.path.isfile(args.code_path):
  print("Error: The specified code file already exists.")
  sys.exit(1)

# Getting the base64 string for the comp
base64_comp = encode_image(args.comp_path) if args.comp_path else None

taskmaker_system_prompt = build_system_prompt("prompt_taskmaker.txt", args.user_request)

if not args.skip_instruct:
  instruct_prompt = build_new_instruct_prompt(base64_comp, args.code_path, args.user_request)
  print(f"\nInstruct prompt: {strip_content(instruct_prompt)}")
  print("Calling GPT4 Vision for instructions...")
  response = call_gpt(taskmaker_system_prompt, instruct_prompt)
  display_response(response)
  instructions = response.choices[0].message.content
else:
  instructions = args.user_request
system_prompt = build_system_prompt("prompt_base.txt", instructions) 
user_prompt = build_code_prompt(base64_comp, args.code_path, instructions)

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

    # Ensure the directory for args.code_path exists
    code_dir = os.path.dirname(args.code_path)
    if not os.path.exists(code_dir):
        os.makedirs(code_dir)

    # Write the file
    with open(file_path, 'w', encoding='utf-8') as file:
      file.write(file_content)