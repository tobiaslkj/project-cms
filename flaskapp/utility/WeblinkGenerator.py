import uuid

def generateURL():
    """Generate a random URL safe string"""
    u = uuid.uuid4()
    return u.hex