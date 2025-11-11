import spacy
from utils.text_extractor import extract_text
from models.resume import Resume

class ResumeParser:
    def __init__(self):
        # Load English language model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Define skill keywords (expand this list as needed)
        self.skill_patterns = [
            "python", "javascript", "java", "c++", "react", "node.js",
            "machine learning", "data analysis", "project management",
            "leadership", "communication", "problem solving"
        ]
    
    def parse(self, text):
        doc = self.nlp(text)
        
        # Extract skills
        skills = self._extract_skills(doc)
        
        # Extract education
        education = self._extract_education(doc)
        
        # Extract work experience
        experience = self._extract_experience(doc)
        
        return Resume(
            skills=skills,
            education=education,
            experience=experience
        ).to_dict()
    
    def _extract_skills(self, doc):
        skills = []
        text_lower = doc.text.lower()
        
        for skill in self.skill_patterns:
            if skill in text_lower:
                # Calculate a confidence score based on frequency and context
                frequency = text_lower.count(skill)
                confidence = min(frequency * 20, 100)  # Scale up to 100
                skills.append({
                    "name": skill.title(),
                    "score": confidence
                })
        
        return skills
    
    def _extract_education(self, doc):
        education = []
        edu_keywords = ["university", "college", "institute", "bachelor", "master", "phd"]
        
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in edu_keywords):
                education.append(sent.text.strip())
        
        return education
    
    def _extract_experience(self, doc):
        experience = []
        
        # Look for date patterns and job title patterns
        for ent in doc.ents:
            if ent.label_ in ["DATE", "ORG"]:
                # Extract surrounding context
                start = max(0, ent.start - 10)
                end = min(len(doc), ent.end + 10)
                context = doc[start:end].text
                experience.append(context)
        
        return experience

def parse_resume(file_path):
    """Main function to parse resume file"""
    # Extract text from file
    text = extract_text(file_path)
    
    # Parse the text
    parser = ResumeParser()
    resume_data = parser.parse(text)
    
    return resume_data