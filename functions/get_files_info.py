import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory, directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        print(f'Error: Cannot list "{directory}" as is outside the permitted working directory')
        return None
    
    if not os.path.isdir(directory):
        print(f'Error: "{directory}" is not a directory')
        return None
    
    list_of_files = ""
    files = os.listdir(target_dir)
    for n in [0, len(files) - 1]:
        list_of_files += f'{files[n]} : file size= {os.path.getsize(os.path.join(target_dir, files[n]))} bytes, is_dir= {os.path.isdir(os.path.join(target_dir, files[n]))} \n'
    try:
        return list_of_files
    except Exception as e:
        print(f'Error: {e}')
        return None
    
    print(list_of_files)