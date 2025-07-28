import re
from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize lightweight TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    max_features=1000,  # Limit features to keep memory usage low
    stop_words='english',
    ngram_range=(1, 2),  # Use unigrams and bigrams
    min_df=1,
    max_df=0.95
)

def rank_sections_by_similarity(sections: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """Rank sections by TF-IDF similarity to the query"""
    if not sections:
        return []
    
    # Prepare section texts for vectorization
    section_texts = [f"{s['title']} - {s['text']}" for s in sections]
    
    # Add query to the corpus for vectorization
    all_texts = [query] + section_texts
    
    # Create TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Calculate similarities between query and sections
    query_vector = tfidf_matrix[0:1]
    section_vectors = tfidf_matrix[1:]
    
    similarities = cosine_similarity(query_vector, section_vectors).flatten()
    
    # Combine with additional ranking factors
    ranked_sections = []
    for i, (similarity, section) in enumerate(zip(similarities, sections)):
        # Calculate additional importance factors
        keyword_score = calculate_keyword_relevance(section, query)
        position_score = calculate_position_score(section)
        content_quality_score = section.get('content_quality_score', 0.5)
        
        # Combine scores with weights
        combined_score = (
            similarity * 0.4 +  # TF-IDF similarity (40%)
            keyword_score * 0.3 +      # Keyword relevance (30%)
            position_score * 0.2 +     # Position importance (20%)
            content_quality_score * 0.1 # Content quality (10%)
        )
        
        ranked_sections.append({
            **section,
            'tfidf_similarity': similarity,
            'keyword_score': keyword_score,
            'position_score': position_score,
            'combined_score': combined_score
        })
    
    # Sort by combined score
    ranked_sections.sort(key=lambda x: x['combined_score'], reverse=True)
    
    return ranked_sections

def calculate_keyword_relevance(section: Dict[str, Any], query: str) -> float:
    """Calculate keyword relevance score"""
    query_words = set(re.findall(r'\b\w+\b', query.lower()))
    section_text = f"{section['title']} {section['text']}".lower()
    section_words = set(re.findall(r'\b\w+\b', section_text))
    
    # Calculate keyword overlap
    overlap = len(query_words.intersection(section_words))
    total_query_words = len(query_words)
    
    if total_query_words == 0:
        return 0.0
    
    return min(overlap / total_query_words, 1.0)

def calculate_position_score(section: Dict[str, Any]) -> float:
    """Calculate position-based importance score"""
    page = section.get('page', 1)
    heading_level = section.get('heading_level', 2)
    
    # Page position score (earlier pages get higher scores)
    page_score = max(0.1, 1.0 - (page - 1) * 0.05)
    
    # Heading level score (lower level = higher importance)
    level_score = max(0.1, 1.0 - (heading_level - 1) * 0.2)
    
    return (page_score + level_score) / 2

def calculate_importance_score(section: Dict[str, Any], persona: str, job: str) -> float:
    """Calculate importance score based on multiple factors"""
    base_score = section.get('combined_score', 0.0)
    
    # Persona-specific scoring
    persona_boost = calculate_persona_boost(section, persona)
    
    # Job-specific scoring
    job_boost = calculate_job_boost(section, job)
    
    # Content type scoring
    content_type_boost = calculate_content_type_boost(section)
    
    # Final importance score
    importance_score = base_score * (1 + persona_boost + job_boost + content_type_boost)
    
    return min(importance_score, 1.0)  # Cap at 1.0

def calculate_persona_boost(section: Dict[str, Any], persona: str) -> float:
    """Calculate persona-specific boost"""
    persona_lower = persona.lower()
    section_text = f"{section['title']} {section['text']}".lower()
    
    boost = 0.0
    
    # Research persona
    if 'research' in persona_lower or 'phd' in persona_lower:
        research_keywords = ['methodology', 'analysis', 'data', 'results', 'conclusion', 'study', 'research']
        research_matches = sum(1 for keyword in research_keywords if keyword in section_text)
        boost += research_matches * 0.1
    
    # Business persona
    elif 'business' in persona_lower or 'analyst' in persona_lower:
        business_keywords = ['compliance', 'risk', 'management', 'procedure', 'policy', 'regulation']
        business_matches = sum(1 for keyword in business_keywords if keyword in section_text)
        boost += business_matches * 0.1
    
    # Education persona
    elif 'professor' in persona_lower or 'education' in persona_lower or 'student' in persona_lower:
        education_keywords = ['curriculum', 'assessment', 'learning', 'teaching', 'course', 'student', 'concept']
        education_matches = sum(1 for keyword in education_keywords if keyword in section_text)
        boost += education_matches * 0.1
    
    return min(boost, 0.3)  # Cap at 30% boost

def calculate_job_boost(section: Dict[str, Any], job: str) -> float:
    """Calculate job-specific boost"""
    job_lower = job.lower()
    section_text = f"{section['title']} {section['text']}".lower()
    
    boost = 0.0
    
    # Literature review job
    if 'literature review' in job_lower:
        review_keywords = ['previous', 'existing', 'literature', 'review', 'background', 'related work']
        review_matches = sum(1 for keyword in review_keywords if keyword in section_text)
        boost += review_matches * 0.08
    
    # Compliance analysis job
    elif 'compliance' in job_lower or 'regulatory' in job_lower:
        compliance_keywords = ['requirement', 'standard', 'regulation', 'compliance', 'audit', 'policy']
        compliance_matches = sum(1 for keyword in compliance_keywords if keyword in section_text)
        boost += compliance_matches * 0.08
    
    # Curriculum development job
    elif 'curriculum' in job_lower or 'assessment' in job_lower:
        curriculum_keywords = ['objective', 'outcome', 'assessment', 'evaluation', 'criteria', 'rubric']
        curriculum_matches = sum(1 for keyword in curriculum_keywords if keyword in section_text)
        boost += curriculum_matches * 0.08
    
    # Exam preparation job
    elif 'exam' in job_lower or 'preparation' in job_lower:
        exam_keywords = ['concept', 'mechanism', 'reaction', 'kinetics', 'principle', 'theory']
        exam_matches = sum(1 for keyword in exam_keywords if keyword in section_text)
        boost += exam_matches * 0.08
    
    return min(boost, 0.2)  # Cap at 20% boost

def calculate_content_type_boost(section: Dict[str, Any]) -> float:
    """Calculate content type boost based on section characteristics"""
    title = section.get('title', '').lower()
    text = section.get('text', '').lower()
    
    boost = 0.0
    
    # Methodological content
    if any(word in title for word in ['method', 'methodology', 'approach', 'procedure']):
        boost += 0.15
    
    # Results and findings
    if any(word in title for word in ['result', 'finding', 'outcome', 'conclusion']):
        boost += 0.12
    
    # Technical specifications
    if any(word in title for word in ['specification', 'requirement', 'standard', 'criteria']):
        boost += 0.10
    
    # Content with actionable information
    action_words = ['should', 'must', 'need to', 'recommend', 'ensure']
    if any(word in text for word in action_words):
        boost += 0.08
    
    return min(boost, 0.25)  # Cap at 25% boost
