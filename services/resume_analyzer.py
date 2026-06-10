class ResumeAnalyzer:
    def analyze(self, parsed_data: dict):
        skills = parsed_data.get("skills", [])
        education = parsed_data.get("education", [])
        experience = parsed_data.get("experience", [])
        email = parsed_data.get("email")
        phone = parsed_data.get("phone")

        strengths = []
        weaknesses = []
        score = 0
        
        if email:
            score += 10
        else:
            weaknesses.append("Missing Email Address.")
        
        if phone:
            score += 10
        else:
            weaknesses.append("Missing Phone Number.")

        if len(education) > 0:
            score += 20
            strengths.append("Education section present.")
        else:
            weaknesses.append("Education section missing.")

        if len(experience) > 0:
            score += 20
            strengths.append("Experience section present.")
        else:
            weaknesses.append("No experience section detected.")

        backend_keywords = {
            "python",
            "fastapi",
            "django",
            "flask",
            "docker",
            "postgresql",
            "redis",
            "git",
            "sqlalchemy",
            "linux",
            "rest apis",
            "kafka",
            "kubernetes",
            "aws",
            "microservices",
            "distributed systems"
        }

        matched_skills = [
            skill
            for skill in skills
            if skill.lower() in backend_keywords
        ]

        if matched_skills:
            score += min(len(matched_skills) * 2, 20)

            if len(matched_skills) >= 5:
                strengths.append("Strong backend technology stack detected.")
            else:
                strengths.append("Some backend technologies detected.")
        else:
            weaknesses.append("No major backend technologies detected.")
        
        if len(matched_skills) >= 5:
            score += 20
            strengths.append("Strong technical skill set.")
        else:
            weaknesses.append("Limited technical skills listed.")

        return {
            "resume_score": min(score, 100),
            "skills_count": len(skills),
            "education_count": len(education),
            "experience_count": len(experience),
            "backend_skills": matched_skills,
            "strengths": strengths,
            "weaknesses": weaknesses
        }