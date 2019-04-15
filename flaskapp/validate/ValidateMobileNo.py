import re

def validateMobileNo(str):
    if (len(str) != 8):
        return False
    

    pattern = re.compile("(9/8)?[0-9]{8}")
    
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    hasAlphabet = re.compile('[a-zA-Z]')
    hasNumber = re.compile('[0-9]')

    if(regex.search(str) is not None) or (hasAlphabet.search(str) is not None):
        return False
    
    if(pattern.match(str) is False):
        return False

    else:
        return True
    
