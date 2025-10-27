"""Reusable validation functions"""

import re
from typing import Optional


class Validators:
    """Common validation methods"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone format"""
        if not phone:
            return False
        cleaned = re.sub(r"[-.\s()]", "", phone)
        return bool(re.match(r"^\+?\d{10,15}$", cleaned))

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        if not url:
            return False
        pattern = r'^https?://[^\s<>"{}|\\^`\[\]]+$'
        return bool(re.match(pattern, url))

    @staticmethod
    def validate_length(
        text: str, min_length: int = 0, max_length: Optional[int] = None
    ) -> bool:
        """Validate text length"""
        if not text:
            return min_length == 0

        length = len(text)
        if length < min_length:
            return False
        if max_length and length > max_length:
            return False
        return True

    @staticmethod
    def validate_required_fields(
        data: dict, required_fields: list
    ) -> tuple[bool, list]:
        """Validate required fields are present"""
        missing = [field for field in required_fields if not data.get(field)]
        return len(missing) == 0, missing

    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        """Validate date format (YYYY-MM or YYYY)"""
        if not date_str:
            return False
        return bool(re.match(r"^\d{4}(-\d{2})?$", date_str))

    @staticmethod
    def validate_no_special_chars(text: str) -> bool:
        """Check text doesn't contain problematic special characters"""
        if not text:
            return True
        problematic = r"[★☆♥♦●○◆◇■□▪▫<>]"
        return not bool(re.search(problematic, text))

    @staticmethod
    def validate_alphanumeric(text: str, allow_spaces: bool = True) -> bool:
        """Validate text is alphanumeric"""
        if not text:
            return False
        pattern = r"^[a-zA-Z0-9\s]+$" if allow_spaces else r"^[a-zA-Z0-9]+$"
        return bool(re.match(pattern, text))
