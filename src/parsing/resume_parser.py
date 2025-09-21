import re
import tempfile
import os
from fastapi import UploadFile
from src.utils.text_extraction import extract_text

class ResumeParser:
    def __init__(self):
        pass

    async def parse(self, file: UploadFile):
        """Parse uploaded resume file and extract text and structured data"""
        # Save uploaded file temporarily
        file_extension = os.path.splitext(file.filename or '')[1] or '.tmp'
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file.flush()
            
            try:
                # Extract text from file
                text = extract_text(tmp_file.name)
                
                # Extract structured information
                structured_data = {
                    "raw_text": text,
                    "contact_info": self.extract_contact_info(text),
                    "skills": self.extract_skills(text),
                    "experience": self.extract_experience(text),
                    "education": self.extract_education(text)
                }
                
                return structured_data
            finally:
                # Clean up temporary file
                os.unlink(tmp_file.name)

    def extract_contact_info(self, text):
        """Extract contact information from resume text"""
        contact_info = {}
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        contact_info['email'] = emails[0] if emails else None
        
        # Extract phone number
        phone_pattern = r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b'
        phones = re.findall(phone_pattern, text)
        contact_info['phone'] = '-'.join(phones[0]) if phones else None
        
        return contact_info

    def extract_skills(self, text):
        """Extract skills from resume text"""
        # Common technical skills keywords
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'express',
            'django', 'flask', 'fastapi', 'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'gitlab',
            'html', 'css', 'bootstrap', 'tailwind', 'machine learning', 'data science',
            'artificial intelligence', 'deep learning', 'tensorflow', 'pytorch', 'pandas',
            'numpy', 'scikit-learn', 'api', 'rest', 'graphql', 'microservices'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills

    def extract_experience(self, text):
        """Extract work experience from resume text"""
        # Basic experience extraction - look for year patterns and job titles
        experience_sections = []
        
        # Look for year patterns (e.g., 2020-2023, 2020-Present)
        year_patterns = re.findall(r'\b(20\d{2})[-–](20\d{2}|Present|present)\b', text)
        
        for pattern in year_patterns:
            experience_sections.append({
                'start_year': pattern[0],
                'end_year': pattern[1]
            })
        
        return experience_sections

    def extract_education(self, text):
        """Extract education details from resume text"""
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'institute']
        education_info = []
        
        text_lower = text.lower()
        for keyword in education_keywords:
            if keyword in text_lower:
                education_info.append(keyword)
        
        return education_info

    def normalize_text(self, text):
        """Normalize text by removing special characters and lowercasing"""
        # Remove special characters and extra whitespace
        normalized = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        normalized = re.sub(r'\s+', ' ', normalized)
        return normalized.strip().lower()