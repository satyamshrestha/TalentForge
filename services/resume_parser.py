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

        skills = self._extract_section(
            lines,
            "TECHNICAL SKILLS",
            {
                "CERTIFICATIONS",
                "LANGUAGES",
                "PROJECTS",
                "EXPERIENCE",
                "EDUCATION"
            }            
        )

        education = self._extract_section(
            lines,
            "EDUCATION",
            {
                "EXPERIENCE",
                "PROJECTS",
                "TECHNICAL SKILLS",
                "CERTIFICATIONS",
                "LANGUAGES"
            }
        )

        experience = self._extract_section(
            lines,
            "EXPERIENCE",
            {
                "PROJECTS",
                "TECHNICAL SKILLS",
                "CERTIFICATIONS",
                "LANGUAGES"
            }
        )
        return {
            "raw_text": text,
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "education": education,
            "experience": experience
        }
    
    def _extract_section(
        self,
        lines: list[str],
        section_name: str,
        stop_headers: set[str]
    ):
        result = []
        try:
            start_idx = lines.index(section_name) + 1
        except ValueError:
            return result
        
        for line in lines[start_idx:]:
            if line in stop_headers:
                break
            result.append(line)
                
        return result