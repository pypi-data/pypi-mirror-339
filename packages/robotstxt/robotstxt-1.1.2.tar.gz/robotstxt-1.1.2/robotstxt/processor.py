import re
import operator
import json
import hashlib
import datetime
from urllib.parse import unquote
from .validation import RobotsValidator, ValidationMessage
from .robots_processing import is_valid_url, select_group, get_url_path
from .directive_match import pattern_match

def hash_generator(content):
    """Generate a hash of the content.
    
    Args:
        content: Either a string or a list that can be converted to a string.
                If it's a list, it will be joined with newlines.
    """
    if isinstance(content, list):
        content = '\n'.join(str(item) for item in content)
    return hashlib.sha256(str(content).encode('utf-8')).hexdigest()

class RobotsFile:
    def __init__(self, contents):
        self.contents = contents
        self.sitemaps = []
        self.byte_size = len(self.contents.encode('utf-8'))
        # self.size_exceeded = True if self.byte_size > 512000 else False
        self.hash_raw = hash_generator(self.contents)
        self.generated_datetime = datetime.datetime.now(datetime.UTC)

        # Process the file for rules
        self.rule_blocks = self._process_rules()

        self.json = json.dumps(self.rule_blocks, sort_keys=True)
        self.hash_material = hash_generator(json.dumps(self.rule_blocks, sort_keys=True))

        # Generate a hash of the sitemaps
        sitemap_list = []
        for sitemap in self.sitemaps:
            sitemap_list.append(sitemap.url)
        sitemap_list.sort()
        self.hash_sitemaps = hash_generator(sitemap_list)
        
        # Validate the file
        self.validator = RobotsValidator()
        self.errors, self.warnings = self.validator.validate(self.contents)

    def _process_rules(self):
        """
        Process the robots.txt content to extract rules and sitemaps.
        Returns a dictionary of groups consisting of a token and rules.
        """
        lines = self.contents.splitlines()
        user_agent_tokens = []
        user_agent_discovery = False
        user_agent_blocks = {}

        for line in lines:
            # Check for sitemap entries
            sitemap = re.search(r'sitemap:\s*(.*?)($|\s)', line, re.IGNORECASE)
            if sitemap:
                self.sitemaps.append(Sitemap(sitemap[1]))
                continue

            # Process user-agent and rule entries
            user_agent = re.search(r'user-agent:\s*(.*?)($|\s)', line, re.IGNORECASE)
            if user_agent:
                if user_agent_discovery:
                    user_agent_tokens.append(user_agent[1].lower())
                else:
                    user_agent_tokens = [user_agent[1].lower()]
                    user_agent_discovery = True
            else:
                user_agent_discovery = False

                # Process disallow rules
                disallow_rule = re.search(r'disallow:\s*(.*?)(?:$|\s*#)', line, re.IGNORECASE)
                if disallow_rule:
                    for token in user_agent_tokens:
                        rule = ['Disallow', -len(disallow_rule[1]), disallow_rule[1].strip(), disallow_rule[1].strip()]
                        if token in user_agent_blocks:
                            user_agent_blocks[token].append(rule)
                        else:
                            user_agent_blocks[token] = [rule]
                    continue

                # Process allow rules
                allow_rule = re.search(r'allow:\s*(.*?)(?:$|\s)', line, re.IGNORECASE)
                if allow_rule:
                    for token in user_agent_tokens:
                        rule = ['Allow', -len(allow_rule[1]), allow_rule[1], allow_rule[1]]
                        if token in user_agent_blocks:
                            user_agent_blocks[token].append(rule)
                        else:
                            user_agent_blocks[token] = [rule]

        # Sort rules by length (descending) and type (Disallow before Allow)
        for user_agent_block in user_agent_blocks:
            user_agent_blocks[user_agent_block] = sorted(
                user_agent_blocks[user_agent_block],
                key=operator.itemgetter(1, 0)
            )

        return user_agent_blocks

    def test_url(self, url, token):
        """Test if a URL is allowed for a given user agent token.
        
        Args:
            url: The URL to test
            token: The user agent token to test against
            
        Returns:
            dict: A dictionary containing:
                - disallowed: bool indicating if the URL is disallowed
                - path_pattern: str of the matching rule pattern
                - matching_token: str of the matching agent token from the rule block
                - directive: str of the full matching rule (e.g., 'Disallow: /path')
        """
        url_path_to_test = get_url_path(unquote(url))
        selected_block = select_group(self.rule_blocks, token.lower())

        if selected_block:
            for rule in self.rule_blocks[selected_block]:
                if rule[3]:
                    if pattern_match(unquote(rule[3]), url_path_to_test):
                        if rule[0] == 'Disallow':
                            return {
                                'disallowed': True,
                                'path_pattern': rule[2],
                                'matching_token': selected_block,
                                'directive': f'Disallow: {rule[2]}'
                            }
                        else:
                            return {
                                'disallowed': False,
                                'path_pattern': rule[2],
                                'matching_token': selected_block,
                                'directive': f'Allow: {rule[2]}'
                            }
            else:
                return {
                    'disallowed': False,
                    'path_pattern': None,
                    'matching_token': None,
                    'directive': None
                }
        else:
            return {
                'disallowed': False,
                'path_pattern': None,
                'matching_token': None,
                'directive': None
            }

    def get_validation_errors(self) -> list[ValidationMessage]:
        """Get all validation errors."""
        return self.errors

    def get_validation_warnings(self) -> list[ValidationMessage]:
        """Get all validation warnings."""
        return self.warnings

    def has_errors(self) -> bool:
        """Check if there are any validation errors."""
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        """Check if there are any validation warnings."""
        return len(self.warnings) > 0

    def compare_with(self, other: 'RobotsFile') -> dict:
        """Compare this robots.txt file with another one.
        
        Args:
            other: Another RobotsFile instance to compare against
            
        Returns:
            dict: A structured diff of the differences between the two files
        """
        # When this method is called, we want to show what changed from 'self' to 'other'
        # So 'self' is the old version and 'other' is the new version
        result = compare_robots_files(self, other)
        
        # If we're comparing in the opposite direction (new to old),
        # we need to swap the added and removed rules
        if hasattr(self, '_is_newer_version') and self._is_newer_version:
            for token in result['token_diffs']:
                result['token_diffs'][token]['added'], result['token_diffs'][token]['removed'] = \
                    result['token_diffs'][token]['removed'], result['token_diffs'][token]['added']
            result['sitemap_changes']['added'], result['sitemap_changes']['removed'] = \
                result['sitemap_changes']['removed'], result['sitemap_changes']['added']
        
        return result

