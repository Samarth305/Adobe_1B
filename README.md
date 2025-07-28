# Adobe DeepDoc Challenge 1B - Persona-Driven Document Intelligence

## Challenge Overview
This system acts as an intelligent document analyst, extracting and prioritizing the most relevant sections from a collection of documents based on a specific persona and their job-to-be-done.

**Theme**: "Connect What Matters — For the User Who Matters"

## Features
- **Generic Solution**: Handles diverse document types (research papers, textbooks, financial reports, etc.)
- **Persona-Driven**: Adapts to different personas (researchers, students, analysts, etc.)
- **Multi-Factor Ranking**: Combines semantic similarity, keyword relevance, position importance, and content quality
- **CPU-Optimized**: Runs entirely on CPU with no GPU requirements
- **Lightweight**: Model size < 1GB, processing time < 60 seconds

## Installation & Setup

### Prerequisites
- Python 3.9+
- Docker (optional, for containerized execution)

### Local Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Docker Setup
```bash
# Build the Docker image
docker build -t adobe-deepdoc-1b .

# Run the container
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output adobe-deepdoc-1b
```

## Usage

### 1. Prepare Input Files
Place your PDF documents in the `input/` directory and create a `persona.json` file:

```json
{
  "persona": "PhD Researcher in Computational Biology",
  "job_to_be_done": "Prepare a literature review focusing on methodologies, datasets, and performance benchmarks"
}
```

### 2. Run the Application
```bash
python extractor_1b.py
```

### 3. View Results
The output will be saved to `output/challenge1b_output.json` with the following structure:

```json
{
  "metadata": {
    "input_documents": ["document1.pdf", "document2.pdf"],
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare a literature review...",
    "processing_timestamp": "2024-01-01T12:00:00"
  },
  "extracted_sections": [
    {
      "document": "document1.pdf",
      "page_number": 1,
      "section_title": "Methodology",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "document1.pdf",
      "page_number": 1,
      "refined_text": "Extracted content...",
      "importance_rank": 1
    }
  ]
}
```

## Test Cases

### Test Case 1: Academic Research
- **Documents**: 4 research papers on "Graph Neural Networks for Drug Discovery"
- **Persona**: PhD Researcher in Computational Biology
- **Job**: "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"

### Test Case 2: Business Analysis
- **Documents**: 3 annual reports from competing tech companies (2022-2024)
- **Persona**: Investment Analyst
- **Job**: "Analyze revenue trends, R&D investments, and market positioning strategies"

### Test Case 3: Educational Content
- **Documents**: 5 chapters from organic chemistry textbooks
- **Persona**: Undergraduate Chemistry Student
- **Job**: "Identify key concepts and mechanisms for exam preparation on reaction kinetics"

## Technical Specifications

### Constraints Met
- ✅ **CPU Only**: No GPU required, optimized for CPU execution
- ✅ **Model Size ≤ 1GB**: Uses all-MiniLM-L6-v2 (~90MB)
- ✅ **Processing Time ≤ 60 seconds**: Optimized for 3-5 documents
- ✅ **No Internet Access**: Models pre-downloaded and cached

### Ranking Methodology
1. **Semantic Similarity (40%)**: Sentence transformer-based content relevance
2. **Keyword Relevance (30%)**: Domain-specific terminology matching
3. **Position Importance (20%)**: Document structure and page hierarchy
4. **Content Quality (10%)**: Technical depth and actionable information

### Persona-Specific Scoring
- **Research**: Methodology, analysis, data, results, conclusions
- **Business**: Compliance, risk, management, procedures, policies
- **Education**: Curriculum, assessment, learning, teaching, evaluation

## File Structure
```
Adobe-Deepdoc-round1b--main/
├── input/
│   ├── persona.json
│   └── *.pdf (your documents)
├── output/
│   └── challenge1b_output.json
├── extractor_1b.py          # Main application
├── heading_utils.py         # Document parsing utilities
├── semantic_utils.py        # Ranking and similarity functions
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── approach_explanation.md # Methodology explanation
└── README.md              # This file
```

## Troubleshooting

### Common Issues
1. **Model Download**: First run may take time to download the model (~90MB)
2. **Memory Issues**: Ensure sufficient RAM for document processing
3. **PDF Compatibility**: Some PDFs may require additional fonts or encoding

### Performance Tips
1. Use SSD storage for faster document processing
2. Limit document size to optimize processing time
3. Ensure PDFs are text-based (not scanned images)

## Scoring Criteria
- **Section Relevance (60 points)**: How well selected sections match persona + job requirements
- **Sub-Section Relevance (40 points)**: Quality of granular subsection analysis

The system is designed to maximize both criteria through intelligent content extraction and persona-aware ranking algorithms.
