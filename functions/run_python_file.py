import os
import subprocess
from config import MAX_CHARS
from google import genai
from google.genai import types



def run_python_file(working_directory, file_path, args=None):

    try:

        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'  
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args:
            command.extend(args)
        # print(f"DEBUG abs_working_dir={working_dir_abs}, abs_file_path={working_dir_abs}")
        newsub = subprocess.run(
            command, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        result = newsub.stdout
        if newsub.returncode != 0:
            result = f"Process exited with code {newsub.returncode}"
        if not newsub.stdout and not newsub.stderr:
            result = "No output produced"
        if newsub.stdout:
            result = (f"STDOUT:\n{newsub.stdout}")
        if newsub.stderr:
            result = (f"STDERR:\n{newsub.stderr}")

        return "".join(result)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specified Python file with optional arguments",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path for the python file to run, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

