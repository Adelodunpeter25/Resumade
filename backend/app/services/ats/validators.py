"""Validation and formatting checks"""

import re
from typing import Dict

PROBLEMATIC_CHARS = r"[★☆♥♦●○◆◇■□▪▫]"


def check_formatting_issues(resume_data: dict) -> Dict:
    """Check for ATS-unfriendly formatting"""
    issues = []
    personal_info = resume_data.get("personal_info", {})

    # Check name
    name = personal_info.get("full_name", "")
    if re.search(PROBLEMATIC_CHARS, name):
        issues.append("Remove special characters/emojis from name")

    # Check email
    email = personal_info.get("email", "")
    if email and not re.match(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email
    ):
        issues.append("Email format may not be recognized")

    # Check phone
    phone = personal_info.get("phone", "")
    if phone and not re.search(r"(\+234|0)[789]\d{9}", phone):
        issues.append(
            "Use standard phone format (e.g., +234-XXX-XXX-XXXX or 0XXX-XXX-XXXX)"
        )

    return {"has_issues": len(issues) > 0, "issues": issues}


def detect_quantifiable_achievements(text: str) -> int:
    """Detect quantified achievements in text"""
    if not text:
        return 0

    patterns = [
        r"\d+%",
        r"\$\d+",
        r"\d+[kKmM]",
        r"increased by \d+",
        r"reduced by \d+",
        r"improved by \d+",
        r"saved \d+",
        r"\d+ users",
        r"\d+ customers",
    ]

    count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in patterns)
    return min(count, 5)
