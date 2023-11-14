"""-<Libraries>-"""

import argparse, os, time, sys, importlib.util
from datetime import datetime

"""-<Functions>-"""

def parse_arguments():
    """-<Parse Arguments>-"""
    parser = argparse.ArgumentParser(description="Arguments and Definitions:", 
                                     add_help=False)
    parser.add_argument( '-h', '--help', 
                        action='help', 
                        default=argparse.SUPPRESS,
                        help="Displays options and arguments." )
    parser.add_argument( "--list-codecs", 
                        action='store_true', 
                        help="Lists codec methods." )
    parser.add_argument( "--codec", 
                        metavar='CODEC.METHOD', 
                        help="Chooses the codec & method. [<codec name>.[encode or decode]]" )
    parser.add_argument( "--input", 
                        metavar='FILE/FOLDER', 
                        help="File(s) to be read. [c:/path/to/[file or folder]]" )
    parser.add_argument( "--output", 
                        metavar='FILE/FOLDER', 
                        help="File(s) to be made/replaced. [c:/path/to/[file or folder]]" )
    args = parser.parse_args()
    
    if args.list_codecs:
        print()
        dir_list = directory_list("./codec")
        [print(os.path.basename(file).split('.')[0]) for file in dir_list]
        print()
        sys.exit()
        
    if args.codec is None:
        print("\nError: You must provide a codec method using --codec.\n")
        sys.exit()
   
    return args

def module_import(module_path):
   spec = importlib.util.spec_from_file_location("module", module_path)
   custom_module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(custom_module)
   return custom_module

def directory_list(directory):
    """-<List files in a given directory>-"""
    file_list = []
    if os.path.isfile(directory):
        file_list.append(directory)
    else:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_list.append(os.path.join(root, file))
    return file_list

def remove_quotes(path):
    if path and path[0] == '"' and path[-1] == '"':
        return path[1:-1]
    return path

def user_input():
    lines = []
    print("Enter text (press Enter twice to exit):\n")
    
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    
    return "\n".join(lines)

def main():
    """-<Main Method>-"""
    
    """ Main variables and parsing """
    
    args = parse_arguments()
    input_text = False
    codec_list = [os.path.basename(codec_name) for codec_name in directory_list("./codec/")]
    user_codec = args.codec.split('.', 1)[0]
    codec_method = args.codec.split('.', 1)[1]
    
    if args.codec and all( # If only args.codec
        value is None or value is False
        for key, value in vars(args).items() if key != 'codec'
    ):
        input_text = True
        content = user_input()
    else: # Create additional variables
        input_dir = args.input
        output_dir = args.output
        og_files = directory_list(remove_quotes(input_dir))
    
    """ Additional ERR checking """
    
    is_error = False
    is_codec = False
    
    if not input_text:
        print()
        input_dir = remove_quotes(input_dir)
        output_dir = remove_quotes(output_dir)
        
        if not os.path.isfile(input_dir) and not os.path.isdir(input_dir):
            print("ERR: Input directory not found.")
            is_error = True
        
        if not os.path.exists(output_dir): # If output_dir doesn't exist
            if os.path.isdir(input_dir):
                os.makedirs(output_dir)
                
            else: # If input_dir is a file (not a folder)
                if not os.path.exists(os.path.dirname(output_dir)): # If directory before filename doesn't exist
                    os.makedirs(os.path.dirname(output_dir))
    
    if user_codec + ".py" in codec_list:
        is_codec = True
            
    if is_codec == False:
        print("ERR: Codec not available.")
        is_error = True
        
    if codec_method not in ["encode", "decode"]:
        print("ERR: Invalid Function call.")
        
    if is_error == True:
        print() # Newline before next command
        sys.exit()
        
    """ Importing the py file """

    try:
        module_location = os.path.abspath("./codec/" + user_codec + ".py")
        module = module_import(module_location)
    except ModuleNotFoundError:
        print(f"Module {user_codec} could not be imported.\n")
        sys.exit()
    except Exception as e:
        print(f"An error occurred: {str(e)}\n")
        sys.exit()
    
    """ Recoding content """
    
    start_time = time.time()
    
    if input_text: # Handling input text
        if codec_method == "encode":
            content = module.encode(content)
        else:
            content = module.decode(content)
    else: # Handling files
        for file_name in og_files:
            # If input  -> file, output -> file
            if os.path.isfile(input_dir) and os.path.isfile(output_dir):
                with open(file_name, 'r') as file:
                    content = file.read()

                if codec_method == "encode":
                    content = module.encode(content)
                else:
                    content = module.decode(content)

                with open(output_dir, 'w') as file:
                    file.write(content)
                    
            # If input -> file, output -> folder
            elif os.path.isfile(input_dir) and os.path.isdir(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                output_file_path = os.path.join(output_dir, os.path.basename(file_name))

                with open(file_name, 'r') as file:
                    content = file.read()

                if codec_method == "encode":
                    content = module.encode(content)
                else:
                    content = module.decode(content)

                with open(output_file_path, 'w') as file:
                    file.write(content)
            # If input -> folder, output -> folder
            else:
                # Makes new folders inside main directory
                relative_path = os.path.relpath(file_name, input_dir)
                os.makedirs(os.path.join(output_dir, os.path.dirname(relative_path)), exist_ok=True)

                with open(file_name, 'r') as file:
                    content = file.read() 

                if codec_method == "encode":
                    content = module.encode(content)
                else:
                    content = module.decode(content)

                with open(os.path.join(output_dir, relative_path), 'w') as file:
                    file.write(content)
        
    """ End time """
    
    end_time = time.time()
    
    elapsed_time = (end_time-start_time) * 1000
    
    print(f"{datetime.fromtimestamp(time.time()).strftime('[%I:%M.%S %p]')} Finished in {elapsed_time:.3f} milliseconds.\n")
    
    if input_text:
        print(f"New text:\n\n{content}\n")
    
"""-<Run Main>-"""
    
if __name__ == "__main__":
    main()
