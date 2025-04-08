import re
from urllib.parse import urlparse

def select_group(groups, token):
    """
    Select the appropriate group for a given token based on the fallback rules.
    
    Args:
        groups (set): Set of available group names
        token (str): The user agent token to match
        
    Returns:
        str: The matched group name or None if no match found
    """
    # Convert token to lowercase for case-insensitive matching
    token_lower = token.lower()
    
    # Special case: Google-Safety token always returns None (allowed)
    if token_lower == 'google-safety':
        return None
        
    # Special case: AdsBot tokens ignore default group
    if token_lower in ['adsbot-google', 'adsbot-google-mobile', 'mediapartners-google', 'apis-google']:
        if token_lower in groups:
            return token_lower
        return None
        
    # First try exact match
    if token_lower in groups:
        return token_lower
        
    # Googlebot special cases with fallback to 'googlebot' group
    if token_lower in ['googlebot-news', 'googlebot-image', 'googlebot-video']:
        if 'googlebot' in groups:
            return 'googlebot'
            
    # Finally try default group
    if '*' in groups:
        return '*'
        
    return None

def get_url_path(url):
    """
    Extract the path component from a URL using urllib.parse
    
    Args:
        url (str): The URL to parse
        
    Returns:
        str: The path component of the URL, or None if invalid/no path
    """
    if not url or not isinstance(url, str):
        return None
    try:
        parsed = urlparse(url)
        # Only return path if it's a valid URL with scheme and netloc
        if parsed.scheme in ('http', 'https') and parsed.netloc:
            # Ensure path starts with / if it exists
            path = parsed.path if parsed.path else '/'
            return path + (f'?{parsed.query}' if parsed.query else '')
        return None
    except (ValueError, AttributeError):
        return None

def is_valid_url(url):
    """
    Validate a URL using urllib.parse
    
    Args:
        url (str): The URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    try:
        result = urlparse(url)
        # Check for valid scheme
        if result.scheme not in ('http', 'https'):
            return False
            
        # Check netloc (domain)
        if not result.netloc:
            return False
            
        # Handle localhost specially
        if result.netloc == 'localhost':
            return True
            
        # For non-localhost, check domain format
        parts = result.netloc.split(':')
        domain = parts[0]
        
        # Domain must have at least one dot and not start/end with one
        if not domain or domain.startswith('.') or domain.endswith('.'):
            return False
            
        # Check if there's at least one dot in the domain
        if '.' not in domain:
            return False
            
        # If there's a port, it should be a valid number
        if len(parts) > 1:
            try:
                port = int(parts[1])
                if not (1 <= port <= 65535):
                    return False
            except ValueError:
                return False
                
        return True
    except (ValueError, AttributeError):
        return False

