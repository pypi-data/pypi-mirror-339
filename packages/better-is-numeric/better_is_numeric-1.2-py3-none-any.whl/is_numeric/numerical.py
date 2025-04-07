"""
An enhancement of str.isnumeric()
"""

from re import fullmatch
from io import StringIO
from typing import Union

NM_ALLOW_NEGATIVE = "AN"
NM_ALLOW_DECIMALS = "AD"
NM_ALLOW_LEADING_ZERO = "AZ"
NM_ALLOW_PLUS_SIGN = "AP"
# NM_ALLOW_COMMAS = "AC" # too difficult for now
#above Set to the string "AC", this flag allows comma-separated numbers like 1,000,000. Useful if you don't need to actually cast to a number.
NM_RETURN_MATCH = "RM"
NM_RETURN_REGEX = "RX"

def is_numeric(string:str, flags:Union[set[str], list[str]]=None):
    """
    This function uses a "flag" system to control what's allowed and what isn't.
    You can pass these in a set called "flags" in the arguments.
    Certain flags switch the function to dictionary output, to include whatever data you requested.
    The simple boolean output is still included in the dictionary output, in the "numeric" field.
    The flags are in variables, but you can also use their string values.
    1: NM_ALLOW_NEGATIVE - Set to the string "AN" and enabled by default, this flag allows negative numbers.
    2: NM_ALLOW_DECIMALS - Set to the string "AD", this flag allows numbers with decimals.
    3: NM_ALLOW_LEADING_ZERO - Set to the string "AZ", this flag allows "invalid" numbers like 01.
    4: NM_ALLOW_PLUS_SIGN - Set to the string "AP", this flag allows explicitly positive numbers, such as +2.
    5: NM_RETURN_MATCH - Set to the string "RM", this flag uses dictionary output and returns the raw output of the match function inside the "match" field.
    6: NM_RETURN_REGEX - Set to the string "RX", this flag uses dictionary output and returns the constructed regex inside the "regex" field.
    """
    if flags is None: # this is ugly and adds unnecessary lines but my IDE complained
        flags = {NM_ALLOW_NEGATIVE}
    if isinstance(flags, list): # i want to use type(flags) == list, but i think this is generally preferred?
        flags = set(flags)
    regex = StringIO() # should be faster than being a string and using regex += "stuff"
    AllowNegative = NM_ALLOW_NEGATIVE in flags
    AllowPlus = NM_ALLOW_PLUS_SIGN in flags
    if AllowNegative or AllowPlus: # avoid re-doing checks by using variables. there are a lot of if statements here its crazy we need to conserve resources
        AllowBoth = AllowNegative and AllowPlus
        if AllowBoth:
            regex.write(r"(")
        if AllowNegative:
            regex.write(r"-?") # allow zero or one (no more than one) minus symbols
        if AllowBoth:
            regex.write(r"|")
        if AllowPlus:
            regex.write(r"\+?")
        if AllowBoth:
            regex.write(r")")
    if NM_ALLOW_LEADING_ZERO in flags:
        regex.write(r"\d+") # allow one or more digits. must be digits
    else:
        regex.write(r"([1-9]\d*|0)") # allows either: a non-zero digit followed by any (including zero) amount of any digits OR a single zero
    if NM_ALLOW_DECIMALS in flags:
        regex.write(r"(\.\d+)?") # allow zero or one instances of: a decimal point followed by one or more digits
    regex.seek(0)
    regex = regex.read()
    match = fullmatch(regex, string) # instead of writing to the StringIO twice to ensure the whole string matches, we just use fullmatch
    ReturnMatch = NM_RETURN_MATCH in flags # same optimization as earlier with negative and positive
    ReturnRegex = NM_RETURN_REGEX in flags
    if ReturnMatch or ReturnRegex:
        output = {"numeric": bool(match)} # ensure the user still gets the simple output as well as whatever they want
        if ReturnMatch:
            output["match"] = match
        if ReturnRegex:
            output["regex"] = regex
        return output
    else:
        return bool(match)