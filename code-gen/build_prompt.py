import os
import json
from codegen import choose_relevant_files
from cg_utilities import strip_string_content

# Load the configuration file
with open('cgconfig.json') as config_file:
    config = json.load(config_file)

# Extract the variables from the configuration
root_dir = config['root_dir']
unwanted_dirs = config['unwanted_dirs']

# Function to walk through the directory structure
def walk_dir(dir_path, depth=0):
    directory_structure = f"{'    ' * depth}{os.path.basename(dir_path)}/\n"

    for item in sorted(os.listdir(dir_path)):
        item_path = os.path.join(dir_path, item)

        if os.path.isdir(item_path) and item not in unwanted_dirs:
            directory_structure += walk_dir(item_path, depth + 1)
        elif os.path.isfile(item_path):
            directory_structure += f"{'    ' * (depth + 1)}{item}\n"

            

    return directory_structure

def build_system_prompt(base_prompt_file, request, npm_build_output=None):
    global important_files
    with open(base_prompt_file, "r") as file:
        base_prompt = file.read()

    # Initialize the prompt with the base prompt
    prompt = f"{base_prompt}\n"

    # Look for a package.json file
    dependencies = {}
    if os.path.exists(os.path.join(root_dir, "package.json")):
        with open(os.path.join(root_dir, "package.json")) as file:
            package_json = json.load(file)
            dependencies = package_json.get("dependencies", {})

    # Add the dependencies and directory structure to the prompt
    prompt += f"Dependencies:\n{dependencies}\n\nDirectory Structure:\n"

    # Walk through the directory structure
    directory_structure = walk_dir(root_dir)
    prompt += directory_structure

    # Add the component samples to the prompt
    prompt += f"\nFile samples:\n"
    important_files = choose_relevant_files(request)
    # Add file contents to the prompt

    for file in important_files:
        if os.path.exists(file['name']):
            prompt += f"\nFile: {file['name']}\nDescription: {file['description']}\nContents:\n"
            with open(file['name'], "r") as file_content:
                lines = file_content.readlines()
                for line in lines:
                    prompt += line
                prompt += "[EOF]\n\n"
    

    print(f"System Prompt: {strip_string_content(prompt)}")

    return prompt

def build_compare_prompt(base64_screen, base64_comp, filename, current_code_contents=None, user_request=None):
        prompt = [
                {"type": "text", "text": f"We need help!\nOur design for {filename} is based on this UI Composite image:"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_comp}",
                    },
                },
                {"type": "text", "text": f"We have the following screenshot showing how {filename} appears:"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_screen}",
                    },
                },
        {"type": "text", "text": f"You are going to be a masterful coder, and provide updated code for {filename}."},
        ]

        if user_request is not None:
                prompt.append({"type": "text", "text": f"Accordingly, please review the following suggestions from a UX and React expert colleague, and implement these changes as described:\n {user_request}"})

        if current_code_contents is not None:
                prompt.append({"type": "text", "text": f"Current contents of {filename} is: \n\n{current_code_contents}\n[EOF]\n\n"})

        return prompt


def build_instruct_prompt(base64_screen, base64_comp, filename, current_code_contents=None, user_request=None):
        prompt = [
                {"type": "text", "text": f"We need help!\nOur design for {filename} is based on this UI Composite image:"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_comp}",
                    },
                },
                {"type": "text", "text": f"The current output of {filename} from the current React code is:"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_screen}",
                    },
                },
        {"type": "text", "text": f"Critique and list the differences between these outputs and provide detailed instructions for an expert React coder to update the current version of {filename}. Your output will be passed directly to the coder as instructions, so please address the coder directly as 'you' and say please and thank you. The coder is an LLM and does not need to be instructed to open files or use an IDE. Simply instruct about the intended structure of the file itself."},
        ]

        if user_request is not None:
                prompt.append({"type": "text", "text": f"Specifically, {user_request}"})

        if current_code_contents is not None:
                prompt.append({"type": "text", "text": f"Current contents of {filename} is: \n\n{current_code_contents}\n[EOF]\n\n"})

        return prompt

def build_code_prompt(base64_comp, filename, user_request=None):
        prompt = []

        if base64_comp is not None:
            prompt.append({"type": "text", "text": f"We need help!\nOur design for {filename} is based on this UI Composite image:"})
            prompt.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_comp}"}})

        prompt.append({"type": "text", "text": f"You are going to be a masterful coder, and provide new code for {filename}."})

        if user_request is not None:
                prompt.append({"type": "text", "text": f"Accordingly, please review the following suggestions from a UX and React expert colleague, and implement them as described:\n {user_request}"})

        return prompt


def build_new_instruct_prompt(base64_comp, filename, user_request=None):
        prompt = []

        if base64_comp is not None:
            prompt.append({"type": "text", "text": f"We need help!\nOur design for {filename} is based on this UI Composite image:"})
            prompt.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_comp}"}})

        prompt.append({"type": "text", "text": f"Provide detailed instructions for an expert React coder to implement {filename}. You will be attentive to ensuring coder is aware of all the necessary pieces, but you will not write the component directly for coder. Instead you will logically work through how props and state should work, what callback methods are required, thinking through how the page or component fits within it's broader context. Your output will be passed directly to the coder as instructions, so please address the coder directly as 'you' and say please and thank you. The coder is an LLM and does not need to be instructed to open files or use an IDE. Simply instruct about the intended structure of the file itself."})

        if user_request is not None:
                prompt.append({"type": "text", "text": f"Specifically, {user_request}"})

        return prompt

