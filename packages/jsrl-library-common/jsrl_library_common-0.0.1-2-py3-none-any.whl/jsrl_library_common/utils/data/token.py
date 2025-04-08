import os
import jwt

def create_token(payload, secret):
    """Create token to send sensitive information
    
    Args:
        - payload: the information to safe
        - secret: the encrypt password
        
    Returns:
        - string: token
        
    """
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token, secret):
    """Extract the information stored into the token
    
    Args:
        - token: the token
        - secret: the password which information was encrypt
        
    Returns:
        - dict: the payload
    
    """
    return jwt.decode(token, secret, algorithms=["HS256"])
