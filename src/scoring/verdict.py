def get_verdict(final_score):
    """
    Determine the verdict based on the final combined score.
    
    Parameters:
    final_score (float): The final combined score between hard and semantic match
    
    Returns:
    str: Verdict categorization (High, Medium, Low)
    """
    if final_score >= 80:
        return "High"
    elif final_score >= 50:
        return "Medium"
    else:
        return "Low"

def get_detailed_verdict(hard_match_score, semantic_match_score):
    """
    Get a detailed verdict with breakdown.
    
    Parameters:
    hard_match_score (float): Hard match score
    semantic_match_score (float): Semantic match score
    
    Returns:
    dict: Detailed verdict information
    """
    combined_score = (hard_match_score * 0.6) + (semantic_match_score * 0.4)
    verdict = get_verdict(combined_score)
    
    return {
        "verdict": verdict,
        "combined_score": combined_score,
        "hard_match_score": hard_match_score,
        "semantic_match_score": semantic_match_score,
        "explanation": get_explanation(verdict, hard_match_score, semantic_match_score)
    }

def get_explanation(verdict, hard_match_score, semantic_match_score):
    """Generate explanation for the verdict"""
    explanations = {
        "High": "Excellent match! The resume shows strong alignment with job requirements.",
        "Medium": "Good match with some gaps. Consider highlighting relevant experience.",
        "Low": "Limited match. Significant skill gaps or experience differences noted."
    }
    
    base_explanation = explanations.get(verdict, "")
    
    details = []
    if hard_match_score < 30:
        details.append("Few matching technical skills found.")
    elif hard_match_score < 60:
        details.append("Some technical skills match, but gaps remain.")
    else:
        details.append("Strong technical skill alignment.")
    
    if semantic_match_score < 30:
        details.append("Limited contextual similarity.")
    elif semantic_match_score < 60:
        details.append("Moderate contextual alignment.")
    else:
        details.append("High contextual similarity.")
    
    return f"{base_explanation} {' '.join(details)}"