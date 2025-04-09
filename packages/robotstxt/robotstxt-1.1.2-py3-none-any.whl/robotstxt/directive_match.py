import urllib.parse

# Test if a URL path matches a pattern
def pattern_match(pattern, path, debug=False):

    """
    Match a robots.txt pattern against a path using dynamic programming approach.
    Similar to Google's C++ implementation.
    """
    path = urllib.parse.unquote(path)
    pattern = urllib.parse.unquote(pattern)
    
    path_len = len(path)
    # pos array holds all possible matching positions in the path
    # True means this position is a potential match point
    pos = [False] * (path_len + 1)
    pos[0] = True  # Start matching at position 0
    
    if debug:
        print(f"Matching pattern '{pattern}' against path '{path}'")
    
    i = 0
    while i < len(pattern):
        if debug:
            print(f"Processing pattern char '{pattern[i]}' at positions: {[j for j,p in enumerate(pos) if p]}")
            
        # Handle end-of-string marker
        if pattern[i] == '$' and i == len(pattern) - 1:
            # Only the last position should be marked
            return pos[path_len]
            
        # Handle wildcard
        elif pattern[i] == '*':
            # Skip consecutive wildcards
            while i + 1 < len(pattern) and pattern[i + 1] == '*':
                i += 1
                
            # For wildcard, extend all current positions to include all possible
            # future positions
            new_pos = pos.copy()
            for j in range(path_len + 1):
                if pos[j]:
                    for k in range(j, path_len + 1):
                        new_pos[k] = True
            pos = new_pos
            
        # Handle normal character
        else:
            new_pos = [False] * (path_len + 1)
            for j in range(path_len):
                if pos[j] and j < path_len and path[j] == pattern[i]:
                    new_pos[j + 1] = True
            pos = new_pos
            
        if not any(pos):  # No valid positions left
            return False
            
        i += 1
        
        if debug:
            print(f"After processing: {[j for j,p in enumerate(pos) if p]}")
    
    # Pattern matched if we have any valid final position
    return any(pos)
