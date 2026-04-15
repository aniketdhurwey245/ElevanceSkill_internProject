# 🩺 MedChat — Medical Q&A Chatbot (MedQuAD)

A specialized medical question-answering chatbot powered by the
[MedQuAD dataset](https://github.com/abachaa/MedQuAD) with TF-IDF retrieval,
rule-based medical entity recognition, and a polished Streamlit UI.

---

## 📁 Project Structure

```
medical_chatbot/
├── app.py                        # Streamlit main application
├── requirements.txt              # Python dependencies
├── README.md
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py            # MedQuAD GitHub fetcher + XML parser
│   ├── retrieval_engine.py       # TF-IDF retrieval with cosine similarity
│   ├── entity_recognizer.py      # Rule-based medical NER
│   └── response_formatter.py     # Answer formatting & confidence scoring
│
└── data/


## ✨ Features

| Feature | Details |
|---|---|
| **Data Source** | MedQuAD: 47,457 QA pairs from 12 NIH websites |
| **Retrieval** | TF-IDF + cosine similarity with keyword boosting |
| **Entity Recognition** | Diseases, Symptoms, Treatments, Medications, Anatomy, Tests |
| **Confidence Scoring** | High / Moderate / Low with percentage display |
| **Question Type Filter** | Information, Symptoms, Treatment, Causes, Diagnosis, Prevention |
| **UI** | Dark-themed Streamlit with chat bubbles, entity highlighting |
| **Caching** | GitHub data + TF-IDF index cached locally for speed |
| **Fallback** | 26 built-in sample QA pairs if GitHub is unavailable |

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 🔧 How It Works

### Data Pipeline
```
GitHub (MedQuAD XML) ──► XML Parser ──► DataFrame ──► JSON Cache
                                                           │
                                                           ▼
                                                     TF-IDF Index ──► PKL Cache
```

### Query Flow
```
User Query
    │
    ▼
Medical Entity Recognition (NER)
    │
    ▼
TF-IDF Vectorization + Cosine Similarity
    │
    ▼
Keyword Boosting (topic + question type)
    │
    ▼
Top-K Retrieval + Confidence Scoring
    │
    ▼
Formatted Response with Entity Highlighting
```

### Entity Recognition Categories
| Label | Examples |
|---|---|
|  DISEASE | diabetes, hypertension, asthma, cancer |
|  SYMPTOM | fever, chest pain, shortness of breath |
|  TREATMENT | chemotherapy, surgery, physical therapy |
|  MEDICATION | insulin, metformin, antibiotics, SSRIs |
|  ANATOMY | heart, lungs, liver, nervous system |
| TEST | MRI, blood test, biopsy, ECG |

---

##  Dataset

**MedQuAD** (Medical Question Answer Dataset) by Ben Abacha & Demner-Fushman:

| Source | Description |
|---|---|
| CancerGov | Cancer-related QA |
| GARD | Rare disease information |
| GHR | Genetics home reference |
| MedlinePlus | General medical info |
| NIDDK | Digestive & kidney diseases |
| NINDS | Neurological disorders |
| SeniorHealth | Senior health topics |
| NHLBI | Heart, lung, blood topics |
| CDC | Public health & prevention |
| MedlinePlus Drugs | Drug information |

---

##  Medical Disclaimer

> This chatbot is for **educational purposes only** and does not constitute
> medical advice, diagnosis, or treatment. Always consult a qualified
> healthcare professional for any medical concerns.

---

##  Key Dependencies

| Package | Version | Purpose |
|---|---|---|
| streamlit | 1.32.0 | Web UI |
| scikit-learn | 1.4.1 | TF-IDF vectorization |
| pandas | 2.2.1 | Data handling |
| numpy | 1.26.4 | Numerical ops |
| requests | 2.31.0 | GitHub API fetch |
| beautifulsoup4 | 4.12.3 | HTML parsing |

---

##  Example Questions

- "What is diabetes?"
- "Symptoms of hypertension"
- "How is asthma treated?"
- "What causes Alzheimer's disease?"
- "How to prevent heart disease?"
- "What medications are used for depression?"
- "What are the signs of a stroke?"