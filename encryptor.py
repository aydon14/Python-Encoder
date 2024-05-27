import argparse, os, sys, importlib.util, inspect

def main_arguments():
    """-<Parse Arguments>-"""
    parser = argparse.ArgumentParser(description="Arguments and Definitions:", 
                                     add_help=False)
    parser.add_argument('-h', '-help', 
                        action='help', 
                        default=argparse.SUPPRESS, 
                        help="Displays options and arguments." )
    parser.add_argument('--list-codecs', '-lc', 
                        action='store_true', 
                        help="Listof available codecs." )
    parser.add_argument('--codec', '-c', 
                        metavar='CODEC.METHOD', 
                        help="Codec & Operation. (encrypt or decrypt)" )
    parser.add_argument('--in-dir', '-i', 
                        metavar='FILE PATH', 
                        help="Input files." )
    parser.add_argument('--out-dir', '-o', 
                        metavar='FILE PATH', 
                        help="Output files." )
    parser.add_argument('--repeat', '-r', 
                        metavar='INTEGER', 
                        default=1,
                        help="Number of iterations for encryption." )
    
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
    
    if not sys_args.codec:
        print("\nERR: You must provide a codec method using -c.\n")
        sys.exit()
        
    codec = sys_args.codec.split('.', 1)[0] + '.py'
    codec_method = (sys_args.codec.split('.', 1)[1]).lower()
    
    if codec not in codec_list:
        print("\nERR: Chosen codec is not available. Use -lc.\n")
        sys.exit()
        
    if codec_method not in ['encrypt', 'decrypt', 'gen_keys']:
        print("\nERR: Invalid method chosen.\n")
        sys.exit()
    
    # Verify iterations/repeat argument
    
    try:
        sys_args.repeat = int(sys_args.repeat)
        if sys_args.repeat <= 0:
            print("\nERR: Iteration argument is not a valid integer.\n")
            sys.exit()
    except ValueError:
        print("\nERR: Iteration argument is not a valid integer.\n")
        sys.exit()
    
    # If there is no in-dir/out-dir, then the user will type it in later.
   
    return sys_args, file_args

def file_arguments(arg_dict, file_args):
    parser = argparse.ArgumentParser()
    
    for key in arg_dict:
        parser.add_argument('--' + key)
            
    args = parser.parse_args(file_args)
    
    for arg, value in vars(args).items():
        if value is None:
            setattr(args, arg, '')
    
    for arg in arg_dict:
        if arg_dict[arg] is None or arg in ['input', 'IE']:
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

