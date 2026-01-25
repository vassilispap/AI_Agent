import os
import subprocess


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
        newsub = subprocess.run(
            command, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        result = newsub.stdout
        if newsub.returncode != 0:
            result += "Process exited with code X"
        if newsub.stdout == "" or newsub.stderr != "":
            result += "No output produced"
        if newsub.returncode == 0  and newsub.stdout != "" and newsub.stderr == "":
            result += f'STDOUT: {newsub.stdout} STDERR: {newsub.stderr}'
        return result
    
    except Exception as e:
        return f"Error: executing Python file: {e}"