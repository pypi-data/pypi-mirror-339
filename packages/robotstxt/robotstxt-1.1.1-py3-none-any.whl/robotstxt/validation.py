from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import re
from urllib.parse import urlparse

class ValidationSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"

@dataclass
class ValidationMessage:
    severity: ValidationSeverity
    message: str
    line_number: Optional[int] = None
    details: Optional[str] = None

    def __str__(self) -> str:
        # Format the line number part if it exists
        line_info = f" on line {self.line_number}" if self.line_number is not None else ""
        
        # Create the base message
        base_message = f"{self.severity.value.upper()}: {self.message}{line_info}"
        
        # Add details if they exist
        if self.details:
            base_message += f" - {self.details}"
        
        return base_message

class RobotsValidator:
    def __init__(self):
        self.errors: List[ValidationMessage] = []
        self.warnings: List[ValidationMessage] = []
        
    def validate(self, content: str) -> tuple[List[ValidationMessage], List[ValidationMessage]]:
        """Validate a robots.txt file content and return errors and warnings."""
        self.errors = []
        self.warnings = []
        
        # Check file size
        if len(content.encode('utf-8')) > 512000:
            self.errors.append(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                message="File size exceeds 500KB limit"
            ))
            
        # Check for BOM
        if content.startswith('\ufeff'):
            self.errors.append(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                message="File contains UTF-8 BOM"
            ))
            
        # Process each line
        lines = content.splitlines()
        current_user_agent = None
        user_agent_rules = {}
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
                
            # Check for invalid characters
            try:
                line.encode('utf-8')
            except UnicodeEncodeError:
                self.errors.append(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    message="Line contains non-UTF-8 characters",
                    line_number=i
                ))
                continue
                
            # Parse directive
            parts = line.split(':', 1)
            if len(parts) != 2:
                self.errors.append(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    message="Invalid directive format - missing colon",
                    line_number=i
                ))
                continue
                
            directive = parts[0].strip().lower()
            value = parts[1].strip()
            
            # Validate user-agent
            if directive == 'user-agent':
                if not value:
                    self.errors.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message="Empty user-agent value",
                        line_number=i
                    ))
                    current_user_agent = None
                    continue
                    
                if not re.match(r'^[a-zA-Z0-9_*-]+$', value):
                    self.errors.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message="Invalid user-agent format - contains invalid characters",
                        line_number=i
                    ))
                    current_user_agent = None
                    continue
                    
                current_user_agent = value
                if current_user_agent not in user_agent_rules:
                    user_agent_rules[current_user_agent] = []
                    
            # Validate allow/disallow rules
            elif directive in ('allow', 'disallow'):
                if not current_user_agent:
                    self.errors.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message=f"{directive} directive without preceding user-agent",
                        line_number=i
                    ))
                    continue
                    
                # Check for missing leading slash (unless it's a wildcard)
                if not value.startswith('/') and not value.startswith('*'):
                    self.warnings.append(ValidationMessage(
                        severity=ValidationSeverity.WARNING,
                        message="disallow rule should start with '/' or '*'",
                        line_number=i
                    ))
                    
                user_agent_rules[current_user_agent].append((directive, value))
                
            # Validate sitemap
            elif directive == 'sitemap':
                if not value:
                    self.errors.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message="Empty sitemap URL",
                        line_number=i
                    ))
                    continue
                    
                if not self._is_valid_url(value):
                    self.errors.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message="Invalid sitemap URL",
                        line_number=i,
                        details=value
                    ))
                    
            # Check for duplicate rules
            if current_user_agent and directive in ('allow', 'disallow'):
                rule_count = sum(1 for d, v in user_agent_rules[current_user_agent] 
                               if d == directive and v == value)
                if rule_count > 1:
                    self.warnings.append(ValidationMessage(
                        severity=ValidationSeverity.WARNING,
                        message=f"Duplicate {directive} rule",
                        line_number=i
                    ))
                    
        return self.errors, self.warnings
        
    def _is_valid_url(self, url: str) -> bool:
        """Validate a URL format."""
        try:
            result = urlparse(url)
            return bool(result.scheme and result.netloc)
        except:
            return False 