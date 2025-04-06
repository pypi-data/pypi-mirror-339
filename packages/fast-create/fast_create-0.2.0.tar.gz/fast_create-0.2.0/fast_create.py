#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess

def create_project_structure(project_name):
    # Get the absolute path of the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(script_dir, "temp")

    # Check if temp directory exists
    if not os.path.exists(temp_dir):
        print(f"Error: 'temp' directory not found at {temp_dir}")
        sys.exit(1)

    # Create the project directory
    os.makedirs(project_name, exist_ok=True)

    # Copy contents from temp to the new project
    for item in os.listdir(temp_dir):
        source = os.path.join(temp_dir, item)
        destination = os.path.join(project_name, item)

        if os.path.isdir(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(source, destination)

    print(f"FastAPI project '{project_name}' created successfully!")

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "new":
        print("Usage: fast-create new <project_name>")
        sys.exit(1)

    project_name = sys.argv[2]
    create_project_structure(project_name)

    # Start FastAPI server if main.py exists
    main_file = os.path.join(project_name, "main.py")
    if os.path.exists(main_file):
        print("Starting FastAPI server...")
        subprocess.run(["uvicorn", "main:app", "--reload"], cwd=project_name)
    else:
        print("Warning: main.py not found. Server not started.")

if __name__ == "__main__":
    main()
