 ______________________________________________________________________________
|                            Python Encoder/Decoder                            |
|                                                                              |
|      I'm going to make this short and simple. This program encodes and       |
|       decodes files, but not text. Text will be added in the future. I       |
|          am also looking to make this cross-platform in the future.          |
|  P.S. This is a remake of the old version with DLL files. Check alpha 1.0.0  |
|                                                                              |
|----------------------------------< Usage >-----------------------------------|
|                                                                              |
| -h, --help                     Lists commands like you see now.              |
|                                                                              |
| --list-methods                 Lists codex methods. (DLL files in codex)     |
|                                                                              |
| --codex-method CODEX_METHOD    Chooses the DLL file & codex function.        |
|                                Formatted as <codex>.<function>               |
|                                Codex - encoding method                       |
|                                Function - encode or decode                   |
|                                Example: base64.encode                        |
|                                                                              |
| --input-file INPUT_FILE        Input file that the program reads to encode.  |
|                                                                              |
| --output-file OUTPUT_FILE      Where the program outputs encoded text.       |
|                                                                              |
|        NEW - If you only use --codex-method, then you can enter text         |
|        in the program, and it will return your encoded/decoded text.         |
|                                                                              |
|-------------------------------< ERR Messages >-------------------------------|
|                                                                              |
|       ERR messages that pop up when arguments are imported incorrectly.      |
|         I tried to make them as clear as possible. Possible messages:        |
|                                                                              |
| - ERR: Input directory not found. # The program couldn't find the path       |
| - ERR: Codex not available. # You entered a codex not supported (Not a DLL)  |
| - ERR: Invalid Function call. # You didn't enter encode or decode            |
| - Module could not be imported. # You didn't enter a valid module/file name  |
| - An error occurred: <exception> # There is an error inside the py file.     |
|                                                                              |
|--------------------------< Developing (DEVS ONLY) >--------------------------|
|   My goal here was to add cross platform support. This can really only be    |
|  achieved using .py files. The problem is module support. I have added some  |
|  hidden modules and a template for you to use if you'd like. The program is  | 
|     meant to not require python to run, so if you need extra libraries,      |
|              you can compile the source code yourself, or add a              |
|                 suggestion in github. Hidden Imports below:                  |
|                 cryptography, base64, hmac, secrets, hashlib                 |
|______________________________________________________________________________|
<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=> Python3 Template <=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>

def encode(input): 
    output = <encoded input>
    return output
                            # Takes a string, returns a string
def decode(input):
    output = <decoded input>
    return output

<>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<>

                   Made by Aydon Fauscett [October 29th, 2023]