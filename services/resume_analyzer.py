class ResumeAnalyzer:
    def analyze(self, parsed_data: dict):
        skills = parsed_data.get("skills", [])
        education = parsed_data.get("education", [])
        experience = parsed_data.get("experience", [])

        strengths = []
        weaknesses = []

        skills_count = len(skills)
        education_count = len(education)
        experience_count = len(experience)
        
        if skills_count >= 5:
            strengths.append("Strong technical skills.")
        else:
            weaknesses.append("Weak technical skills.")

        if education_count > 0:
            strengths.append("Education section present.")
        else:
            weaknesses.append("Education section missing.")

        if experience_count > 0:
            strengths.append("Experience section present.")
        else:
            weaknesses.append("No experience section detected.")

        resume_score = (
            min(skills_count * 10, 50)
            + min(education_count * 20, 30)
            + min(experience_count * 20, 20)
        )

        return {
            "skills_count": skills_count,
            "education_count": education_count,
            "experience_count": experience_count,
            "resume_score": resume_score,
            "strengths": strengths,
            "weaknesses": weaknesses
        }