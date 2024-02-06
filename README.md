# GPTReactor Project

GPTReactor is a demonstration project that uses GPT4 Turbo (with or without Vision) to generate a React UI from natural language instructions and images. The project aims to explore the potential of AI in automating and simplifying the process of building user interfaces. The project supports the OpenAI API via Azure OpenAI, or direct to OpenAI. Using Azure OpenAI generally allows for higher quota/throughput. You may also use any local llms that support the OpenAI api format.

There are two top folders in the repository: /code-gen and /web-app. /web-app contains a React project, a simple web app built using Vite using React + Typescript using SWC (superfast web compiler). /code-gen contains python scripts that can be used to alter that React web app code with GPT. 

## Getting Started

1. First, ensure that you have the latest versions of Node.js and Python installed on your system. You can download them from their official websites:

    - [Node.js](https://nodejs.org/)
    - [Python](https://www.python.org/)

2. Install Yarn, a package manager for your code. You can install Yarn globally on your system using the following command in your terminal:

    ```bash
    npm install --global yarn
    ```

3. Clone the GPTReactor project from GitHub:

    ```bash
    git clone https://github.com/pgazmuri/GPTReactor
    ```

4. Navigate to the `/web-app` directory in the GPTReactor project:

    ```bash
    cd GPTReactor/web-app
    ```

5. Install the web project dependencies:

    ```bash
    yarn install
    ```

6. Start the web project:

    ```bash
    npm run dev
    ```

GPTReactor's basic empty web application should now be running. You can view the application by opening your web browser and navigating to the URL provided in your terminal. Next, we will setup the python code-gen project.

Open a second terminal and navigate to the GPTReactor/code-gen directory. Run the following command to install the Python dependencies:

```bash
pip install -r requirements.txt
```

You are now ready to run GPTReactor. Try the following script:

```bash
python .\cg_orchestrate_update.py --user_request "Add a calculator page to the application."
```

You should see something like the following:

```bash
Filtered File from GPT output:

python ./cg_update_fix.py --user_request "Add a navigation link to the Calculator page in the sidebarItems array, using CalculatorIcon for the icon and 'Calculator' as the text." --code_path ../web-app/src/components/Sidebar.tsx
python ./cg_new_file.py --user_request "Create Calculator page component with a basic structure, including placeholders for display and buttons." --code_path ../web-app/src/pages/Calculator.tsx
python ./cg_update_fix.py --user_request "Import Calculator component and add a route for '/calculator' that renders the Calculator component." --code_path ../web-app/src/App.tsx
python ./cg_update_fix.py --user_request "Implement the calculator's UI including a display area and buttons for digits 0-9, addition, subtraction, multiplication, division, and an equals button in a grid layout." --code_path ../web-app/src/pages/Calculator.tsx


Do you wish to execute the orchestration command? (y/n):
```

Entering 'y' will invoke the commands suggested by the orchestrator.

The first time you run any command that invokes GPT, you will be asked for your connection information. It will be stored in /code-gen/config.json.

## How GPTReactor Works

GPTReactor uses a collection of Python scripts in /code-gen to perform various actions that contribute to the generation of the React UI in /web-app. File-level actions include:

- **File Creation**: cg_new_file.py action generates a file from a UI Comp image, a description, or both.
- **Fix Error**: cg_error_fix.py action rectifies errors in a file.
- **Component/File Update**: cg_update_fix.py action updates a component or file as per the user's request.
- **Comparison/Update**: cg_comparison_fix.py action compares code output to a UI comp and updates the component file to match the comp more accurately.

Each File-level action utilizes both shared (system) and unique (user) prompts. Relevant stack information is included and injected into prompts to provide the model with grounding and context, enabling it to perform the task correctly using the current stack's conventions. The prompts are in text files called "prompt_coder", "prompt_orchestrator", and "prompt_taskmaker", where they can be further customized to reflect the software stack. A file called cgconfig.json contains details about the web-app project that is useful in helping us inject the right filepaths and file contents into the prompts.

## GPTReactor Calls

Each action internally triggers multiple GenAI calls:

1. The first call identifies what file(s) contents should be included in the “instruct” call prompt.
2. The next call is the “instruction” call, which provides a detailed set of steps to alter a given file.
3. The next call identifies what file(s) contents should be included in the “code” call prompt.
4. The next call is the “code” call, which follows the detailed set of steps output from the instruct call.
5. A fourth call validates whether the output from call 2 is a complete file, or needs to be merged with the file on disk.
6. If step 5 determines that we need to merge, we pass the existing and updated file contents to a final call to merge the file contents.

## Orchestrator Script

The `cg_orchestrate_update.py` script in GPTReactor coordinates changes across multiple files. It first builds a prompt for the GPT model using various inputs such as a screenshot (optional), a comp (UI mockup) path (optional), a user request, and typescript build output. The prompt is then sent to the GPT model, which returns a set of instructions. These instructions are parsed and filtered to extract the commands provided by the GPT model. These commands, once confirmed by the user, are then executed to perform the necessary updates to the files (pass --skip_confirm if you wish). If you do not provide a screenshot_url or comp_path, the vision model will not be used.

If there are any errors in the npm build output after the command execution, the script builds a new orchestrator prompt that includes the original instructions and a request to fix the errors. This prompt is sent to the GPT model, which returns a set of instructions to fix the errors.

### Example of executing the orchestrator:

An example user_registration.png UI comp is provided so you can try this:

```bash
python cg_orchestrate_update.py --user_request "Build a user registration page based on the provided comp. When the form is submitted, update the name and email in the userstore. Use the route /register and add a sidebar menu item." --comp_path ./examples/user_registration.png
```

If you want to update the page after it's created (replace the screenshot url with your currently running dev url):

```bash
python cg_orchestrate_update.py --user_request "Update the user registration page to ensure the form is left aligned and to better match the comp" --comp_path ./examples/user_registration.png --screenshot_url http://localhost:5173/register
```

Try this example, where we use a report mockup image to generate code for a report:

```bash
python cg_orchestrate_update.py --user_request "Build a report page to match the comp. Mock the data in a reportStore. Add a link to the sidebar." --comp_path ./examples/report.png
```

The output from one run of this command was the following, you can see the logical structure of the commands and how the comp path is passed on to create the reports page:

```bash
python ./cg_new_file.py --user_request "Create a report store file named reportStore.ts in the store directory. Add mock data that includes various metrics to be displayed on the report page, such as bar chart data, pie chart data, and statistics." --code_path ../web-app/src/store/reportStore.ts
python ./cg_new_file.py --user_request "Create a Reports page component named Reports.tsx in the pages directory. This component should include placeholders for the different charts and metrics that will match the comp as closely as possible, utilizing inline styles and MUI components where helpful." --code_path ../web-app/src/pages/Reports/Reports.tsx --comp_path ./examples/reports.jpg
python ./cg_update_fix.py --user_request "Add a new Route within the Router component in App.tsx for the Reports page. The path should be '/reports' and the element should be the newly created Reports component." --code_path ../web-app/src/App.tsx
python ./cg_update_fix.py --user_request "Add a new sidebar item for the Reports page with a corresponding icon and text, 'Reports'. The path should be '/reports'." --code_path ../web-app/src/components/Sidebar.tsx  
```

If the output still needs improvement (and it often does):

```bash
python cg_orchestrate_update.py --user_request "Update the report page to better match the comp. use or improve the mock data in reportstore. import additional libraries as needed to ensure you can display the charts and graphs and indicators needed." --comp_path ./examples/reports.jpg --screenshot_url http://localhost:5173/reports
```

Again, be sure to replace the screenshot url with your currently running dev url.

To fix compilation errors:

```bash
python cg_orchestrate_update.py --user_request "Just fix the errors and make it work."
```

Though it would help, this call doesn’t need to include details about compile time errors, as typescript build output is included in the context of all orchestration requests.

## FAQs

Why didn't you use LangChan/Semantic Kernel/Prompt Flow, etc...?

I intentionally wanted the python code to be as simple as possible for transparency/ease of understanding by React devs and others not familiar with these frameworks. I myself am not particularly familiar with python and it's conventions, but chose python as it's the default stack for AI, benefiting from the most comprehensive ecosystem while keeping the solution 'agnostic' in terms of potential stacks and languages that it can operate against. Consequently, the current set of scripts could be easily ported to Typescript as is to better fit within the React ecosystem.

## Future Work
This demonstration project is just that, a demonstration. GPT compute is sufficiently expensive that performing proper evaluation at scale to validate improvements is cost prohibitive. At the same time, there is plenty of low-hanging fruit in terms of potential improvements and optimizations. If there is any interest in further refining this tool, I would recommend:

* Improve logging and error handling
* Clean up console output to be more useful
* Improve prompts with additional examples
* Set up an evaluation pipeline to properly evaluate prompt effectiveness (this is costly)
* Generally test various use cases and review completions to understand failure modes and potential mitigations
* Generally improve the base React app stack to include a more complete set of non-functional and cross-functional conventions/libraries
* Extend to support full stack integration of some kind
