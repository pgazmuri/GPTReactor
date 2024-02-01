import os
import argparse

# Create the argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--lazy_load", action="store_true", help="Enable lazy loading", default=False)
parser.add_argument("--component_count", type=int, help="Number of components to generate", default=2500)

# Parse the command-line arguments
args = parser.parse_args()

# Check if lazy loading is enabled
if args.lazy_load:
    # Lazy loading logic here
    print("Lazy loading of components is enabled")
else:
    # Non-lazy loading logic here
    print("Lazy loading will not be included in the generated components")


# Define the template file path
template_file = "./../packages/web-app/src/components/Template/Template.tsx"

# Define the output directory
output_directory = "./../packages/web-app/src/components/Generated"

# Make sure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Delete every file in the output directory
for filename in os.listdir(output_directory):
    file_path = os.path.join(output_directory, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)


# Define the number of components to generate
num_components = args.component_count

# Read the template file
with open(template_file, "r") as file:
    template_content = file.read()

# Generate the components
for i in range(num_components):
    # Generate the component name
    component_name = f"Component{i}"

    # Generate the component file path
    component_file = os.path.join(output_directory, f"{component_name}.tsx")

    # Replace the template name in the template content
    component_content = template_content.replace("Template", component_name)

    # Write the component content to the component file
    with open(component_file, "w") as file:
        file.write(component_content)


# Generate the ComponentLoader file
component_loader_file = os.path.join(output_directory, "ComponentLoader.tsx")

# Delete the ComponentLoader file if it already exists
if os.path.exists(component_loader_file):
    os.remove(component_loader_file)

# Start the ComponentLoader content with the import statements and the start of the ComponentLoader component
component_loader_content = "import React, { Suspense } from 'react';\nimport { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';\n\n"

# Import each component
for i in range(num_components):
    component_name = f"Component{i}"
    if args.lazy_load:
        component_loader_content += f"const {component_name} = React.lazy(() => import('./{component_name}'));\n"
    else:
        component_loader_content += f"import {component_name} from './{component_name}';\n"

component_loader_content += "\nconst ComponentLoader = () => {\n"
component_loader_content += "  return (\n"
component_loader_content += "      <Suspense fallback={<div>Loading...</div>}>\n"
component_loader_content += "      <div>\n"

# Add a Link for each component
for i in range(num_components):
    component_name = f"Component{i}"
    component_loader_content += f'        <Link to="{component_name}">{component_name}</Link>\n'

component_loader_content += "      </div>\n"
component_loader_content += "      <Routes>\n"

# Add a Route for each component
for i in range(num_components):
    component_name = f"Component{i}"
    component_loader_content += f'        <Route path="/{component_name}" element={{<{component_name}/>}} />\n'

# Close the Switch, Router, ComponentLoader component and export it
component_loader_content += "      </Routes>\n"
component_loader_content += "      </Suspense>\n"
component_loader_content += "  );\n"
component_loader_content += "};\n\n"
component_loader_content += "export default ComponentLoader;\n"

# Write the ComponentLoader content to the ComponentLoader file
with open(component_loader_file, "w") as file:
    file.write(component_loader_content)