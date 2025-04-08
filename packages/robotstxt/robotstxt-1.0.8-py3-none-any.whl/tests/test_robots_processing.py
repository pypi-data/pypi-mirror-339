import pytest
from robotstxt.robots_processing import select_group, get_url_path, is_valid_url

# Test data fixtures
@pytest.fixture
def basic_groups():
    """Basic robots.txt with default group and specific user agents"""
    return {
        '*',  # default group
        'googlebot',
        'bingbot',
        'slurp'
    }

@pytest.fixture
def googlebot_groups():
    """Complex robots.txt with Googlebot variants"""
    return {
        'googlebot',
        'googlebot-news',
        'googlebot-image',
        'googlebot-video',
        '*'
    }

@pytest.fixture
def adsbot_groups():
    """Robots.txt with AdsBot tokens"""
    return {
        'adsbot-google',
        'adsbot-google-mobile',
        'mediapartners-google',
        'apis-google',
        '*'
    }

@pytest.fixture
def mixed_groups():
    """Robots.txt with mixed tokens"""
    return {
        'googlebot',
        'googlebot-news',
        'adsbot-google',
        'bingbot',
        '*'
    }

def test_basic_group_selection(basic_groups):
    """Test basic group selection with standard user agents"""
    # Test exact matches
    assert select_group(basic_groups, 'googlebot') == 'googlebot'
    assert select_group(basic_groups, 'bingbot') == 'bingbot'
    assert select_group(basic_groups, 'slurp') == 'slurp'
    
    # Test fallback to default group
    assert select_group(basic_groups, 'unknown-bot') == '*'
    
    # Test case insensitivity
    assert select_group(basic_groups, 'GOOGLEBOT') == 'googlebot'
    assert select_group(basic_groups, 'BingBot') == 'bingbot'

def test_googlebot_special_cases(googlebot_groups, basic_groups):
    """Test Googlebot special cases and fallback behavior"""
    # Test exact matches for Googlebot variants
    assert select_group(googlebot_groups, 'googlebot-news') == 'googlebot-news'
    assert select_group(googlebot_groups, 'googlebot-image') == 'googlebot-image'
    assert select_group(googlebot_groups, 'googlebot-video') == 'googlebot-video'
    
    # Test fallback to googlebot group when specific variant not found
    assert select_group(basic_groups, 'googlebot-news') == 'googlebot'
    assert select_group(basic_groups, 'googlebot-image') == 'googlebot'
    assert select_group(basic_groups, 'googlebot-video') == 'googlebot'
    
    # Test case insensitivity
    assert select_group(googlebot_groups, 'GOOGLEBOT-NEWS') == 'googlebot-news'
    assert select_group(googlebot_groups, 'Googlebot-Image') == 'googlebot-image'

def test_adsbot_special_cases(adsbot_groups, basic_groups):
    """Test AdsBot special cases that ignore default group"""
    # Test exact matches
    assert select_group(adsbot_groups, 'adsbot-google') == 'adsbot-google'
    assert select_group(adsbot_groups, 'adsbot-google-mobile') == 'adsbot-google-mobile'
    assert select_group(adsbot_groups, 'mediapartners-google') == 'mediapartners-google'
    assert select_group(adsbot_groups, 'apis-google') == 'apis-google'
    
    # Test that AdsBot tokens don't fall back to default group
    assert select_group(basic_groups, 'adsbot-google') is None
    assert select_group(basic_groups, 'adsbot-google-mobile') is None
    
    # Test case insensitivity
    assert select_group(adsbot_groups, 'ADSBOT-GOOGLE') == 'adsbot-google'
    assert select_group(adsbot_groups, 'Mediapartners-Google') == 'mediapartners-google'

def test_google_safety_special_case(basic_groups, googlebot_groups, adsbot_groups, mixed_groups):
    """Test Google-Safety special case that always returns None"""
    # Test with various group configurations
    assert select_group(basic_groups, 'google-safety') is None
    assert select_group(googlebot_groups, 'google-safety') is None
    assert select_group(adsbot_groups, 'google-safety') is None
    assert select_group(mixed_groups, 'google-safety') is None
    
    # Test case insensitivity
    assert select_group(basic_groups, 'GOOGLE-SAFETY') is None

def test_mixed_scenarios(mixed_groups):
    """Test mixed scenarios with various combinations of tokens and groups"""
    # Test Googlebot variants in mixed groups
    assert select_group(mixed_groups, 'googlebot-news') == 'googlebot-news'
    assert select_group(mixed_groups, 'googlebot') == 'googlebot'
    
    # Test AdsBot in mixed groups
    assert select_group(mixed_groups, 'adsbot-google') == 'adsbot-google'
    
    # Test standard bot in mixed groups
    assert select_group(mixed_groups, 'bingbot') == 'bingbot'
    
    # Test unknown bot falls back to default
    assert select_group(mixed_groups, 'unknown-bot') == '*'

@pytest.mark.parametrize("url,expected", [
    ('https://example.com/', '/'),  # Note the trailing slash
    ('http://example.com/path/to/page.html', '/path/to/page.html'),
    ('https://example.com/search?q=test', '/search?q=test'),
    ('https://example.com/path?param1=value&param2=value2', '/path?param1=value&param2=value2'),
    ('not_a_url', None),  # Invalid URL
    ('', None),  # Empty string
    (None, None),  # None input
])
def test_get_url_path(url, expected):
    """Test URL path extraction for various URL formats"""
    assert get_url_path(url) == expected

@pytest.mark.parametrize("url,expected", [
    ('https://example.com/', True),  # Note the trailing slash
    ('http://example.com/', True),    # Note the trailing slash
    ('https://sub.example.com/path', True),
    ('https://example.com/path?query=value', True),
    ('not_a_url', False),
    ('ftp://example.com', False),  # Wrong scheme
    ('http://', False),  # Missing domain
    ('', False),  # Empty string
    (None, False),  # None input
    ('https://.com', False),  # Invalid domain
    ('http://example', False),  # Incomplete domain
    ('http://.example.com', False),  # Invalid domain format
    ('http://example.com.', False),  # Invalid domain format
    ('http://localhost:999999', False),  # Invalid port
])
def test_is_valid_url(url, expected):
    """Test URL validation for various URL formats"""
    assert is_valid_url(url) == expected
