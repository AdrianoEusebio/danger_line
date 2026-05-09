import re
from typing import List, Tuple

class StaticShield:
    """Static security layer using Regex patterns to identify and scrub sensitive data."""
    
    # Patterns for common sensitive data
    PATTERNS: List[Tuple[str, str, str]] = [
        # (Name, Regex Pattern, Replacement Placeholder)
        ("OpenAI Key", r"sk-[a-zA-Z0-9]{48}", "<HIDDEN_OPENAI_KEY>"),
        ("AWS Key", r"AKIA[0-9A-Z]{16}", "<HIDDEN_AWS_KEY>"),
        ("Google API Key", r"AIza[0-9A-Za-z\\-_]{35}", "<HIDDEN_GOOGLE_KEY>"),
        ("Generic API Key", r"(?:api_key|apikey|secret|password|token)[\"']?\s*[:=]\s*[\"']?([a-zA-Z0-9\-_]{16,})[\"']?", "<HIDDEN_SECRET>"),
        ("Database URL", r"(?:mongodb(?:\+srv)?|postgres(?:ql)?|mysql|oracle|jdbc:[a-z]+)://[^\"\s'\n]+", "<HIDDEN_DB_URL>"),
        ("Email", r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "<HIDDEN_EMAIL>"),
        ("IPv4", r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "<HIDDEN_IP>"),
    ]

    @classmethod
    def scrub(cls, text: str) -> str:
        """Applies all regex patterns to the text and replaces matches with placeholders."""
        sanitized_text = text
        for name, pattern, replacement in cls.PATTERNS:
            try:
                # If the pattern has a capture group, we only want to replace that part
                if "(" in pattern:
                    def replace_func(match):
                        if match.groups():
                            # Replace the first capturing group's content
                            full = match.group(0)
                            secret = match.group(1)
                            return full.replace(secret, replacement)
                        return replacement
                    
                    sanitized_text = re.sub(pattern, replace_func, sanitized_text, flags=re.IGNORECASE)
                else:
                    # Simple replacement for patterns without groups
                    sanitized_text = re.sub(pattern, replacement, sanitized_text, flags=re.IGNORECASE)
            except Exception as e:
                # Fallback to simple sub if something goes wrong with complex logic
                sanitized_text = re.sub(pattern, replacement, sanitized_text, flags=re.IGNORECASE)
        
        return sanitized_text

if __name__ == "__main__":
    # Test Shield
    test_text = """
    My OpenAI key is sk-123456789012345678901234567890123456789012345678 and 
    my DB is postgres://admin:password123@localhost:5432/mydb.
    Contact me at secret@example.com or 192.168.1.1.
    API_KEY = "my-super-secret-token-123"
    """
    print("Original Text:\n", test_text)
    print("\nSanitized Text:\n", StaticShield.scrub(test_text))
