from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class JobMatcher:
    def __init__(self):
        # Sample job database (in production, this would come from a real database)
        self.jobs = [
            {
                "title": "Software Engineer",
                "description": "Developing web applications using Python, JavaScript, and modern frameworks",
                "required_skills": ["python", "javascript", "react", "node.js"],
                "industry": "Technology"
            },
            {
                "title": "Data Scientist",
                "description": "Analyzing data and building machine learning models",
                "required_skills": ["python", "machine learning", "data analysis"],
                "industry": "Data Science"
            },
            {
                "title": "Project Manager",
                "description": "Leading technical projects and coordinating with stakeholders",
                "required_skills": ["project management", "leadership", "communication"],
                "industry": "Management"
            }
        ]
        
        self.vectorizer = TfidfVectorizer()
    
    def match_jobs(self, resume_data):
        # Extract skills from resume
        resume_skills = [skill["name"].lower() for skill in resume_data["skills"]]
        
        # Calculate job matches
        job_matches = []
        for job in self.jobs:
            match_score = self._calculate_match_score(resume_skills, job["required_skills"])
            job_matches.append({
                "title": job["title"],
                "description": job["description"],
                "matchScore": match_score,
                "industry": job["industry"]
            })
        
        # Sort by match score
        job_matches.sort(key=lambda x: x["matchScore"], reverse=True)
        
        # Calculate industry matches
        industry_matches = self._calculate_industry_matches(job_matches)
        
        return {
            "recommendations": job_matches[:3],  # Top 3 recommendations
            "industries": industry_matches
        }
    
    def _calculate_match_score(self, resume_skills, job_skills):
        # Convert skills to sets for comparison
        resume_set = set(resume_skills)
        job_set = set(job_skills)
        
        # Calculate match score
        matched_skills = resume_set.intersection(job_set)
        match_score = (len(matched_skills) / len(job_set)) * 100
        
        return round(match_score)
    
    def _calculate_industry_matches(self, job_matches):
        industry_scores = {}
        
        # Aggregate scores by industry
        for job in job_matches:
            industry = job["industry"]
            score = job["matchScore"]
            
            if industry in industry_scores:
                industry_scores[industry] = max(industry_scores[industry], score)
            else:
                industry_scores[industry] = score
        
        # Convert to list format
        industry_matches = [
            {"name": industry, "matchScore": score}
            for industry, score in industry_scores.items()
        ]
        
        # Sort by match score
        industry_matches.sort(key=lambda x: x["matchScore"], reverse=True)
        
        return industry_matches

def match_jobs(resume_data):
    """Main function to match resume with jobs"""
    matcher = JobMatcher()
    return matcher.match_jobs(resume_data)