def get_var_names(func):
    source_lines = inspect.getsource(func).split('\n')
    
    return_line_index = -1
    for i, line in enumerate(source_lines):
        if line.strip().startswith("return "):
            return_line_index = i
            break
    
    if return_line_index != -1:
        return_line = source_lines[return_line_index]
        returned_variables = return_line.split("return ")[1].split(",")
        return [var.strip() for var in returned_variables[1:]]
    else:
        return []

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
    additional_data = []

    # Importing the codec file
    
    try:
        module = module_import(os.path.abspath("./codec/" + sys_args.codec.split('.', 1)[0] + ".py"))
    except Exception as e:
        print(f"ERR: {str(e)}\n")
        sys.exit()
        
    # Generate keys (Asymmetric)
    
    if sys_args.codec.split('.', 1)[1] == 'gen_keys':
        public_key, private_key = module.generate_keys()
        
        print(f'\nPublic Key: {public_key}\nPrivate Key: {private_key}\n')
    else: 
        # Set File arguments
        
        arg_dict = module.encrypt_args if is_encrypt else module.decrypt_args
        
        file_args = file_arguments(arg_dict, file_args)
        
        # Check iterative encryption
        
        if (not arg_dict['IE']) and (sys_args.repeat > 1):
            print("\nERR: Chosen codec doesn't support iterative encryption.\n")
            sys.exit()
            
        del file_args['IE']
            
        if sys_args.codec.split('.', 1)[1] == 'gen_keys' and (not hasattr(module, 'generate_keys')):
            print("ERR: Cipher is not asymmetric or gen_keys function doesn't exist.")
            sys.exit()
        
        # User input (Optional)
        
        if input_dir is None:
            input_text = user_input()
            
            lengths = module.encrypt_args['input'] if is_encrypt else module.decrypt_args['input']
            
            while lengths is not None and len(input_text) not in lengths:
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
            if hasattr(module, 'pad') and is_encrypt:
                file_args['input'] = module.pad(file_args['input'], module.block_size)
                
            if is_encrypt:
                for _ in range(sys_args.repeat):
                    result = module.encrypt(*file_args.values())
                    content, *ad_values = result if isinstance(result, (tuple, list)) else [result]
                    file_args['input'] = content
                    additional_data.extend(ad_values)
            else:
                for _ in range(sys_args.repeat):
                    result = module.decrypt(*file_args.values())
                    content, *ad_values = result if isinstance(result, (tuple, list)) else [result]
                    file_args['input'] = content
                    additional_data.extend(ad_values)
                
            if hasattr(module, 'unpad') and not is_encrypt:
                content = module.unpad(content)
                
            print(f"New text:\n\n{content.decode('latin-1')}\n")
                
        else: # Handling files
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
                        
                    if hasattr(module, 'pad') and is_encrypt:
                        file_args['input'] = module.pad(file_args['input'], module.block_size)

                    if is_encrypt:
                        for _ in range(sys_args.repeat):
                            result = module.encrypt(*file_args.values())
                            content, *ad_values = result if isinstance(result, (tuple, list)) else [result]
                            file_args['input'] = content
                            additional_data.extend(ad_values)
                    else:
                        for _ in range(sys_args.repeat):
                            result = module.decrypt(*file_args.values())
                            content, *ad_values = result if isinstance(result, (tuple, list)) else [result]
                            file_args['input'] = content
                            additional_data.extend(ad_values)
                        
                    if hasattr(module, 'unpad') and not is_encrypt:
                        content = module.unpad(content)

                    with open(output_dir, 'wb') as file:
                        file.write(content)
                        
                # If input -> file, output -> folder
                elif os.path.isfile(input_dir) and os.path.isdir(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                    output_file_path = os.path.join(output_dir, os.path.basename(file_name))

                    with open(file_name, 'rb') as file:
                        file_args['input'] = file.read()
                        
                    if hasattr(module, 'pad') and is_encrypt:
                        file_args['input'] = module.pad(file_args['input'], module.block_size)

                    if is_encrypt:
                        for _ in range(sys_args.repeat):
                            result = module.encrypt(*file_args.values())
                            content, *ad_values = result if isinstance(result, (tuple, list)) else [result]
                            file_args['input'] = content
                            additional_data.extend(ad_values)
                    else:
                        for _ in range(sys_args.repeat):
                            result = module.decrypt(*file_args.values())
                            content, *ad_values = result if isinstance(result, (tuple, list)) else [result]
                            file_args['input'] = content
                            additional_data.extend(ad_values)
                        
                    if hasattr(module, 'unpad') and not is_encrypt:
                        content = module.unpad(content)

                    with open(output_file_path, 'wb') as file:
                        file.write(content)
                # If input -> folder, output -> folder
                else:
                    relative_path = os.path.relpath(file_name, input_dir)
                    os.makedirs(os.path.join(output_dir, os.path.dirname(relative_path)), exist_ok=True)

                    with open(file_name, 'rb') as file:
                        file_args['input'] = file.read()
                        
                    if hasattr(module, 'pad') and is_encrypt:
                        file_args['input'] = module.pad(file_args['input'], module.block_size)

                    if is_encrypt:
                        for _ in range(sys_args.repeat):
                            result = module.encrypt(*file_args.values())
                            content, *ad_values = result if isinstance(result, (tuple, list)) else [result]
                            file_args['input'] = content
                            additional_data.extend(ad_values)
                    else:
                        for _ in range(sys_args.repeat):
                            result = module.decrypt(*file_args.values())
                            content, *ad_values = result if isinstance(result, (tuple, list)) else [result]
                            file_args['input'] = content
                            additional_data.extend(ad_values)
                        
                    if hasattr(module, 'unpad') and not is_encrypt:
                        content = module.unpad(content)

                    with open(os.path.join(output_dir, relative_path), 'wb') as file:
                        file.write(content)
                        
        # Dealing with additional returned values

        ad_var_names = get_var_names(module.encrypt if is_encrypt else module.decrypt)
        name_counter = {}
        
        if len(additional_data) > 0:
            print("\nAdditional returned values:\n")
        
        for i, value in enumerate(additional_data):
            base_name = ad_var_names[i % len(ad_var_names)]
            
            if base_name in name_counter:
                name_counter[base_name] += 1
            else:
                name_counter[base_name] = 1
                
            if name_counter[base_name] == 1:
                name = base_name
            else:
                name = f"{base_name}_{name_counter[base_name]}"
            
            print(f"{name.title()}: {value}")
            
        print()

if __name__ == "__main__":
    main()