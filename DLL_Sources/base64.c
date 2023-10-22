#include <stdio.h>
#include <string.h>
#include <stdlib.h>

const char base64_chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

char* encode(const char* input) {
    size_t input_len = strlen(input);
    size_t output_len = 4 * ((input_len + 2) / 3); // Calculate the length of the encoded string
    char* output = (char*)malloc(output_len + 1); // +1 for null terminator

    if (output) {
        size_t i = 0;
        size_t j = 0;

        while (i < input_len) {
            unsigned char char_array_3[3] = {0};
            unsigned char char_array_4[4] = {0};

            for (int k = 0; k < 3 && i < input_len; k++) {
                char_array_3[k] = input[i++];
            }

            char_array_4[0] = (char_array_3[0] & 0xFC) >> 2;
            char_array_4[1] = ((char_array_3[0] & 0x03) << 4) | ((char_array_3[1] & 0xF0) >> 4);
            char_array_4[2] = ((char_array_3[1] & 0x0F) << 2) | ((char_array_3[2] & 0xC0) >> 6);
            char_array_4[3] = char_array_3[2] & 0x3F;

            for (int k = 0; k < 4; k++) {
                output[j++] = base64_chars[char_array_4[k]];
            }
        }

        // Add padding characters if necessary
        while (j < output_len) {
            output[j++] = '=';
        }

        output[output_len] = '\0'; // Null-terminate the output
    }

    return output;
}

char* decode(const char *input) {
    size_t input_len = strlen(input);

    size_t output_len = (input_len / 4) * 3;
    if (input[input_len - 1] == '=') {
        output_len--;
    }
    if (input[input_len - 2] == '=') {
        output_len--;
    }

    char *decoded_output = (char*)malloc(output_len + 1); // +1 for null terminator

    if (decoded_output) {
        size_t i = 0;
        size_t j = 0;

        while (i < input_len) {
            unsigned char char_array_4[4] = {0};
            unsigned char char_array_3[3] = {0};

            for (int k = 0; k < 4; k++) {
                char_array_4[k] = strchr(base64_chars, input[i++]) - base64_chars;
            }

            char_array_3[0] = (char_array_4[0] << 2) | (char_array_4[1] >> 4);
            char_array_3[1] = (char_array_4[1] << 4) | (char_array_4[2] >> 2);
            char_array_3[2] = (char_array_4[2] << 6) | char_array_4[3];

            for (int k = 0; k < 3; k++) {
                decoded_output[j++] = char_array_3[k];
            }
        }

        decoded_output[output_len] = '\0'; // Null-terminate the output
        return decoded_output; // Decoding successful
    }

    return NULL; // Memory allocation failed
}