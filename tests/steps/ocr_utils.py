import difflib

"""This method returns True if the strings matches greater than the threshold provided"""
def fuzzy_match(string1, string2, threshold):
    return difflib.SequenceMatcher(None, string1, string2).ratio() >= threshold