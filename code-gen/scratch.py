import re

config = "../web-app"
file_content = "yarn add react react-dom react-scripts\npython .\script.py"

revised_file_content = ""
for line in file_content.split("\n"):
    if line.startswith("yarn"):
        revised_file_content += f"cd {config}\n"
    revised_file_content += line + "\n"
    if line.startswith("yarn"):
        revised_file_content += "cd ../code-gen\n"

print(revised_file_content)

