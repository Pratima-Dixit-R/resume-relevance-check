import re
import tempfile
import os
from fastapi import UploadFile
from src.utils.text_extraction import extract_text

class JDParser:
    def __init__(self):
        pass

    async def parse(self, file: UploadFile):
        """Parse uploaded job description file and extract text and structured data"""
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
                    "role_title": self.extract_role_title(text),
                    "required_skills": self.extract_skills(text),
                    "qualifications": self.extract_qualifications(text),
                    "experience_required": self.extract_experience_requirements(text)
                }
                
                return structured_data
            finally:
                # Clean up temporary file
                os.unlink(tmp_file.name)

    def extract_role_title(self, text):
        """Extract role title from job description"""
        # Look for common job title patterns
        title_patterns = [
            r'(?i)position[:\s]+([^\n]+)',
            r'(?i)role[:\s]+([^\n]+)',
            r'(?i)job title[:\s]+([^\n]+)',
            r'(?i)we are looking for[\s]+(?:a|an)?\s*([^\n]+)',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return None

    def extract_skills(self, text):
        """Extract required skills from job description"""
        # Common technical skills and keywords
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'express',
            'django', 'flask', 'fastapi', 'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'gitlab',
            'html', 'css', 'bootstrap', 'tailwind', 'machine learning', 'data science',
            'artificial intelligence', 'deep learning', 'tensorflow', 'pytorch', 'pandas',
            'numpy', 'scikit-learn', 'api', 'rest', 'graphql', 'microservices',
            'communication', 'teamwork', 'leadership', 'problem solving', 'analytical'
        ]
        
        text_lower = text.lower()
        required_skills = []
        preferred_skills = []
        
        # Split into required and preferred sections
        required_section = self._extract_section(text, ['required', 'must have', 'essential'])
        preferred_section = self._extract_section(text, ['preferred', 'nice to have', 'plus', 'bonus'])
        
        # Find skills in required section
        if required_section:
            for skill in skill_keywords:
                if skill.lower() in required_section.lower():
                    required_skills.append(skill)
        
        # Find skills in preferred section
        if preferred_section:
            for skill in skill_keywords:
                if skill.lower() in preferred_section.lower():
                    preferred_skills.append(skill)
        
        # If no specific sections found, look in entire text
        if not required_skills and not preferred_skills:
            for skill in skill_keywords:
                if skill.lower() in text_lower:
                    required_skills.append(skill)
        
        return {
            'required': required_skills,
            'preferred': preferred_skills
        }

    def extract_qualifications(self, text):
        """Extract qualifications from job description"""
        qualifications = []
        
        # Look for degree requirements
        degree_patterns = [
            r'(?i)(bachelor[\s\']*s?\s*degree)',
            r'(?i)(master[\s\']*s?\s*degree)',
            r'(?i)(phd|doctorate)',
            r'(?i)(\d+\+?\s*years?\s*(?:of\s+)?experience)'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, text)
            qualifications.extend(matches)
        
        return qualifications

    def extract_experience_requirements(self, text):
        """Extract experience requirements from job description"""
        # Look for experience patterns
        exp_patterns = [
            r'(?i)(\d+)\+?\s*years?\s*(?:of\s+)?experience',
            r'(?i)minimum\s*(\d+)\s*years?',
            r'(?i)at least\s*(\d+)\s*years?'
        ]
        
        experience_years = []
        for pattern in exp_patterns:
            matches = re.findall(pattern, text)
            experience_years.extend([int(match) for match in matches])
        
        return max(experience_years) if experience_years else 0

    def _extract_section(self, text, keywords):
        """Helper method to extract specific sections from text"""
        for keyword in keywords:
            pattern = rf'(?i){keyword}[^\n]*([\s\S]*?)(?=\n\s*\n|$)'
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None