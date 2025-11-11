class Resume:
    def __init__(self, skills=None, education=None, experience=None):
        self.skills = skills or []
        self.education = education or []
        self.experience = experience or []
    
    def to_dict(self):
        """Convert Resume object to dictionary"""
        return {
            "skills": self.skills,
            "education": self.education,
            "experience": self.experience
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Resume object from dictionary"""
        return cls(
            skills=data.get("skills", []),
            education=data.get("education", []),
            experience=data.get("experience", [])
        )