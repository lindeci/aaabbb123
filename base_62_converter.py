#!/usr/bin/env python

#
# Converts any integer into a base [BASE] number. I have chosen 62
# as it is meant to represent the integers using all the alphanumeric
# characters, [no special characters] = {0..9}, {A..Z}, {a..z}
#
# I plan on using this to shorten the representation of possibly long ids,
# a la url shortenters
#
# saturate()  takes the base 62 key, as a string, and turns it back into an integer
# dehydrate() takes an integer and turns it into the base 62 string
#
import math
import sys

BASE = 62
SHORT_URL_LEN = 9

UPPERCASE_OFFSET = 65 - 10 - 26
LOWERCASE_OFFSET = 97 - 10
DIGIT_OFFSET = 48

def char_to_int(char):
    """
    Turns a digit [char] in character representation
    from the number system with base [BASE] into an integer.
    """
    
    if char.isdigit():
        return ord(char) - DIGIT_OFFSET
    elif 'A' <= char <= 'Z':
        return ord(char) - UPPERCASE_OFFSET
    elif 'a' <= char <= 'z':
        return ord(char) - LOWERCASE_OFFSET
    else:
        raise ValueError("%s is not a valid character" % char)

def int_to_char(integer):
    """
    Turns an integer [integer] into digit in base [BASE]
    as a character representation.
    """
    if 0<= integer < 10:
        return chr(int(integer + DIGIT_OFFSET))
    elif 10 <= integer <= 35:
        return chr(int(integer + LOWERCASE_OFFSET))
    elif 36 <= integer < 62:
        return chr(int(integer + UPPERCASE_OFFSET))
    else:
        raise ValueError("%d is not a valid integer in the range of base %d" % (integer, BASE))


def string_to_int(key):
    """
    Turn the base [BASE] number [key] into an integer
    """
    int_sum = 0
    reversed_key = key[::-1]
    for idx, char in enumerate(reversed_key):
        int_sum += char_to_int(char) * int(math.pow(BASE, idx))
    return int_sum


def int_to_string(integer):
    """
    Turn an integer [integer] into a base [BASE] number
    in string representation
    """
    
    # we won't step into the while if integer is 0
    # so we just solve for that case here
    if integer == 0:
        return '0'
    
    string = ""
    while integer >= 0:
        remainder = integer % BASE
        # fix string startwith 0
        if integer == 0:
            break
        string = int_to_char(remainder) + string
        integer = int(integer / BASE)
    return string.zfill(SHORT_URL_LEN)

if __name__ == '__main__':
    
    # not really unit tests just a rough check to see if anything is way off
    if sys.argv[1] == '-tests':
        passed_tests = True
        for i in xrange(0, 1000):
            passed_tests &= (i == (int_to_string(i)))
        print(passed_tests)
    else:
        user_input = sys.argv[2]
        try:
            if sys.argv[1] == '-s':
                print(string_to_int(user_input))
            elif sys.argv[1] == '-d':
                print(int_to_string(int(user_input)))
            else:
                print("I don't understand option %s" % sys.argv[1])
        except ValueError as e:
            print(e)
