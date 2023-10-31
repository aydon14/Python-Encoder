"""-<Libraries>-"""

import argparse, os, ctypes, time, sys
from datetime import datetime

"""-<Functions>-"""

def parse_arguments():
    """-<Parse Arguments>-"""
    parser = argparse.ArgumentParser(description="Arguments and Definitions.") # --help
    parser.add_argument("--list-methods", action='store_true', help="Lists codex methods.")
    parser.add_argument("--codex-method", type=str, help="Chooses the DLL file & codex function. [codex.[encode or decode]]")
    parser.add_argument("--input-file", type=str, help="File(s) to be read. [c:/path/to/[file or folder]]")
    parser.add_argument("--output-file", type=str, help="File(s) to be made/replaced. [c:/path/to/[file or folder]]")
    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.error("Please provide arguments. Use --help for assistance.")
    elif args.list_methods:
        print()
        dir_list = directory_list(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codex"))
        [print(os.path.basename(file).split('.')[0]) for file in dir_list]
        print()
        sys.exit()
    elif args.codex_method is None or args.input_file is None or args.output_file is None:
        parser.error("You must provide all three arguments: --codex-method, --input-file, and --output-file")
    return args

def directory_list(directory):
    """-<List files in a given directory>-"""
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def remove_quotes(path):
    if path and path[0] == '"' and path[-1] == '"':
        return path[1:-1]
    return path

def main():
    """-<Main Method>-"""
    # Local variables and parsing
    args = parse_arguments()
    
    input_dir = args.input_file.strip('"')
    output_dir = args.output_file.strip('"')
    og_files = directory_list(input_dir)
    
    # Additional ERR checking
    
    print() # This isn't random. It adds a seperator to the command
    
    is_error = False
    is_codex = False
    
    input_dir = remove_quotes(input_dir)
    output_dir = remove_quotes(output_dir)
    
    if not os.path.isfile(input_dir) and not os.path.isdir(input_dir):
        print("ERR: Input directory not found.")
        is_error = True
    
    if not os.path.exists(output_dir): # If output_dir doesn't exist
        if os.path.isdir(input_dir): # If input_dir is a directory
            os.makedirs(output_dir) # Make output_dir a directory
        else: # If input_dir is a file
            if not os.path.exists(os.path.dirname(output_dir)): # If directory before filename doesn't exist
                os.makedirs(os.path.dirname(output_dir)) # Make it a directory
    
    if args.codex_method.split('.', 1)[0] + ".dll" in [os.path.basename(codex_name) for codex_name in directory_list("./codex/")]:
        is_codex = True
            
    if is_codex == False:
        print("ERR: Codex not available.")
        is_error = True
        
    if args.codex_method.split('.', 1)[1] not in ["encode", "decode"]:
        print("ERR: Invalid Function call.")
        
    if is_error == True:
        print() # Newline before next command
        sys.exit()
        
    # Importing the DLL file

    try:
        codex = ctypes.CDLL("./codex/" + args.codex_method.split('.', 1)[0] + ".dll")
        # codex = ctypes.CDLL("./codex/base64.dll")
    except Exception as e:
        print("DLL loading error:", e)
        
    encode = codex.encode
    encode.restype = ctypes.c_char_p
    encode.argtypes = [ctypes.c_char_p]
    decode = codex.decode
    decode.restype = ctypes.c_char_p
    decode.argtypes = [ctypes.c_char_p]
    
    # Reading file content
    
    start_time = time.time()
    
    for file_name in og_files:
        os.makedirs(os.path.dirname(os.path.join(output_dir, os.path.relpath(file_name, input_dir))), exist_ok=True)
        
        with open(file_name, 'r') as file:
            content = file.read() # Reading file as content
        
        if args.codex_method.split('.', 1)[1] == "encode": # formatting file content
            content = ctypes.string_at(encode(content.encode('utf-8'))).decode('utf-8')
        else:
            content = ctypes.string_at(decode(content.encode('utf-8'))).decode('utf-8')
        
        with open(os.path.join(output_dir, os.path.relpath(file_name, input_dir)), 'w') as file:
            file.write(content) # Writing content to new file
        
    # End time
    
    end_time = time.time()
    
    elapsed_time = (end_time-start_time) * 1000
    
    print(f"{datetime.fromtimestamp(time.time()).strftime('[%I:%M.%S %p]')} Finished in {elapsed_time:.3f} milliseconds.\n")
    
"""-<Run Main>-"""
    
if __name__ == "__main__":
    main()
