import random
import string
from config import current_config

def generate_shortcode(length=None):
    """
    Generate a random short code for URL shortening.
    
    Args:
        length (int, optional): Length of the short code. Defaults to config value.
    
    Returns:
        str: A random string of specified length.
    """
    if length is None:
        length = current_config.SHORTCODE_LENGTH
    
    # Use all letters (uppercase and lowercase) and digits for the shortcode
    # This is effectively base62 encoding (26 lowercase + 26 uppercase + 10 digits)
    characters = string.ascii_letters + string.digits
    
    # Generate a random string of the specified length
    shortcode = ''.join(random.choice(characters) for _ in range(length))
    
    return shortcode 