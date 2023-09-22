"""
This module implements functions to manipulate mesonh namelist
"""

def getKeysValue(nam, keyName):
    """
    If found, returns the value of a given namelist key
    If not found, returns keyValue='' and keyValueString=keyName
    """
    index = nam.find(keyName)
    terminating_symbol= {',', '/'}
    keyValueString = keyName
    keyValue = ''
    value_found = False
    if index != -1:
        next_char = nam[index+len(keyName)]
        while not value_found:
            if next_char in terminating_symbol:
                value_found = True
            else:
                keyValue = keyValue + next_char
                index+=1
            next_char = nam[index+len(keyName)]
    keyValueString = keyName + keyValue
    keyValue=keyValue.replace('=','')
    keyValue=keyValue.replace(' ','')
    return keyValueString, keyValue

def nextSignificantChar(nam, index):
    """
    Return the next character following the one at index position which are not space, not \n 
    Does not handle FORTRAN comment for now
    """
    for el in nam[index+1:]:
        if el == ' ' or el == '\n':
            pass
        else:
            return el

def cleanCommas(nam):
    """
    Remove all single ',' before a '/'
    eg. &NAM_CONF NMODEL=1, / becomes &NAM_CONF NMODEL=1 /
    """
    found=True
    while found: 
        for index,el in enumerate(nam):
            found=False
            if el == ',':
                nextSymbol = nextSignificantChar(nam, index)
                if nextSymbol == '/' or nextSymbol == ',':
                    found=True
                    newnam = nam[:index] + nam[index+1:]
                    if nextSymbol == ',': # This specificity is for removing the second ',' instead of the first one to avoid a \n with a ',' alone
                        newnam = nam[:index+1] + nam[index+2:]
                    nam = newnam
                    break
    return nam    