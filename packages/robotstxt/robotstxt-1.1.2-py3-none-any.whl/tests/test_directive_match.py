import pytest
from robotstxt.processor import pattern_match

@pytest.mark.parametrize("pattern,path,expected", [
    # Root and lower levels match
    ('/', '/anything', True),
    ('/*', '/anything', True),
    
    # Root only match
    ('/$', '/', True),
    ('/$', '/anything', False),
    
    # Contains match
    ('/fish', '/fish', True),
    ('/fish', '/fish.html', True),
    ('/fish', '/fish/salmon.html', True),
    ('/fish', '/fishheads', True),
    ('/fish', '/fishheads/yummy.html', True),
    ('/fish', '/fish.php?id=anything', True),
    ('/fish', '/Fish.asp', False),
    ('/fish', '/catfish', False),
    ('/fish', '/?id=fish', False),
    ('/fish', '/desert/fish', False),
    
    # Trailing wildcard match
    ('/fish*', '/fish', True),
    ('/fish**', '/fish', True),
    ('/fish*', '/fish.html', True),
    ('/fish*', '/fish/salmon.html', True),
    ('/fish*', '/fishheads', True),
    ('/fish*', '/fishheads/yummy.html', True),
    ('/fish*', '/fish.php?id=anything', True),
    ('/fish*', '/Fish.asp', False),
    ('/fish*', '/catfish', False),
    ('/fish*', '/?id=fish', False),
    ('/fish*', '/desert/fish', False),
    
    # Undermatch match
    ('/fish/', '/fish/', True),
    ('/fish/', '/fish/?id=anything', True),
    ('/fish/', '/fish/salmon.htm', True),
    ('/fish/', '/fish', False),
    ('/fish/', '/fish.html', False),
    ('/fish/', '/animals/fish/', False),
    ('/fish/', '/Fish/Salmon.asp', False),
    
    # Leading wildcard and end of string match
    ('/*.php$', '/filename.php', True),
    ('/*.php$', '/folder/filename.php', True),
    ('/*.php$', '/filename.php?parameters', False),
    ('/*.php$', '/filename.php/', False),
    ('/*.php$', '/filename.php5', False),
    ('/*.php$', '/windows.PHP', False),
    
    # Wildcard middle of string match
    ('/*.php', '/fish.php', True),
    ('/*.php', '/fishheads/catfish.php?parameters', True),
    ('/*.php', '/Fish.PH', False),
    
    # Missing leading slash or wildcard match
    ('fish', '/fish', False),
    
    # End of string
    ('/fish$', '/fish', True),
    ('/fish$', '/fish123', False),
    
    # Dollar not end of string
    ('/ab$cd$', '/ab$cd', True),
    ('/ab$cd$', '/ab$cd$', False),
    ('/ab$cd', '/ab$cd', True),
    ('/ab$', '/ab$cd', False),
    
    # Leading wildcard match
    ('/*.php', '/index.php', True),
    ('/**.php', '/index.php', True),
    ('/***.php', '/index.php', True),
    ('/*.php', '/filename.php', True),
    ('/*.php', '/folder/filename.php', True),
    ('/*.php', '/folder/filename.php?parameters', True),
    ('/*.php', '/folder/any.php.file.html', True),
    ('/*.php', '/filename.php/', True),
    ('/*.php', '/', False),
    ('/*.php', '/windows.PHP', False),
    ('*.php', '/index.php', True),
    
    # Generous wildcard match
    ('/*aa-bb', '/aa-aa-bb', True),
    ('/*ab*cd*ab', '/ab-cd-ab', True),
    ('/*aa*bb', '/aa-bb-aa-cc', True),
    
    # Asterisk in path match
    ('/a*b', '/a*b', True),
    
    # Space in patterns
    ('/ b', '/ b', True),
    
    # Encoded patterns
    ('/%20a', '/ a', True),
    ('/ b', '/%20b', True),
    ('/?c', '/%3Fc', True),
    ('/%3Fd', '/?d', True),
    ('/?e', '/%3fe', True),
    ('/%3ff', '/?f', True),
    ('/%3Ff', '/?f', True),
    ('/%253Fg', '/?g', False),
    ('/%25253Fh', '/?h', False),
    ('/?i', '/%253Fi', False),
    ('/?j', '/%25253Fj', False),
    
    # Trailing wildcard and end of line
    ('/blog/*/page/*$', '/blog/en/page/4', True),
])
def test_pattern_match(pattern, path, expected):
    """Test pattern matching for various URL patterns and paths"""
    assert pattern_match(pattern, path) == expected

