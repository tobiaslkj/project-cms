import re

def validateMobileNo(str):
    if (len(str) != 8):
        return False
    
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    hasAlphabet = re.compile('[a-zA-Z]')
    hasNumber = re.compile('[0-9]')

    if(regex.search(str) is not None) or (hasAlphabet.search(str) is not None):
        return False

    else:
        return True
    
