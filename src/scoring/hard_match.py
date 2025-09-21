import re
from difflib import SequenceMatcher

def calculate_hard_match(resume_data, jd_data):
    """
    Calculate the hard match score based on exact and fuzzy matches of skills.

    Parameters:
    resume_data (dict): Resume data with skills and other information
    jd_data (dict): Job description data with required skills

    Returns:
    float: A score between 0 and 100 representing the hard match.
    """
    # Extract skills from both resume and JD
    if isinstance(resume_data, dict):
        resume_skills = resume_data.get('skills', [])
    else:
        resume_skills = extract_skills_from_text(str(resume_data))
    
    if isinstance(jd_data, dict):
        required_skills = jd_data.get('required_skills', {}).get('required', [])
        preferred_skills = jd_data.get('required_skills', {}).get('preferred', [])
        all_jd_skills = required_skills + preferred_skills
    else:
        all_jd_skills = extract_skills_from_text(str(jd_data))
    
    if not all_jd_skills:
        return 0.0
    
    # Calculate exact matches
    exact_matches = set([skill.lower() for skill in resume_skills]) & set([skill.lower() for skill in all_jd_skills])
    exact_score = len(exact_matches) / len(all_jd_skills) * 100
    
    # Calculate fuzzy matches for remaining skills using difflib
    fuzzy_matches = 0
    remaining_jd_skills = [skill for skill in all_jd_skills if skill.lower() not in [s.lower() for s in exact_matches]]
    remaining_resume_skills = [skill for skill in resume_skills if skill.lower() not in [s.lower() for s in exact_matches]]
    
    for jd_skill in remaining_jd_skills:
        best_similarity = 0
        for resume_skill in remaining_resume_skills:
            similarity = SequenceMatcher(None, jd_skill.lower(), resume_skill.lower()).ratio()
            best_similarity = max(best_similarity, similarity)
        
        if best_similarity >= 0.8:  # 80% similarity threshold
            fuzzy_matches += 1
    
    fuzzy_score = fuzzy_matches / len(all_jd_skills) * 100 if all_jd_skills else 0
    
    # Combine exact and fuzzy scores (weighted towards exact matches)
    final_score = (exact_score * 0.8) + (fuzzy_score * 0.2)
    
    return min(final_score, 100.0)

def extract_skills_from_text(text):
    """Extract skills from raw text if structured data is not available"""
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