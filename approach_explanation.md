# Approach Explanation - Persona-Driven Document Intelligence

## Methodology Overview

Our solution implements a multi-stage document analysis pipeline that intelligently extracts and ranks relevant sections based on persona-specific requirements. The approach combines TF-IDF-based similarity with domain-aware scoring to deliver personalized document insights while maintaining a lightweight footprint under 1GB.

## Core Architecture

### 1. Document Processing & Section Extraction
The system begins by parsing PDF documents using PyMuPDF, extracting both structural elements (headings, page numbers) and content. We employ intelligent heading detection using regex patterns to identify section boundaries, avoiding the common pitfall of treating entire pages as single sections. This ensures granular content extraction while maintaining document structure.

### 2. Multi-Factor Ranking Algorithm
Our ranking methodology combines four weighted factors to determine section relevance:

- **TF-IDF Similarity (40%)**: Uses scikit-learn's TF-IDF vectorizer with cosine similarity to compute content relevance to the query. This lightweight approach provides robust text similarity without heavy model dependencies.

- **Keyword Relevance (30%)**: Calculates keyword overlap between the query and section content, ensuring domain-specific terminology is properly weighted.

- **Position Importance (20%)**: Considers document structure by prioritizing earlier pages and higher-level headings, reflecting typical document organization patterns.

- **Content Quality (10%)**: Evaluates content structure, technical depth, and actionable information to filter out low-quality sections.

### 3. Persona-Specific Optimization
The system implements domain-aware scoring that adapts to different personas:
- **Research personas** receive boosts for methodological content, data analysis, and research findings
- **Business personas** are prioritized for compliance, risk management, and procedural content
- **Educational personas** focus on learning objectives, assessment criteria, and conceptual explanations

### 4. Content Deduplication & Optimization
To meet the 60-second processing constraint, we implement efficient deduplication using content fingerprints and quality filtering. Sections are truncated to 500 characters for the refined_text output, ensuring concise yet informative summaries.

## Technical Constraints Compliance

- **CPU Only**: All operations use scikit-learn and numpy, ensuring CPU compatibility
- **Model Size ≤ 1GB**: TF-IDF vectorizer with limited features (~50MB total footprint)
- **Processing Time ≤ 60 seconds**: Optimized batch processing and efficient algorithms ensure timely execution
- **No Internet Access**: All processing is done locally with no external dependencies

## Output Structure

The system generates a structured JSON output with:
- **Metadata**: Input documents, persona, job description, and timestamp
- **Extracted Sections**: Top 10 ranked sections with document, page, title, and importance rank
- **Subsection Analysis**: Detailed analysis with refined text (≤500 chars) and importance ranking

This approach ensures that the solution is generic enough to handle diverse document types, personas, and job requirements while maintaining high relevance and performance standards within the strict model size constraints. 