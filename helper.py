#!/usr/bin/python

import string


#Checks if a string is a number
def isNumber(s):
    try:
        floatVal = float(s)
        return True
        
    except ValueError:
        return False




