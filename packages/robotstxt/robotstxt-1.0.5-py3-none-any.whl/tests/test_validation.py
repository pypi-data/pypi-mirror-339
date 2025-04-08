import pytest
from robotstxt.validation import RobotsValidator, ValidationSeverity, ValidationMessage

def test_file_size_validation():
    validator = RobotsValidator()
    # Create a valid base robots.txt
    base_content = """User-agent: *
Disallow: /private
Allow: /public
Sitemap: https://example.com/sitemap.xml

# The following comment is artificially long to test file size limits
#"""
    # Add a long comment that pushes us over 500KB
    padding = "#" + ("x" * 512000)
    large_content = base_content + padding
    
    errors, warnings = validator.validate(large_content)
    
    assert len(errors) == 1
    assert errors[0].severity == ValidationSeverity.ERROR
    assert errors[0].message == "File size exceeds 500KB limit"

def test_bom_validation():
    validator = RobotsValidator()
    content_with_bom = '\ufeffUser-agent: *'
    errors, warnings = validator.validate(content_with_bom)
    
    assert len(errors) == 1
    assert errors[0].severity == ValidationSeverity.ERROR
    assert errors[0].message == "File contains UTF-8 BOM"

def test_invalid_directive_format():
    validator = RobotsValidator()
    content = "User-agent * \nDisallow"  # Missing colons
    errors, warnings = validator.validate(content)
    
    assert len(errors) == 2
    assert errors[0].severity == ValidationSeverity.ERROR
    assert errors[0].message == "Invalid directive format - missing colon"

def test_empty_user_agent():
    validator = RobotsValidator()
    content = "User-agent:\nDisallow: /"
    errors, warnings = validator.validate(content)
    
    assert len(errors) == 2
    assert errors[0].severity == ValidationSeverity.ERROR
    assert errors[0].message == "Empty user-agent value"
    assert errors[1].severity == ValidationSeverity.ERROR
    assert errors[1].message == "disallow directive without preceding user-agent"

def test_invalid_user_agent_characters():
    validator = RobotsValidator()
    content = "User-agent: bot@name\nDisallow: /"
    errors, warnings = validator.validate(content)
    
    assert len(errors) == 2
    assert errors[0].severity == ValidationSeverity.ERROR
    assert errors[0].message == "Invalid user-agent format - contains invalid characters"
    assert errors[1].severity == ValidationSeverity.ERROR
    assert errors[1].message == "disallow directive without preceding user-agent"

def test_rule_without_user_agent():
    validator = RobotsValidator()
    content = "Disallow: /private"
    errors, warnings = validator.validate(content)
    
    assert len(errors) == 1
    assert errors[0].message == "disallow directive without preceding user-agent"

def test_warning_for_missing_leading_slash():
    validator = RobotsValidator()
    content = "User-agent: bot\nDisallow: private"
    errors, warnings = validator.validate(content)
    
    assert len(warnings) == 1
    assert warnings[0].severity == ValidationSeverity.WARNING
    assert warnings[0].message == "disallow rule should start with '/' or '*'"

def test_invalid_sitemap_url():
    validator = RobotsValidator()
    content = "Sitemap: not-a-url"
    errors, warnings = validator.validate(content)
    
    assert len(errors) == 1
    assert errors[0].message == "Invalid sitemap URL"
    assert errors[0].details == "not-a-url"

def test_duplicate_rules():
    validator = RobotsValidator()
    content = """
    User-agent: bot
    Disallow: /private
    Disallow: /private
    """
    errors, warnings = validator.validate(content)
    
    assert len(warnings) == 1
    assert warnings[0].severity == ValidationSeverity.WARNING
    assert warnings[0].message == "Duplicate disallow rule"

def test_valid_robots_txt():
    validator = RobotsValidator()
    content = """
    User-agent: *
    Disallow: /private
    Allow: /public
    Sitemap: https://example.com/sitemap.xml
    """
    errors, warnings = validator.validate(content)
    
    assert len(errors) == 0
    assert len(warnings) == 0

def test_valid_wildcard_patterns():
    validator = RobotsValidator()
    content = """
    User-agent: *
    Disallow: *
    Disallow: /*.php
    Disallow: /private/*.html
    """
    errors, warnings = validator.validate(content)
    
    assert len(errors) == 0
    assert len(warnings) == 0

def test_invalid_regex_patterns():
    validator = RobotsValidator()
    content = """
    User-agent: *
    Disallow: /.*
    Disallow: /[a-z]+
    Disallow: /(private|secret)
    """
    errors, warnings = validator.validate(content)
    
    assert len(errors) == 0
    assert len(warnings) == 3
    assert all(warning.severity == ValidationSeverity.WARNING for warning in warnings)
    assert all("probable regex pattern" in warning.message for warning in warnings)

def test_mixed_patterns():
    validator = RobotsValidator()
    content = """
    User-agent: *
    Disallow: /private/*.html
    Disallow: /.*.php
    Disallow: /public/*.txt
    """
    errors, warnings = validator.validate(content)
    
    assert len(errors) == 0
    assert len(warnings) == 1  # Only the /.*.php pattern should trigger a warning
    assert warnings[0].severity == ValidationSeverity.WARNING
    assert "probable regex pattern" in warnings[0].message 