def build_error_instruct_prompt(filename, current_code_contents=None, user_request=None):
        prompt = [
                {"type": "text", "text": f"We need help!\nSomething is wrong with {filename}, we are seeing a failure in the npm build output."},
                {"type": "text", "text": f"Provide detailed instructions for an expert React coder to implement fixes required for {filename}. You will be attentive to ensuring coder is aware of all the necessary pieces, but you will not write the component directly for coder. Instead you will logically work through each error and how to approach a fix for each, thinking through how the page or component fits within it's broader context. Your output will be passed directly to the coder as instructions, so please address the coder directly as 'you' and say please and thank you. The coder is an LLM and does not need to be instructed to open files or use an IDE. Simply instruct about how to alter the file itself.  If the issue is that the app can't resolve a css file, remove the reference to that file."},
        ]

        if user_request is not None:
                prompt.append({"type": "text", "text": f"Specifically, {user_request}"})

        if current_code_contents is not None:
                prompt.append({"type": "text", "text": f"Current contents of {filename} is: \n\n{current_code_contents}\n[EOF]\n\n"})

        return prompt


def build_error_code_prompt(filename, compilation_errors, current_code_contents=None, user_request=None):
        prompt = [
                {"type": "text", "text": f"We need help!\nSomething is wrong with {filename}, we are seeing the following errors on compile:\n\n{compilation_errors}"},
                {"type": "text", "text": f"You are going to be a masterful coder, and provide new code for {filename} that fixes the errors. If the issue is that the app can't resolve a css file, remove the reference to that file."},
        ]

        if user_request is not None:
                prompt.append({"type": "text", "text": f"Accordingly, please review the following suggestions from a React expert colleague, and implement them as described:\n {user_request}"})
        
        if current_code_contents is not None:
                prompt.append({"type": "text", "text": f"Current contents of {filename} is: \n\n{current_code_contents}\n[EOF]\n\n"})

        return prompt


def build_update_instruct_prompt(filename, current_code_contents=None, user_request=None, base64_screen=None):
        prompt = [
                {"type": "text", "text": f"We need help!\nWe are working to improve {filename}, we need to update it."},
                {"type": "text", "text": f"Provide detailed instructions for an expert React coder to implement updates required for {filename}. You will be attentive to ensuring coder is aware of all the necessary pieces, but you will not write the component directly for coder. Instead you will logically work through each error and how to approach a fix for each, thinking through how the page or component fits within it's broader context. Your output will be passed directly to the coder as instructions, so please address the coder directly as 'you' and say please and thank you. The coder is an LLM and does not need to be instructed to open files or use an IDE. Simply instruct about the intended structure of the file itself."},
        ]

        if user_request is not None:
                prompt.append({"type": "text", "text": f"Specifically, {user_request}"})

        
        if base64_screen is not None:
            prompt.append({"type": "text", "text": f"\nThe UI currently looks as follows when rendered, coder will not be able to see this image, so be specific in your instructions:\n"})
            prompt.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_screen}"}})

        if current_code_contents is not None:
                prompt.append({"type": "text", "text": f"\nCurrent contents of {filename} is: \n\n{current_code_contents}\n[EOF]\n\n"})

        return prompt


def build_update_code_prompt(filename, current_code_contents=None, user_request=None):
        prompt = [
                {"type": "text", "text": f"We need help!\nWe are working to improve {filename}, we need to update it."},
                {"type": "text", "text": f"You are going to be a masterful coder, and provide updated code for {filename}."},
        ]

        if user_request is not None:
                prompt.append({"type": "text", "text": f"Accordingly, please review the following suggestions from a React expert colleague, and implement them as described:\n {user_request}"})
        
        if current_code_contents is not None:
                prompt.append({"type": "text", "text": f"Current contents of {filename} is: \n\n{current_code_contents}\n[EOF]\n\n"})

        return prompt

def build_orchestrator_prompt(base64_screen, screenshot_url, base64_comp, comp_path, user_request=None, npm_build_output=None):
        prompt = []

        if base64_screen is not None:
            prompt.append({"type": "text", "text": f"Examine the current output of the React code for screenshot_url: {screenshot_url} :"})
            prompt.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_screen}",
                },
            })
            prompt.append({"type": "text", "text": f"That is the current state of our app in development."})
            

        if base64_comp is not None:
            prompt.append({"type": "text", "text": f"The design comp we are trying to match is at comp_path: {comp_path} and is shown here:"})
            prompt.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_comp}"}})
            prompt.append({"type": "text", "text": f"Compare to current output (if available) to perform the task requested below."})

        if user_request is not None:
                prompt.append({"type": "text", "text": f"We need help!\nWe are working to improve this code base, it surely needs work, and you are the right person for the job. Specifically, {user_request}"})

        
        prompt.append({"type": "text", "text": f"You know about the context here, all the filenames and the relevant file contents of our stack. Start by analyzing relevant parts of the code base or code files and provide a high level overview of any issues or steps relevant to the request that you see. Then you will logically work through each issue or step and how to approach a fix or implementation for each based on the instruction set provided. \n\nCurrent NPM Build output:\n\n{npm_build_output}\n\n[END NPM OUTPUT]\n"})
        
        prompt.append({"type": "text", "text": f"Finally, output the specific actions as bash script invoking only the allowed commands. Provide detailed instructions within user_request arguments."});

        return prompt
