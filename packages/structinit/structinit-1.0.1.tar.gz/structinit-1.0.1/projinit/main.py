import os
import argparse
import requests
# import sys
import re
import json


def detect_root_name_and_lines(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as file:
        lines = [line for line in file.readlines() if line.strip()]

    for line in lines:
        if line.strip().endswith('/') or line.strip().endswith('\\'):
            root_name = line.strip().replace('/', '').replace('\\', '')
            root_indent = (len(line) - len(line.lstrip(' '))) // 2
            return root_name, root_indent, lines

    return "", 0, lines


def preprocess_structure_md(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f if line.strip()]

    # Check if the file contains a tree-like structure
    if not any(any(sym in line for sym in ['├──', '└──', '│']) for line in lines):
        print("⚠️ No tree-like structure detected in the file. Skipping preprocessing.")
        return

    processed_lines = []
    root_found = False  # To track if the root folder has been processed
    root_indent_level = 0  # To calculate relative indentation for nested items

    for line in lines:
        stripped = line.strip()

        # Handle the root folder
        if stripped.endswith('/') and not root_found:
            processed_lines.append(stripped)  # Add the root folder as is
            root_indent_level = line.count('│')  # Set the root indentation level
            root_found = True
            continue

        # Determine the level of indentation based on tree symbols
        if any(sym in stripped for sym in ['├──', '└──']):
            # Calculate the current level relative to the root
            relative_indent_level = line.count('│') - root_indent_level
            clean = stripped.lstrip('├└─│ ')
            processed_lines.append(f"{'  ' * (relative_indent_level + 1)}{clean}")
        else:
            # For plain lines like LICENSE, README, etc.
            processed_lines.append(f"{'  ' * (root_indent_level + 1)}{stripped}")

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(processed_lines) + '\n')

    print("✅ structure.md preprocessed into clean tree format!")


def create_license(base_dir, project_name):
    license_path = os.path.join(base_dir, "LICENSE")
    with open(license_path, 'w', encoding='utf-8') as f:
        f.write(f"""MIT License

Copyright (c) 2025 {project_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")
    print(f"✅ MIT License added at: {license_path}")


def create_structure_from_md(md_file_path, base_dir, add_license, project_name):
    with open(md_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    stack = []
    license_found = False  # Track if LICENSE is found in the .md file

    for line in lines:
        if not line.strip():
            continue

        indent_level = (len(line) - len(line.lstrip(' '))) // 2
        name = line.strip().replace('/', '')

        while len(stack) > indent_level:
            stack.pop()

        current_path = os.path.join(base_dir, *stack, name) if stack else os.path.join(base_dir, name)

        if line.strip().endswith('/'):
            os.makedirs(current_path, exist_ok=True)
            stack.append(name)

            # Auto-add __init__.py if it's a Python package
            if is_python_package(current_path):
                init_path = os.path.join(current_path, '__init__.py')
                with open(init_path, 'w', encoding='utf-8') as f:
                    f.write('# This file makes this directory a Python package.\n')
                print(f"📄 Created file: {init_path}")

        else:
            # Check if the file is LICENSE
            if name == "LICENSE":
                license_found = True
                create_license(os.path.dirname(current_path), project_name)
                continue

            dir_path = os.path.dirname(current_path)
            os.makedirs(dir_path, exist_ok=True)

            with open(current_path, 'w', encoding='utf-8') as f:
                f.write(get_boilerplate(name))

            print(f"📄 Created file: {current_path}")

    # If LICENSE was not found in the .md file but requested by the user, create it
    if add_license and not license_found:
        create_license(base_dir, project_name)


def get_boilerplate(filename):
    ext = os.path.splitext(filename)[1]

    if ext == '.py':
        return "#!/usr/bin/env python3\n\nif __name__ == \"__main__\":\n    print(\"Hello, world!\")\n"
    elif ext == '.js':
        return "console.log('Hello, world!');\n"
    elif ext == '.html':
        return "<!DOCTYPE html>\n<html>\n<head>\n  <title>My Page</title>\n</head>\n<body>\n</body>\n</html>\n"
    elif ext == '.md':
        return "# Project Title\n\n> Short description here.\n"
    elif ext == '.txt':
        return ""
    else:
        return ""


def is_python_package(directory):
    return any(name in directory.lower() for name in ['utils', 'src', 'package', 'module'])


def fetch_gitignore_template(language):
    url = f"https://raw.githubusercontent.com/github/gitignore/main/{language}.gitignore"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"⚠️ No .gitignore template found for '{language}'.")
        return None


def initialize_project(config):
    project_name = config['project_name']
    md_path = config['md_path']
    language = config['language']
    init_git = config['init_git']
    add_license = config['add_license']

    print(f"\n🚀 Initializing project: {project_name}")

    
    # Build structure
    base_dir = '.' if config['skip_name'] else project_name
    create_structure_from_md(md_path, base_dir, add_license, project_name)
    print(f"✅ Project structure created at: {base_dir}")

    # Add .gitignore if applicable
    if language:
        gitignore_content = fetch_gitignore_template(language)
        if gitignore_content:
            gitignore_path = os.path.join(project_name, ".gitignore")
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print(f"✅ Added .gitignore for {language}.")


    # Initialize Git repo
    if init_git:
        os.system(f'cd {project_name} && git init')
        print("✅ Git initialized.")


def load_test_input():
    """
    Load test input from a predefined JSON file or environment variable.
    This function is used when running in a test environment.
    """
    test_input_path = os.getenv("TEST_INPUT_PATH", "test_input.json")
    if os.path.exists(test_input_path):
        with open(test_input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"Test input file '{test_input_path}' not found.")



def main():
    parser = argparse.ArgumentParser(
        description="🛠️ Structinit: Generate full project structures from markdown blueprints.",
        epilog=(
            "📘 Example usage:\n"
            "  structinit --file structure.md    # Generate project from structure.md\n"
            "  structinit --test                 # Run in test mode with preconfigured values"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '--file', '-f',
        type=str,
        help="Path to the .md structure file that defines your project layout."
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help="Run in test mode using predefined test input (for debugging/demo)."
    )

    args = parser.parse_args()
    skip_name = False

    # ---- Test mode ----
    if args.test:
        print("🧪 Running in test mode...")
        test_config = load_test_input()
        project_name = test_config['project_name']
        md_path = test_config['md_path']
        language = test_config['language']
        init_git = test_config['init_git']
        add_license = test_config['add_license']
        skip_name = test_config['skip_name']

    # ---- Normal execution ----
    elif args.file:
        preprocess_structure_md(args.file)
        root_name, _, _ = detect_root_name_and_lines(args.file)

        if root_name:
            print(f"📦 Root project name detected in markdown: {root_name}")
            project_name = root_name
            skip_name = True
        else:
            project_name = input("🔤 Enter the project name: ").strip()

        language = input("📦 Primary language for .gitignore (leave empty to skip): ").strip()
        init_git = input("🌀 Initialize Git repository? (y/n): ").lower().strip() == 'y'
        add_license = input("📜 Add MIT License? (y/n): ").lower().strip() == 'y'

    # ---- No input provided ----
    else:
        parser.print_help()
        return

    # ---- Final config ----
    config = {
        'project_name': project_name,
        'md_path': args.file if not args.test else md_path,
        'language': language,
        'init_git': init_git,
        'add_license': add_license,
        'skip_name': skip_name
    }

    initialize_project(config)
    print("✅ Project structure created successfully.")
    
if __name__ == '__main__':
    main()
