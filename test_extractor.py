#!/usr/bin/env python3
"""
Test script for the enhanced 1B extractor
This script demonstrates the functionality without requiring the actual model
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

def create_mock_sections() -> List[Dict[str, Any]]:
    """Create mock sections for testing"""
    return [
        {
            "title": "Methodology and Approach",
            "text": "This section describes the research methodology used in computational biology. The approach involves data analysis, statistical methods, and performance benchmarks. Key findings include significant improvements in accuracy and efficiency.",
            "page": 1,
            "document": "research_paper.pdf",
            "heading_level": 1,
            "key_insights": [
                "Research methodology involves data analysis and statistical methods",
                "Significant improvements in accuracy and efficiency achieved"
            ],
            "actionable_items": [
                "should implement the described methodology",
                "must verify the statistical methods"
            ],
            "relevance_reason": "Contains methodological information",
            "content_quality_score": 0.85
        },
        {
            "title": "Compliance Requirements",
            "text": "This document outlines the compliance requirements for financial services. Risk management procedures must be followed according to regulatory standards. All policies should be reviewed annually.",
            "page": 2,
            "document": "compliance_guide.pdf",
            "heading_level": 1,
            "key_insights": [
                "Compliance requirements are mandatory for financial services",
                "Risk management procedures must follow regulatory standards"
            ],
            "actionable_items": [
                "must follow risk management procedures",
                "should review policies annually"
            ],
            "relevance_reason": "Contains compliance and regulatory information",
            "content_quality_score": 0.90
        },
        {
            "title": "Curriculum Development",
            "text": "The curriculum development process involves creating learning objectives and assessment criteria. Students should demonstrate proficiency in advanced programming concepts. Evaluation methods include practical assignments and theoretical assessments.",
            "page": 3,
            "document": "curriculum_manual.pdf",
            "heading_level": 1,
            "key_insights": [
                "Curriculum development requires clear learning objectives",
                "Assessment criteria must evaluate both practical and theoretical skills"
            ],
            "actionable_items": [
                "should create clear learning objectives",
                "must develop comprehensive assessment criteria"
            ],
            "relevance_reason": "Contains educational content and assessment information",
            "content_quality_score": 0.88
        }
    ]

def mock_rank_sections(sections: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """Mock ranking function that simulates the semantic ranking"""
    # Simulate different scores based on content relevance
    for i, section in enumerate(sections):
        # Simulate semantic similarity (0.6-0.9 range)
        semantic_sim = 0.6 + (i * 0.1)
        
        # Simulate keyword relevance
        query_words = set(query.lower().split())
        section_words = set(f"{section['title']} {section['text']}".lower().split())
        keyword_score = len(query_words.intersection(section_words)) / len(query_words) if query_words else 0.5
        
        # Simulate position score
        position_score = max(0.1, 1.0 - (section['page'] - 1) * 0.1)
        
        # Combine scores
        combined_score = (
            semantic_sim * 0.4 +
            keyword_score * 0.3 +
            position_score * 0.2 +
            section.get('content_quality_score', 0.5) * 0.1
        )
        
        section.update({
            'semantic_similarity': semantic_sim,
            'keyword_score': keyword_score,
            'position_score': position_score,
            'combined_score': combined_score
        })
    
    # Sort by combined score
    sections.sort(key=lambda x: x['combined_score'], reverse=True)
    return sections

def generate_test_output(persona: str, job: str) -> Dict[str, Any]:
    """Generate test output for a given persona and job"""
    sections = create_mock_sections()
    ranked_sections = mock_rank_sections(sections, f"{persona}. Task: {job}")
    
    output = {
        "metadata": {
            "input_documents": ["research_paper.pdf", "compliance_guide.pdf", "curriculum_manual.pdf"],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    for i, item in enumerate(ranked_sections[:3]):
        output["extracted_sections"].append({
            "document": item["document"],
            "page_number": item["page"],
            "section_title": item["title"],
            "importance_rank": i + 1
        })
        
        # Truncate text to meet constraints (500 chars max for refined_text)
        refined_text = item["text"]
        if len(refined_text) > 500:
            refined_text = refined_text[:497] + "..."
        
        output["subsection_analysis"].append({
            "document": item["document"],
            "page_number": item["page"],
            "refined_text": refined_text,
            "importance_rank": i + 1
        })
    
    return output

def main():
    """Main test function"""
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Test personas
    test_personas = {
        "research": {
            "persona": "PhD Researcher in Computational Biology",
            "job_to_be_done": "Prepare a literature review focusing on methodologies, datasets, and performance benchmarks"
        },
        "business": {
            "persona": "Investment Analyst",
            "job_to_be_done": "Analyze revenue trends, R&D investments, and market positioning strategies"
        },
        "education": {
            "persona": "Undergraduate Chemistry Student",
            "job_to_be_done": "Identify key concepts and mechanisms for exam preparation on reaction kinetics"
        }
    }
    
    # Generate test outputs
    for persona_type, persona_data in test_personas.items():
        output = generate_test_output(persona_data["persona"], persona_data["job_to_be_done"])
        
        with open(f"output/test_{persona_type}_output.json", "w") as f:
            json.dump(output, f, indent=2)
        
        print(f"Generated test output for {persona_type} persona")
    
    # Generate main output (using research persona as default)
    main_output = generate_test_output(
        test_personas["research"]["persona"],
        test_personas["research"]["job_to_be_done"]
    )
    
    with open("output/test_challenge1b_output.json", "w") as f:
        json.dump(main_output, f, indent=2)
    
    print("Test outputs generated successfully!")
    print("Files created:")
    print("- output/test_research_output.json")
    print("- output/test_business_output.json")
    print("- output/test_education_output.json")
    print("- output/test_challenge1b_output.json")

if __name__ == "__main__":
    main() 