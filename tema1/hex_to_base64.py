import base64
import sys
import re

hex_pattern = re.compile("^[a-fA-F0-9]+$")
constants64 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']

def hex_to_base64(str_for_conversion):
    str_len = len(str_for_conversion)
    result = ""

    for index in range (0, str_len, 3):
        chunk_to_dec = int(str_for_conversion[index:index + 3], 16)
        result += dec_to_base64ch(chunk_to_dec / 64)

        if chunk_to_dec >= 64:
            result += dec_to_base64ch(chunk_to_dec % 64)

    return result

def dec_to_base64ch(dec):
    if dec < 0 or dec > 63:
        print "Invalid number %s. It should be from interval [0, 64)"
        return

    return constants64[dec]

if __name__ == "__main__":
    string_for_conversion = raw_input('Insert the string for conversion\n')
    print "\n\n"

    if hex_pattern.match(string_for_conversion) is None:
        print "%s is not a valid hex string" % string_for_conversion
        sys.exit()

    print "Result using base64 module          : %s" % base64.encodestring(string_for_conversion.decode('hex'))
    print "Result using my conversion function : %s" % hex_to_base64(string_for_conversion)
