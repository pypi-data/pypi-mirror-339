import pytest
from robotstxt.processor import RobotsFile, compare_robots_files

class TestRobotsComparison:



    def test_identical_files(self):
        content = """
User-agent: *
Disallow: /private/
Allow: /public/
        """.strip()
        
        robots1 = RobotsFile(content)
        robots2 = RobotsFile(content)
        
        diff = compare_robots_files(robots1, robots2)
        
        assert diff["materially_different"] == False
        assert diff["token_diffs"] == {}
        assert diff["sitemap_changes"] == {"added": [], "removed": []}

    def test_separate_and_shared_groups(self):
        content1 = """
User-agent: googlebot
User-agent: bingbot
Disallow: /something

        """.strip()
        
        content2 = """
User-agent: googlebot
Disallow: /something

# Separated the group for bingbot
User-agent: bingbot
Disallow: /something

        """.strip()
        
        robots1 = RobotsFile(content1)
        robots2 = RobotsFile(content2)
        
        diff = compare_robots_files(robots1, robots2)
        
        assert diff["materially_different"] == False


    def test_different_rules(self):
        content1 = """
User-agent: googlebot
Disallow: /old/
Allow: /public/
        """.strip()
        
        content2 = """
User-agent: googlebot
Disallow: /new/
Allow: /public/
        """.strip()
        
        robots1 = RobotsFile(content1)
        robots2 = RobotsFile(content2)
        
        diff = compare_robots_files(robots1, robots2)
        
        assert diff["materially_different"] == True
        assert "googlebot" in diff["token_diffs"]
        assert "Disallow: /new/" in diff["token_diffs"]["googlebot"]["added"]
        assert "Disallow: /old/" in diff["token_diffs"]["googlebot"]["removed"]

    def test_different_tokens(self):
        content1 = """
User-agent: googlebot
Disallow: /private/
        """.strip()
        
        content2 = """
User-agent: bingbot
Disallow: /private/
        """.strip()
        
        robots1 = RobotsFile(content1)
        robots2 = RobotsFile(content2)
        
        diff = compare_robots_files(robots1, robots2)
        
        assert diff["materially_different"] == True
        assert "googlebot" in diff["token_diffs"]
        assert "bingbot" in diff["token_diffs"]

    def test_different_sitemaps(self):
        content1 = """
User-agent: *
Disallow: /private/
Sitemap: https://example.com/old-sitemap.xml
        """.strip()
        
        content2 = """
User-agent: *
Disallow: /private/
Sitemap: https://example.com/new-sitemap.xml
        """.strip()
        
        robots1 = RobotsFile(content1)
        robots2 = RobotsFile(content2)
        
        diff = compare_robots_files(robots1, robots2)
        
        assert diff["materially_different"] == True
        assert "https://example.com/new-sitemap.xml" in diff["sitemap_changes"]["added"]
        assert "https://example.com/old-sitemap.xml" in diff["sitemap_changes"]["removed"]

    def test_compare_with_method(self):
        """Test the convenience method on RobotsFile class"""
        content1 = """
User-agent: *
Disallow: /old/
        """.strip()
        
        content2 = """
User-agent: *
Disallow: /new/
        """.strip()
        
        robots1 = RobotsFile(content1)
        robots2 = RobotsFile(content2)
        
        # Test both ways to ensure symmetrical comparison
        diff1 = robots1.compare_with(robots2)
        robots2._is_newer_version = True  # Mark robots2 as the newer version
        diff2 = robots2.compare_with(robots1)
        
        assert diff1["materially_different"] == True
        assert diff2["materially_different"] == True
        assert "Disallow: /new/" in diff1["token_diffs"]["*"]["added"]
        assert "Disallow: /old/" in diff2["token_diffs"]["*"]["removed"]

    def test_whitespace_insensitive(self):
        content1 = """
User-agent: *
Disallow: /private/
Allow:    /public/
        """.strip()
        
        content2 = """
User-agent: *
Disallow:/private/
Allow: /public/
        """.strip()
        
        robots1 = RobotsFile(content1)
        robots2 = RobotsFile(content2)
        
        diff = compare_robots_files(robots1, robots2)
        
        assert diff["materially_different"] == False
        assert diff["token_diffs"] == {}

    def test_case_insensitive_tokens(self):
        content1 = """
User-agent: GoogleBot
Disallow: /private/
        """.strip()
        
        content2 = """
User-agent: googlebot
Disallow: /private/
        """.strip()
        
        robots1 = RobotsFile(content1)
        robots2 = RobotsFile(content2)
        
        diff = compare_robots_files(robots1, robots2)
        
        assert diff["materially_different"] == False
        assert diff["token_diffs"] == {} 