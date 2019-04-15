import re


def validateIncidentName(str):
    if(str.isspace()):
        return False
    
    if(len(str) <= 1):
        return False

    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    haveNumber = re.compile('[0-9]')
        
    if(regex.search(str) is not None) or (haveNumber.search(str) is not None):
            return False
    
    else:
        return True