# Log Classification System

A multi-modal log classification system that uses regex patterns, BERT embeddings, and LLM-based processing to automatically categorize system logs from multiple sources.

## Project Overview

This project implements a hybrid log classification pipeline that intelligently routes logs through different classifiers based on their source:

- **Legacy Systems (LegacyCRM)**: Uses Groq LLM for complex semantic understanding
- **Modern Systems**: Uses regex patterns first, falls back to BERT embeddings for unmatched logs

## Directory Structure

```
project1/
├── training/
│   ├── classify.py              # Main classification pipeline
│   ├── processorllm.py          # Groq LLM processor
│   ├── processorbert.py         # BERT embedding processor
│   ├── regex.py                 # Regex pattern classifier
│   ├── server.py                # FastAPI server for REST API
│   ├── training.ipynb           # Data exploration & clustering analysis
│   └── dataset/
│       └── synthetic_logs.csv   # Synthetic log dataset
├── models/
│   └── log_classifier.pkl       # Trained BERT classifier model
├── processor_llm.py             # LLM integration example
└── README.md
```

## Features

### 1. **Regex-Based Classification**
Pattern matching for known log formats with immediate categorization

### 2. **BERT Embeddings (Sentence Transformers)**
- Uses `all-MiniLM-L6-v2` model for semantic similarity
- Fallback mechanism for logs unmatched by regex
- Trained classifier model stored in `models/log_classifier.pkl`

### 3. **LLM Processing**
- Groq API integration for complex log analysis
- Best-in-class understanding for ambiguous or legacy system logs
- Uses `llama-3.3-70b-versatile` model

### 4. **DBSCAN Clustering**
Unsupervised clustering analysis of log embeddings for pattern discovery

## Installation

### Prerequisites
- Python 3.11+
- pip

### Setup

1. Install dependencies:
```bash
pip install sentence-transformers joblib pandas groq python-dotenv scikit-learn fastapi uvicorn
```

2. Create `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
```

3. Ensure the trained model is in place:
```
models/log_classifier.pkl
```

## Usage

### REST API Server

Start the FastAPI server:
```bash
cd training
uvicorn server:app --reload
```

The server runs on `http://localhost:8000`

#### API Endpoint: POST `/classify-logs/`

Upload a CSV file with log data and get predictions:

```bash
curl -X POST http://localhost:8000/classify-logs/ \
  -F "file=@input.csv"
```

**Request**: Form-data with CSV file containing `source` and `log_message` columns

**Response**: CSV file with added `target_label` column

**Example Input:**
```csv
source,log_message
LegacyCRM,Password reset requested by user User789
Billing System,User User123 logged in
Modern CRM,System updated to version 2.1.0
```

**Example Output:**
```csv
source,log_message,target_label
LegacyCRM,Password reset requested by user User789,User Action
Billing System,User User123 logged in,User Action
Modern CRM,System updated to version 2.1.0,System Update
```

#### Error Handling
- Returns `400` if file is not CSV or missing required columns
- Returns `500` if processing fails

### Classify logs from CSV

```python
from training.classify import classify_csv

classify_csv("path/to/input.csv")
```

Input CSV format:
```
source,log_message
LegacyCRM,Password reset requested by user User789
Billing System,User User123 logged in
Modern CRM,System updated to version 2.1.0
```

Output: `output.csv` with added `target_label` column

### Classify individual logs

```python
from training.classify import classify_log

label = classify_log("LegacyCRM", "Backup started at 2024-06-01 10:00:00")
print(label)  # Output: appropriate classification
```

### Using specific classifiers

```python
from training.regex import classify_with_regex
from training.processorbert import classify_with_bert
from training.processorllm import classify_with_llm

# Regex classification
label = classify_with_regex("User User123 logged in")

# BERT classification
label = classify_with_bert("Some log message")

# LLM classification
label = classify_with_llm("Complex legacy system log")
```

## Classification Logic

```
Input Log
    ↓
Source == "LegacyCRM"?
    ├─ YES → Use LLM (Groq)
    └─ NO  → Use Regex Pattern
            ↓
        Pattern Found?
            ├─ YES → Return regex label
            └─ NO  → Use BERT embeddings → Return predicted class
```

## Supported Log Categories

- **User Action**: Login, logout, account creation
- **System Notification**: Backup operations, disk cleanup
- **System Update**: Version updates, patches
- **File Operation**: Upload, download, deletion
- **System Reboot**: Reboot initiations
- **System Maintenance**: Maintenance tasks

## Model Details

### BERT Model
- **Name**: `all-MiniLM-L6-v2`
- **Type**: Sentence Transformer
- **Dimensions**: 384-dimensional embeddings
- **Training Data**: Synthetic logs from `dataset/synthetic_logs.csv`

### LLM Model
- **Provider**: Groq
- **Model**: `llama-3.3-70b-versatile`
- **Use Case**: Complex legacy system logs

## Data Processing Pipeline

1. **Data Exploration** (`training.ipynb`):
   - Load synthetic log dataset
   - Generate embeddings using BERT
   - Cluster logs using DBSCAN (eps=0.2, metric='cosine')
   - Analyze cluster patterns

2. **Model Training**:
   - Train classifier on embedded vectors
   - Save model to `models/log_classifier.pkl`

3. **Inference**:
   - Classify new logs through multi-stage pipeline
   - Output structured CSV with predictions

## Configuration

### Environment Variables
```bash
GROQ_API_KEY=your_groq_api_key  # Required for LLM processing
```

### Hyperparameters (DBSCAN)
- `eps`: 0.2 (epsilon parameter)
- `min_samples`: 1
- `metric`: cosine distance

## Output Format

```csv
source,log_message,target_label
Billing System,User User123 logged in,User Action
Modern CRM,System updated to version 2.1.0,System Update
LegacyCRM,Backup started at 2024-06-01 10:00:00,System Notification
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| sentence-transformers | Latest | BERT embeddings |
| scikit-learn | Latest | ML utilities |
| pandas | Latest | Data manipulation |
| joblib | Latest | Model serialization |
| groq | Latest | LLM API access |
| python-dotenv | Latest | Environment configuration || fastapi | Latest | REST API framework |
| uvicorn | Latest | ASGI server |
## Troubleshooting

### Missing GROQ_API_KEY
Ensure `.env` file exists with valid API key, or set environment variable:
```bash
$env:GROQ_API_KEY="your_key"  # PowerShell
export GROQ_API_KEY="your_key"  # Linux/Mac
```

### Model Not Found
Retrain the model or ensure `models/log_classifier.pkl` exists in the project root.

### Import Errors
Verify all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Future Enhancements

- [ ] Fine-tune BERT on domain-specific logs
- [ ] Add more regex patterns for emerging log types
- [ ] Implement confidence scores for predictions
- [ ] Add streaming log processing
- [ ] Create REST API endpoint for log classification

## Author

Rashi Kaushik (Resume Project)

## License

Educational Project
