 ______________________________________________________________________________
|                          Python Encryptor/Decryptor                          |
|                                                                              |
|--------------------------------<Installation>--------------------------------|
|                                                                              |
| 1.  Download release: https://github.com/aydon14/Python-Encoder/releases     |
| 2.  Extract files into any folder (Portable installation)                    |
| 3.  Go to source code: https://github.com/aydon14/Python-Encoder             |
| 4.  Download codecs from 'Packs/type', and paste codecs into 'codec' folder  |
|                                                                              |
|----------------------------------< Usage >-----------------------------------|
|                                                                              |
| -h, --help                     Displays options and arguments.               |
|                                                                              |
| --list-codecs                  Lists codex methods. (py files in codec)      |
|                                                                              |
| --codec CODEC.METHOD           The codec and function you want to use.       |
|                                                                              |
| --input FILE/FOLDER            Input file that the program reads to encode.  |
|                                                                              |
| --output FILE/FOLDER           Where the program outputs encoded text.       |
|                                                                              |
|          P.S. --input and --output are for files/folders, not text.          |
|                                                                              |
|-------------------------------< ERR Messages >-------------------------------|
|                                                                              |
|       ERR messages that pop up when arguments are imported incorrectly.      |
|         I tried to make them as clear as possible. Possible messages:        |
|                                                                              |
| - ERR: Input directory not found. # The program couldn't find the path       |
| - ERR: Codec not available. # You entered a codec not supported (Not a file) |
| - ERR: Invalid Function call. # You didn't enter encode or decode            |
| - Module could not be imported. # You didn't enter a valid module/file name  |
| - An error occurred: <exception> # There is an error inside the py file.     |
|                                                                              |
|--------------------------< Developing (DEVS ONLY) >--------------------------|
|   I have added some hidden modules and a template for you to use if you'd    |
|   like. The program is meant to not require python to run, so if you need    |
|     extra libraries, you can compile the source code yourself, or add a      |
|                 suggestion in github. Hidden Imports below:                  |
|         cryptography, base64, hmac, secrets, hashlib, random, struct         |
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
/ /\/ /\/ /\/ /\/ Made by Aydon Fauscett [November 13th, 2023] /\/ /\/ /\/ /\/ /
\/\ \/\ \/\ \/\ \_____________________________________________/\ \/\ \/\ \/\ \/\