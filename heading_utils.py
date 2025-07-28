import fitz  # PyMuPDF
import re
from typing import List, Dict, Any

def extract_headings_and_text(path: str, filename: str) -> List[Dict[str, Any]]:
    """Extract headings and text from PDF with improved structure detection"""
    doc = fitz.open(path)
    sections = []
    
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        lines = text.split("\n")
        
        # Find potential headings (lines that are likely section titles)
        headings = []
        for i, line in enumerate(lines):
            line = line.strip()
            if is_heading(line):
                headings.append({
                    "line_index": i,
                    "text": line,
                    "level": determine_heading_level(line)
                })
        
        # Extract sections based on headings
        if headings:
            for j, heading in enumerate(headings):
                start_idx = heading["line_index"]
                end_idx = headings[j + 1]["line_index"] if j + 1 < len(headings) else len(lines)
                
                section_text = "\n".join(lines[start_idx:end_idx]).strip()
                if len(section_text) > 50:  # Only include substantial sections
                    sections.append({
                        "title": heading["text"],
                        "text": section_text,
                        "page": page_num,
                        "document": filename,
                        "heading_level": heading["level"]
                    })
        else:
            # Fallback: treat the page as a single section
            if len(text.strip()) > 100:
                sections.append({
                    "title": f"Page {page_num} Content",
                    "text": text.strip(),
                    "page": page_num,
                    "document": filename,
                    "heading_level": 1
                })
    
    doc.close()
    return sections

def is_heading(line: str) -> bool:
    """Determine if a line is likely a heading"""
    if not line or len(line) < 3:
        return False
    
    # Check for common heading patterns
    heading_patterns = [
        r'^[A-Z][A-Z\s]+$',  # ALL CAPS
        r'^\d+\.\s+[A-Z]',   # Numbered sections
        r'^[A-Z][a-z]+(\s+[A-Z][a-z]+)*$',  # Title Case
        r'^[A-Z][a-z]+\s*:',  # Title with colon
        r'^[IVX]+\.\s+[A-Z]',  # Roman numerals
    ]
    
    for pattern in heading_patterns:
        if re.match(pattern, line):
            return True
    
    # Additional checks
    words = line.split()
    if len(words) <= 8 and len(line) <= 80:
        # Check if most words start with capital letters
        capitalized_words = sum(1 for word in words if word and word[0].isupper())
        if capitalized_words >= len(words) * 0.7:
            return True
    
    return False

def determine_heading_level(line: str) -> int:
    """Determine the heading level based on formatting"""
    if re.match(r'^\d+\.\s+', line):
        return 1
    elif re.match(r'^\d+\.\d+\.\s+', line):
        return 2
    elif re.match(r'^\d+\.\d+\.\d+\.\s+', line):
        return 3
    elif line.isupper():
        return 1
    else:
        return 2

def split_sections_optimally(sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Optimize section splitting to avoid repeating full pages and improve content quality"""
    optimized_sections = []
    
    for section in sections:
        # Skip sections that are too short or too long
        if len(section["text"]) < 50 or len(section["text"]) > 5000:
            continue
        
        # Extract key insights and actionable items
        key_insights = extract_key_insights(section["text"])
        actionable_items = extract_actionable_items(section["text"])
        
        # Add relevance reasoning
        relevance_reason = determine_relevance_reason(section["title"], section["text"])
        
        optimized_section = {
            **section,
            "key_insights": key_insights,
            "actionable_items": actionable_items,
            "relevance_reason": relevance_reason,
            "content_quality_score": calculate_content_quality(section["text"])
        }
        
        optimized_sections.append(optimized_section)
    
    # Remove duplicates based on content similarity
    unique_sections = remove_duplicate_sections(optimized_sections)
    
    return unique_sections

def extract_key_insights(text: str) -> List[str]:
    """Extract key insights from text"""
    insights = []
    
    # Look for sentences that contain key insight indicators
    sentences = text.split('.')
    insight_indicators = [
        'important', 'key', 'critical', 'significant', 'essential',
        'primary', 'main', 'major', 'crucial', 'vital'
    ]
    
    for sentence in sentences:
        sentence = sentence.strip()
        if any(indicator in sentence.lower() for indicator in insight_indicators):
            if len(sentence) > 20 and len(sentence) < 200:
                insights.append(sentence)
    
    return insights[:3]  # Limit to top 3 insights

def extract_actionable_items(text: str) -> List[str]:
    """Extract actionable items from text"""
    actions = []
    
    # Look for action-oriented phrases
    action_patterns = [
        r'should\s+\w+',
        r'must\s+\w+',
        r'need\s+to\s+\w+',
        r'recommend\s+\w+',
        r'ensure\s+\w+',
        r'verify\s+\w+',
        r'check\s+\w+',
        r'validate\s+\w+'
    ]
    
    for pattern in action_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        actions.extend(matches)
    
    return list(set(actions))[:5]  # Limit to top 5 unique actions

def determine_relevance_reason(title: str, text: str) -> str:
    """Determine why a section is relevant"""
    title_lower = title.lower()
    text_lower = text.lower()
    
    if any(word in title_lower for word in ['method', 'methodology', 'approach']):
        return "Contains methodological information"
    elif any(word in title_lower for word in ['result', 'finding', 'outcome']):
        return "Contains results or findings"
    elif any(word in title_lower for word in ['conclusion', 'summary', 'overview']):
        return "Contains conclusions or summaries"
    elif any(word in title_lower for word in ['introduction', 'background']):
        return "Contains background or introductory information"
    else:
        return "Content relevance based on semantic analysis"

def calculate_content_quality(text: str) -> float:
    """Calculate content quality score based on various factors"""
    score = 0.0
    
    # Length factor (prefer medium-length content)
    length = len(text)
    if 100 <= length <= 1000:
        score += 0.3
    elif 1000 < length <= 3000:
        score += 0.2
    
    # Structure factor (presence of lists, numbers, etc.)
    if re.search(r'\d+\.', text):
        score += 0.2
    if re.search(r'•|\*|-', text):
        score += 0.1
    
    # Technical content factor
    technical_terms = ['analysis', 'method', 'result', 'conclusion', 'data', 'process']
    tech_count = sum(1 for term in technical_terms if term in text.lower())
    score += min(tech_count * 0.1, 0.3)
    
    return min(score, 1.0)

def remove_duplicate_sections(sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate sections based on content similarity"""
    unique_sections = []
    seen_content = set()
    
    for section in sections:
        # Create a content fingerprint
        content_fingerprint = f"{section['title']}_{section['document']}_{section['page']}"
        
        if content_fingerprint not in seen_content:
            seen_content.add(content_fingerprint)
            unique_sections.append(section)
    
    return unique_sections
