import re
import os
import sys
import base64
from cg_utilities import call_gpt, display_response
from openai import AzureOpenAI
import argparse
import json

def validate_complete(file_contents):
    
    print("\nChecking file completion:\n\n")

    user_content = [
                    {"type": "text", "text": f"It is essential for humanity to know whether a file is a complete code file or not. A file with content that indicates 'rest of file remains unchanged' or 'existing components here', etc... will NOT be considered a complete file. A file whose content looks like it is meant to be merged with existing code is not a complete file. Is this file content representative of a complete file? Answer yes or no only. Do not answer anything but a single word, yes or no. Is this file complete? :\n{file_contents}"}
                ]
    response = call_gpt("Assistant is an AI specialized expert coder and interpreter of React UI in TypeScript.",
                        user_content,
                        max_tokens=1, temperature=0.1, top_p=.1)
    
    display_response(response)

    return response.choices[0].message.content

def merge_contents(file_contents, existing_file_path, previous_instructions):
    
    if(not os.path.exists(existing_file_path)):
        print("Error: The existing file path does not exist.")
        sys.exit(1)
    
    with open(existing_file_path, 'r') as file:
        existing_file_contents = file.read()

    print("\nMerging file contents:\n\n")

    
    user_content = [
                    {"type": "text", "text": f"A coding assistant was prompted with the following intructions to alter a file: {previous_instructions} [END PREVIOUS INSTRUCTIONS]. Following these instructions, coding assistant suggested the following file update:\n{file_contents}\n[END FILE]\n\nPlease accurately merge it with the existing file contents:{existing_file_contents}\n[END FILE]\n\nPlease merge the two files and return the resulting file contents only. Take care to consider file structure and syntax to ensure the merged file is coherent. Maintain the original intent of the previous instructions when merging. Do not respond with anything except for the merged file content."}
                ]

    response = call_gpt("Assistant is an AI specialized expert coder and interpreter of React UI in TypeScript. Assistant is meticulous and will not make mistakes. Assistant is most skilled at merging code into existing files. Assistant always responds with only the merged file content, and merged file content only. Assistant follows the instructions in code comments indicating how to merge the new content.",
                        user_content,
                        max_tokens=4092, temperature=0.2, top_p=.5)
    
    print("\n\nMerged Content:\n")
    
    display_response(response)


    return response.choices[0].message.content


def choose_relevant_files(user_request, npm_build_output=None):
    
    # Load the configuration file
    with open('cgconfig.json') as config_file:
        config = json.load(config_file)

    # Extract the variables from the configuration
    root_dir = config['root_dir']
    unwanted_dirs = config['unwanted_dirs']
    important_files = config['important_files']
    available_file_paths = ""

    for root, dirs, files in os.walk(root_dir):
        # Exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in unwanted_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            available_file_paths += file_path + "\n"

    # Remove the trailing newline character
    available_file_paths = available_file_paths.rstrip("\n")

    user_content = [
                    {"type": "text", "text": f"This request was received by a coding assistant:\n{user_request}\n[end request]\n\nPlease provide a list of filepaths that are relevant to the request. The files selected will be included in context of an llm call to assist the model in solving the user_request. Do not respond with anything except for the list of filepaths."}
                ]
    
    if npm_build_output:
        user_content.append({"type": "text", "text": f"\n\nThe npm build output is:\n{npm_build_output}"})

    response = call_gpt(f"Assistant is an AI specialized expert coder and interpreter of React UI in TypeScript. Assistant is meticulous and will not make mistakes. Assistant is most skilled at determining which files are relevant for a given task. Assistant will include any files with errors, unless the files are so numerous that the error lies in a more central location. Assistant will make a best guess as to what files are appropriate to include. Assistant always responds with only a list of file paths, and list of filepaths only. The only file paths available are:\n{available_file_paths}\n\nAssistant will ONLY include paths that are available. Any Paths not listed above are invalid and must not be included.",
                        user_content,
                        4092,
                        0.3,
                        .5)
                    
        

    print("\n\nGPT4 guesses relevant files:\n")
    display_response(response)

    response_file_paths = response.choices[0].message.content.split("\n")

    for file_path in response_file_paths:
        if file_path and not any(f['name'] == file_path for f in important_files):
            important_files.append({"name": file_path, "description": "Relevant File"})

    return important_files

