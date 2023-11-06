 ______________________________________________________________________________
|                            Python Encoder/Decoder                            |
|                                                                              |
|--------------------------------<Installation>--------------------------------|
|                                                                              |
| 1. Download release: https://github.com/aydon14/Python-Encoder/releases      |
| 2. Extract files into any folder (Portable installation)                     |
| 3. Go to source code: https://github.com/aydon14/Python-Encoder              |
| 4. Download selected codecs, and paste codecs into 'codex' folder            |
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
|   I have added some hidden modules and a template for you to use if you'd    |
|   like. The program is meant to not require python to run, so if you need    |
|     extra libraries, you can compile the source code yourself, or add a      |
|                 suggestion in github. Hidden Imports below:                  |
|                 cryptography, base64, hmac, secrets, hashlib                 |
|______________________________________________________________________________|
+-----------------------------< Python3 Template >-----------------------------+

def encode(input): 
    output = <encoded input>
    return output
                            # Takes a string, returns a string
def decode(input):
    output = <decoded input>
    return output

_______________________________________________________________________________
\/\ \/\ \/\ \/\ \/                                             \ \/\ \/\ \/\ \/\
/ /\/ /\/ /\/ /\/ Made by Aydon Fauscett  [November 5th, 2023] /\/ /\/ /\/ /\/ /
\/\ \/\ \/\ \/\ \_____________________________________________/\ \/\ \/\ \/\ \/\