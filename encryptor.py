import argparse, os, time, sys, importlib.util

def main_arguments():
    """-<Parse Arguments>-"""
    parser = argparse.ArgumentParser(description="Arguments and Definitions:", 
                                     add_help=False)
    parser.add_argument('-h', '-help', 
                        action='help', 
                        default=argparse.SUPPRESS,
                        help="Displays options and arguments." )
    parser.add_argument("-list-codecs", 
                        action='store_true', 
                        help="Lists codec methods." )
    parser.add_argument("-codec", 
                        metavar='CODEC.METHOD', 
                        help="Chooses the codec & method. [<file name>.<encode or decode>]" )
    parser.add_argument("-in-dir", 
                        metavar='FILE/FOLDER', 
                        help="File(s) to be read. [c:/path/to/<file or folder>]" )
    parser.add_argument("-out-dir", 
                        metavar='FILE/FOLDER', 
                        help="File(s) to be made/replaced. [c:/path/to/<file or folder>]" )
    
    sys_args, file_args = parser.parse_known_args()
    
    # List codecs and exit.
    
    if sys_args.list_codecs:
        print()
        dir_list = directory_list("./codec")
        [print(os.path.basename(file).split('.')[0]) for file in dir_list]
        print()
        sys.exit()
        
    # Verify codec argument
    
    codec_list = [os.path.basename(codec) for codec in directory_list("./codec/")]
    
    if sys_args.codec is None:
        print("\nError: You must provide a codec method using -codec.\n")
        sys.exit()
        
    codec = sys_args.codec.split('.', 1)[0] + '.py'
    codec_method = (sys_args.codec.split('.', 1)[1]).lower()
    
    if codec not in codec_list:
        print("\nError: Chosen codec is not available. Use -list-codecs.\n")
        sys.exit()
        
    if codec_method not in ['encrypt', 'decrypt']:
        print("\nError: Chosen method isn't encrypt or decrypt.\n")
        sys.exit()
        
    # If there is no in-dir/out-dir, then the user will type it in later.
   
    return sys_args, file_args

def file_arguments(module, file_args, is_encrypt=True):
    parser = argparse.ArgumentParser()
    
    arg_dict = module.encrypt_args if is_encrypt else module.decrypt_args
    
    for key in arg_dict:
        parser.add_argument('--' + key)
            
    args = parser.parse_args(file_args)
    
    for arg in arg_dict:
        if arg_dict[arg] == 'any' or arg == 'input':
            pass
        else:
            while len(getattr(args, arg)) not in arg_dict[arg]:
                length_strings = [str(length) for length in arg_dict[arg]]
                prompt = arg.title() + ' has to be '
                if len(length_strings) == 1:
                    prompt += length_strings[0]
                else:
                    prompt += ', '.join(length_strings[:-1]) + ' or ' + length_strings[-1]
                prompt += ' bytes long. Try again: '

                setattr(args, arg, input(prompt))
            
    arg_dict = vars(args)

    return arg_dict

def module_import(module_path):
   spec = importlib.util.spec_from_file_location("module", module_path)
   custom_module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(custom_module)
   return custom_module

def directory_list(directory):
    file_list = []
    if os.path.isfile(directory):
        file_list.append(directory)
    else:
        for root, _, files in os.walk(directory):
            for file in files:
                file_list.append(os.path.join(root, file))
    return file_list

def remove_quotes(path):
    if isinstance(path, str):
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
    # Set/Verify program-wide arguments and variables
    # Note: I'm using 'sys' as a shortcut to program-wide, NOT system-wide
    
    sys_args, file_args = main_arguments()
    input_dir = remove_quotes(sys_args.in_dir)
    output_dir = remove_quotes(sys_args.out_dir)
    is_encrypt = True if sys_args.codec.split('.', 1)[1] == 'encrypt' else False

    # Importing the chosen codec file
    
    try:
        module = module_import(os.path.abspath("./codec/" + sys_args.codec.split('.', 1)[0] + ".py"))
    except Exception as e:
        print(f"An error occurred: {str(e)}\n")
        sys.exit()
        
    # Set File arguments
    
    file_args = file_arguments(module, file_args, is_encrypt)
    
    # User input (Optional)
    
    if input_dir is None:
        input_text = user_input()
        
        lengths = module.encrypt_args['input'] if is_encrypt else module.decrypt_args['input']
        
        while lengths != ['any'] and len(input_text) not in lengths:
            length_strings = [str(length) for length in lengths]
            prompt = 'Input has to be '
            if len(length_strings) == 1:
                prompt += length_strings[0]
            else:
                prompt += ', '.join(length_strings[:-1]) + ' or ' + length_strings[-1]
            prompt += ' bytes long. Try again: '
            
            input_text = input(prompt)
            
        file_args['input'] = input_text.encode('latin-1')
    elif (not os.path.isfile(input_dir) and
          not os.path.isdir(input_dir)):
        print("ERR: Input directory not found.")
        sys.exit()
        
    # Reading and encrypting content (Main procedure)
    
    if input_dir is None: # Handling input text
        if is_encrypt:
            content = module.encrypt(*file_args.values())
        else:
            content = module.decrypt(*file_args.values())
            
        print(f"New text:\n\n{content.decode('latin-1')}\n")
            
    else: # Handling files
        # if output directory doesn't exist:
        #     if input directory is a folder:
        #         Make output a directory
        #     if input directory is a file:
        #         Make parent output directory exist
        if not os.path.exists(output_dir):
            if os.path.isdir(input_dir):
                os.makedirs(output_dir)
            else:
                if not os.path.exists(os.path.dirname(output_dir)):
                    os.makedirs(os.path.dirname(output_dir))
        
        for file_name in directory_list(input_dir):
            # If input  -> file, output -> file
            if os.path.isfile(input_dir) and os.path.isfile(output_dir):
                with open(file_name, 'rb') as file:
                    file_args['input'] = file.read()

                if is_encrypt:
                    content = module.encrypt(*file_args.values())
                else:
                    content = module.decrypt(*file_args.values())

                with open(output_dir, 'wb') as file:
                    file.write(content)
                    
            # If input -> file, output -> folder
            elif os.path.isfile(input_dir) and os.path.isdir(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                output_file_path = os.path.join(output_dir, os.path.basename(file_name))

                with open(file_name, 'rb') as file:
                    file_args['input'] = file.read()

                if is_encrypt:
                    content = module.encrypt(*file_args.values())
                else:
                    content = module.decrypt(*file_args.values())

                with open(output_file_path, 'wb') as file:
                    file.write(content)
            # If input -> folder, output -> folder
            else:
                relative_path = os.path.relpath(file_name, input_dir)
                os.makedirs(os.path.join(output_dir, os.path.dirname(relative_path)), exist_ok=True)

                with open(file_name, 'rb') as file:
                    file_args['input'] = file.read()

                if is_encrypt:
                    content = module.encrypt(*file_args.values())
                else:
                    content = module.decrypt(*file_args.values())

                with open(os.path.join(output_dir, relative_path), 'wb') as file:
                    file.write(content)

if __name__ == "__main__":
    main()