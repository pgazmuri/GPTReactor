from openai import AzureOpenAI
import os
import sys
import base64
from build_prompt import build_system_prompt, build_error_code_prompt, build_error_instruct_prompt
from cg_utilities import call_gpt, display_response, get_npm_errors, strip_content
import argparse
import re
import os
from codegen import validate_complete, merge_contents

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--user_request", default="Your default user request")
parser.add_argument("--code_path", required=True, help="Path to the broken code file")
parser.add_argument("--skip_instruct", required=False, help="Skip the instruct step and run code generation based on user_response alone")
args = parser.parse_args()

# Check if the code file exists
if not os.path.isfile(args.code_path):
  print("Error: The specified code file does not exist.")
  sys.exit(1)

code_errors = get_npm_errors("../packages/web-app")
taskmaker_system_prompt = build_system_prompt("prompt_taskmaker.txt", args.user_request, code_errors)

# Get the code contents
with open(args.code_path, "r") as file:
  code_contents = file.read()

taskmaker_code_contents = code_contents if code_contents not in taskmaker_system_prompt else None

if not args.skip_instruct:
  instruct_prompt = build_error_instruct_prompt(args.code_path, taskmaker_code_contents, args.user_request)
  print(f"\nInstruct prompt: {strip_content(instruct_prompt)}")
  print("Calling GPT4 Vision for instructions...")
  response = call_gpt(taskmaker_system_prompt, instruct_prompt)
  display_response(response)
  instructions = response.choices[0].message.content
else:
  instructions = args.user_request

system_prompt = build_system_prompt("prompt_base.txt", instructions, code_errors) 
code_contents = code_contents if code_contents not in system_prompt else None
user_prompt = build_error_code_prompt(args.code_path, code_contents, instructions)


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