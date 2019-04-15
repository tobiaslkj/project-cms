import re
from flaskapp.utility.Address import getAddress



def validateIncidentAddress(address):
    if(address.isspace()):
        return False
    
    if(len(address)<=2):
        return False
    
    regex = re.compile('[_!$%^&*<>?/\|}{~:]')

    if (regex.search(address) is not None):
        return False

    result = getAddress(address)

    if(result is None):
        return False
 
    else:
        return True