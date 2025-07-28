import os, json, datetime
from heading_utils import extract_headings_and_text, split_sections_optimally
from semantic_utils import rank_sections_by_similarity, calculate_importance_score
from typing import List, Dict, Any

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def load_persona_job():
    """Load persona and job description from JSON file"""
    with open(os.path.join(INPUT_DIR, "persona.json"), "r") as f:
        data = json.load(f)
    return data["persona"], data["job_to_be_done"]

def process_documents(persona: str, job: str) -> List[Dict[str, Any]]:
    """Process documents and extract relevant sections based on persona and job"""
    combined_query = f"{persona}. Task: {job}"
    
    all_sections = []
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    
    for filename in pdf_files:
        doc_path = os.path.join(INPUT_DIR, filename)
        doc_sections = extract_headings_and_text(doc_path, filename)
        all_sections.extend(doc_sections)
    
    # Optimize section splitting to avoid repeating full pages
    optimized_sections = split_sections_optimally(all_sections)
    
    # Rank sections using semantic similarity and importance scoring
    ranked_sections = rank_sections_by_similarity(optimized_sections, combined_query)
    
    return ranked_sections, pdf_files

def generate_output(ranked_sections: List[Dict], pdf_files: List[str], persona: str, job: str) -> Dict[str, Any]:
    """Generate the final output JSON with correct structure as per challenge requirements"""
    output = {
        "metadata": {
            "input_documents": pdf_files,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    # Process top 10 sections for extracted_sections
    for i, item in enumerate(ranked_sections[:10]):
        output["extracted_sections"].append({
            "document": item["document"],
            "page_number": item["page"],
            "section_title": item["title"],
            "importance_rank": i + 1
        })
    
    # Process top 10 sections for subsection_analysis
    for i, item in enumerate(ranked_sections[:10]):
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
    """Main execution function"""
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load persona and job
    persona, job = load_persona_job()
    
    # Process documents
    ranked_sections, pdf_files = process_documents(persona, job)
    
    # Generate output
    output = generate_output(ranked_sections, pdf_files, persona, job)
    
    # Save main output
    with open(os.path.join(OUTPUT_DIR, "challenge1b_output.json"), "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Processing complete. Output saved to {OUTPUT_DIR}/challenge1b_output.json")
    print(f"Processed {len(pdf_files)} documents for persona: {persona}")

if __name__ == "__main__":
    main()
