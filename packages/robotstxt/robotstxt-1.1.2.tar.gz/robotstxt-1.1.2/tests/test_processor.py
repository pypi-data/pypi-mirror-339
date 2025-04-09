import pytest
from robotstxt.processor import RobotsFile, Sitemap

@pytest.fixture
def test_robots():
    return '''
# some more comments
some uncommented comments

user-agent: bingbot
user-agent: googlebot
Disallow: /case_insensitive_token
Disallow: /*url_query_test
Disallow: /multiple_token_block
Allow:    /same_length_allow_beats_disallow
Disallow: /same_length_allow_beats_disallow
Allow:    /longer_allow_beats_disallow*
Disallow: /longer_allow_beats_disallow
Disallow: /inline_comment # inline comment
Disallow: missing_leading_slash
Disallow: *leading_wildcard
Disallow: /multiple*wildcards*test
Disallow: /trailing_space_in_directive 
Disallow: /*unencoded|
Disallow: /*encoded%40 # @ symbol
Disallow: /positive_fallback_test
Disallow: /default_trailing_wildcard
Disallow: /..something # dot character handling
Disallow: / b
Disallow: *radius=

Disallow: /block_break

user-agent: googlebot
Disallow: /split_block_test

user-agent: googlebot-images
Disallow: /negative_fallback_test

user-agent: *
Disallow: /default_token

user-agent: blank
Disallow:

Sitemap: https://www.domain.com/sitemap.xml
sitemap: https://www.domain.com/lower_case.xml
SITEMAP: https://www.domain.com/upper_case.xml
sitemap: www.domain.com/missing_protocol.xml
sitemap: missing_domain.xml
sitemap: https://www.domain.com/has_comment.xml #comment
  Sitemap: https://www.domain.com/leading_whitespace.xml
Sitemap: https://www.domain.com/trailing_whitespace.xml   
Sitemap:    https://www.domain.com/rule_leading_whitespace.xml   
'''

@pytest.fixture
def test_robots_token_hierarchy():
    return '''
# Test robots.txt with explicit token hierarchy
user-agent: *
disallow: /default-block

user-agent: Googlebot
disallow: /googlebot-block

user-agent: Googlebot-Images
disallow: /googlebot-images-block

user-agent: Other
disallow: /other-block

user-agent: google
Disallow: /

'''

@pytest.fixture
def robots_file(test_robots):
    return RobotsFile(test_robots)

@pytest.fixture
def robots_file_token_hierarchy(test_robots_token_hierarchy):
    return RobotsFile(test_robots_token_hierarchy)

@pytest.mark.parametrize("url,user_agent,expected_disallowed,expected_token,expected_directive", [
    ('http://test.chris24.co.uk/default-block', 'Default', True, '*', 'Disallow: /default-block'),  # Should match default block
    ('http://test.chris24.co.uk/googlebot-block', 'Googlebot-Video', True, 'googlebot', 'Disallow: /googlebot-block'),  # Should match parent token
    ('http://test.chris24.co.uk/googlebot-images-block', 'Googlebot-Images', True, 'googlebot-images', 'Disallow: /googlebot-images-block'),  # Should match exact token
    ('http://test.chris24.co.uk/other-block', 'Other', True, 'other', 'Disallow: /other-block'),  # Should match exact token
    ('http://test.chris24.co.uk/non-existent', 'Googlebot', False, None, None),  # No match
    ('http://test.chris24.co.uk/google-safety', 'google-safety', False, None, None),  # No match
    ('http://test.chris24.co.uk/adsbot-google', 'adsbot-google', False, None, None),  # No match
])
def test_url_matching_token(robots_file_token_hierarchy, url, user_agent, expected_disallowed, expected_token, expected_directive):
    """Test URL matching token behavior for various scenarios
    
    Tests the token matching hierarchy:
    - Default block (*) matches when no specific token matches
    - Parent tokens (e.g., Googlebot) match for child tokens (e.g., Googlebot-Video)
    - Exact tokens match when available
    """
    result = robots_file_token_hierarchy.test_url(url, user_agent)
    assert result['disallowed'] == expected_disallowed
    assert result['matching_token'] == expected_token
    assert result['directive'] == expected_directive
    if expected_directive:
        assert result['path_pattern'] == expected_directive.split(': ')[1]
    else:
        assert result['path_pattern'] is None

