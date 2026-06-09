import re

class ResumeParser:
    def parse(self, text: str):
        email_match = re.search(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            text
        )
        email = (
            email_match.group()
            if email_match
            else None
        )

        phone_match = re.search(
            r"(\+?\d[\d\s\-]{7,}\d)",
            text
        )
        phone = (
            phone_match.group()
            if phone_match
            else None
        )

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]
        name = lines[0] if lines else None

        return {
            "raw_text": text,
            "name": name,
            "email": email,
            "phone": phone,
            "skills": [],
            "education": [],
            "experience": []
        }