 ______________________________________________________________________________
|                            Python Encoder/Decoder                            |
|                                                                              |
|      I'm going to make this short and simple. This program encodes and       |
|       decodes files, but not text. Text will be added in the future. I       |
|          am also looking to make this cross-platform in the future.          |
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
|       PS - Make sure you use codex-method, input-file, and output-file       |
|                 together, or you will get an error on start.                 |
|                                                                              |
|-------------------------------< ERR Messages >-------------------------------|
|                                                                              |
|       ERR messages that pop up when arguments are imported incorrectly.      |
|         I tried to make them as clear as possible. Possible messages:        |
|                                                                              |
| - ERR: Input directory not found. # The program couldn't find the path       |
| - ERR: Codex not available. # You entered a codex not supported (Not a DLL)  |
| - ERR: Invalid Function call. # You didn't enter encode or decode            |
| - DLL loading error: <exception> # The DLL file isn't formatted correctly.   |
|                                                                              |
|--------------------------< Developing (DEVS ONLY) >--------------------------|
|                                                                              |
|   This project was coded with Python. The problem is, python doesn't have    |
|    native DLL support, so the DLL codex files have to be made with C/C++.    |
|     I will supply templates for DLL files below if you want to make your     |
|           own codex/encoding method. Compilations for MinGW below:           |
|                                                                              |
|  MinGW GCC - gcc -shared -o <filename>.dll -Wall -Werror -fpic <filename>.c  |
| MinGW G++ - g++ -shared -o <filename>.dll -Wall -Werror -fpic <filename>.cpp |
|______________________________________________________________________________|
<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<> C Template <>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>

char* encode(const char* input) {
    // Code goes here
    char* output;
    return output;
}
char* decode(const char *input) {
    // Code goes here
    char* output;
    return output;
}

<>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<> C++ Template <>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<>

extern "C" {
    __declspec(dllexport) const char* encode(const char* input) {
        // Code goes here
        string output;
        return output.c_str();
    }
    __declspec(dllexport) const char* decode(const char* input) {
        // Code goes here
        string output;
        return output.c_str();
    }
}

<>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<=>-<>