@pytest.mark.parametrize("url,user_agent,expected", [
    ('http://test.chris24.co.uk/ b', 'googlebot', True),
    ('http://test.chris24.co.uk/', 'googlebot', False),
    ('http://test.chris24.co.uk/trailing_space_in_directive', 'googlebot', True),
    ('http://test.chris24.co.uk/case_insensitive_token', 'GOOGLEBOT', True),
    ('http://test.chris24.co.uk/split_block_test', 'googlebot', True),
    ('http://test.chris24.co.uk/multiple_token_block', 'bingbot', True),
    ('http://test.chris24.co.uk/default_token', 'some_token', True),
    ('http://test.chris24.co.uk/inline_comment', 'googlebot', True),
    ('http://test.chris24.co.uk/?url_query_test=123', 'googlebot', True),
    ('http://test.chris24.co.uk/missing_leading_slash', 'googlebot', False),
    ('http://test.chris24.co.uk/negative_fallback_test', 'googlebot-images', True),
    ('http://test.chris24.co.uk/same_length_allow_beats_disallow', 'googlebot', False),
    ('http://test.chris24.co.uk/longer_allow_beats_disallow', 'googlebot', False),
    ('http://test.chris24.co.uk/block_break', 'googlebot', True),
    ('http://test.chris24.co.uk/positive_fallback_test', 'googlebot-news', True),
    ('http://test.chris24.co.uk/leading_wildcard', 'googlebot', True),
    ('http://test.chris24.co.uk/multiple_wildcards_test_', 'googlebot', True),
    ('http://test.chris24.co.uk/default_trailing_wildcard_test', 'googlebot', True),
    ('http://test.chris24.co.uk/encoded%40', 'googlebot', True),
    ('http://test.chris24.co.uk/encoded@', 'googlebot', True),
    ('http://test.chris24.co.uk/unencoded%7C', 'googlebot', True),
    ('http://test.chris24.co.uk/blank_disallow', 'blank', False),
    ('http://test.chris24.co.uk/..something', 'googlebot', True),
    ('http://test.chris24.co.uk/.ssomething', 'googlebot', False),
    ('http://test.chris24.co.uk/for-sale/property/barking/?radius=2.0', 'googlebot', True),
])
def test_url_disallow(robots_file, url, user_agent, expected):
    """Test URL disallow rules for various URLs and user agents"""
    assert robots_file.test_url(url, user_agent)['disallowed'] == expected

@pytest.mark.parametrize("url,expected_valid,expected_url", [
    ('https://www.example.com/sitemap.xml', True, 'https://www.example.com/sitemap.xml'),
    ('ttps://www.example.com/sitemap.xml', False, 'ttps://www.example.com/sitemap.xml'),
])
def test_sitemap(url, expected_valid, expected_url):
    """Test sitemap URL validation"""
    sitemap = Sitemap(url)
    assert sitemap.valid_url == expected_valid
    assert sitemap.url == expected_url

@pytest.mark.parametrize("index,expected_url,expected_valid", [
    (0, 'https://www.domain.com/sitemap.xml', True),
    (1, 'https://www.domain.com/lower_case.xml', True),
    (2, 'https://www.domain.com/upper_case.xml', True),
    (3, 'www.domain.com/missing_protocol.xml', False),
    (4, 'missing_domain.xml', False),
    (5, 'https://www.domain.com/has_comment.xml', True),
    (6, 'https://www.domain.com/leading_whitespace.xml', True),
    (7, 'https://www.domain.com/trailing_whitespace.xml', True),
    (8, 'https://www.domain.com/rule_leading_whitespace.xml', True),
])
def test_sitemap_in_robotstxt(robots_file, index, expected_url, expected_valid):
    """Test sitemap extraction and validation from robots.txt"""
    sitemap = robots_file.sitemaps[index]
    assert sitemap.url == expected_url
    assert sitemap.valid_url == expected_valid