class Sitemap:
    def __init__(self, url):
        self.url = url
        self.valid_url = True if is_valid_url(self.url) else False



def compare_robots_files(robots1: RobotsFile, robots2: RobotsFile) -> dict:
    """Compare two robots.txt files and generate a structured diff of their rules.
    
    Args:
        robots1: First RobotsFile instance (considered the "old" version)
        robots2: Second RobotsFile instance (considered the "new" version)
        
    Returns:
        dict: A structured diff containing:
            - materially_different: bool indicating if the files have different rules
            - token_diffs: dict of differences per token
            - sitemap_changes: dict of sitemap differences
    """
    # Get all unique tokens from both files
    all_tokens = set(robots1.rule_blocks.keys()) | set(robots2.rule_blocks.keys())
    
    token_diffs = {}
    materially_different = False
    
    for token in all_tokens:
        rules1 = robots1.rule_blocks.get(token, [])
        rules2 = robots2.rule_blocks.get(token, [])
        
        # Compare rules for this token
        added_rules = []
        removed_rules = []
        
        # Convert rules to comparable format (directive and pattern)
        rules1_set = {(r[0], r[2]) for r in rules1}
        rules2_set = {(r[0], r[2]) for r in rules2}
        
        # Find differences - rules in robots2 that aren't in robots1 are added
        # rules in robots1 that aren't in robots2 are removed
        added_rules = [f"{directive}: {pattern}" for directive, pattern in rules2_set - rules1_set]
        removed_rules = [f"{directive}: {pattern}" for directive, pattern in rules1_set - rules2_set]
        
        if added_rules or removed_rules:
            materially_different = True
            token_diffs[token] = {
                "added": added_rules,
                "removed": removed_rules
            }
    
    # Compare sitemaps
    sitemap_changes = {
        "added": [s.url for s in robots2.sitemaps if s.url not in [s1.url for s1 in robots1.sitemaps]],
        "removed": [s.url for s in robots1.sitemaps if s.url not in [s2.url for s2 in robots2.sitemaps]]
    }
    
    if sitemap_changes["added"] or sitemap_changes["removed"]:
        materially_different = True
    
    return {
        "materially_different": materially_different,
        "token_diffs": token_diffs,
        "sitemap_changes": sitemap_changes
    }