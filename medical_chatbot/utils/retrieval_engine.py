
import re
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ───────────────────────────────────────────────────────────────
# DATA CLASS
# ───────────────────────────────────────────────────────────────

@dataclass
class RetrievalResult:
    question: str
    answer: str
    focus: str
    question_type: str
    source: str
    score: float
    rank: int


#
# TEXT CLEANING
# 

def _clean_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)

    abbrevs = {
        r'\bdiab\b': 'diabetes',
        r'\bhtn\b': 'hypertension',
        r'\bchf\b': 'congestive heart failure',
        r'\bcopd\b': 'chronic obstructive pulmonary disease',
        r'\bca\b': 'cancer',
        r'\bms\b': 'multiple sclerosis',
        r'\bad\b': "alzheimer's disease",
        r'\bra\b': 'rheumatoid arthritis',
        r'\bibd\b': 'inflammatory bowel disease',
        r'\bibs\b': 'irritable bowel syndrome',
        r'\bgerd\b': 'gastroesophageal reflux disease',
        r'\buti\b': 'urinary tract infection',
        r'\bmi\b': 'myocardial infarction',
        r'\bcvd\b': 'cardiovascular disease',
    }

    for pattern, replacement in abbrevs.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text



# RETRIEVER CLASS


class MedicalQARetriever:

    MEDICAL_BOOST_TERMS = [
        'symptom', 'symptoms', 'treatment', 'treatments',
        'cause', 'causes', 'diagnosis', 'prevent', 'medication',
        'therapy', 'cure', 'risk', 'complication'
    ]

    def __init__(self, index_path: str = "data/retrieval_index.pkl"):
        self.index_path = Path(index_path)
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self.df: Optional[pd.DataFrame] = None
        self.is_built = False

    
    # BUILD INDEX

    def build_index(self, df: pd.DataFrame, save: bool = True) -> None:
        self.df = df.copy().reset_index(drop=True)

        combined_texts = []
        for _, row in df.iterrows():
            q = _clean_text(str(row.get("question", "")))
            focus = _clean_text(str(row.get("focus", "")))

            # Boost focus importance
            combined = f"{q} {focus} {focus} {focus}"
            combined_texts.append(combined)

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=50000,
            stop_words="english",
            sublinear_tf=True,
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(combined_texts)
        self.is_built = True

        if save:
            self._save_index()


    # RETRIEVE

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        question_type_filter: Optional[str] = None
    ) -> List[RetrievalResult]:

        if not self.is_built:
            return []

        clean_query = _clean_text(query)

        query_vec = self.vectorizer.transform([clean_query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Apply boosting
        scores = self._apply_keyword_boost(query, scores)

        # Filter by question type
        if question_type_filter and "type" in self.df.columns:
            mask = self.df["type"].str.lower() == question_type_filter.lower()
            scores[~mask.values] *= 0.3

        # Sort indices
        top_indices = np.argsort(scores)[::-1][:top_k * 3]

        results = []
        seen_answers = set()

        for idx in top_indices:
            if scores[idx] < 0.05:   # threshold
                continue

            row = self.df.iloc[idx]
            answer = str(row.get("answer", ""))

            # Remove duplicate answers
            if answer[:100] in seen_answers:
                continue

            seen_answers.add(answer[:100])

            results.append(RetrievalResult(
                question=str(row.get("question", "")),
                answer=answer,
                focus=str(row.get("focus", "")),
                question_type=str(row.get("type", "")),
                source=str(row.get("source", "")),
                score=float(scores[idx]),
                rank=len(results) + 1,
            ))

            if len(results) >= top_k:
                break

        #  NEW: Add diversity (random pick among top results)
        if len(results) > 2:
            top_candidates = results[:3]
            best = random.choice(top_candidates)

            # Move selected result to top
            results.remove(best)
            results.insert(0, best)

        return results

    #BOOSTING
    def _apply_keyword_boost(self, query: str, scores: np.ndarray) -> np.ndarray:
        query_lower = query.lower()
        boost = np.zeros(len(scores))

        # Boost by focus matching
        if self.df is not None and "focus" in self.df.columns:
            for i, focus in enumerate(self.df["focus"]):
                if str(focus).lower() in query_lower:
                    boost[i] += 0.2

        # Boost by intent
        intent_map = {
            "symptom": ["symptom", "sign"],
            "treatment": ["treat", "therapy", "medicine"],
            "cause": ["cause", "why"],
            "diagnosis": ["test", "diagnose"],
        }

        for intent, keywords in intent_map.items():
            if any(k in query_lower for k in keywords):
                mask = self.df["type"].str.lower() == intent
                boost[mask.values] += 0.1

        return scores + boost

    
    # SAVE / LOAD


    def _save_index(self):
        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.index_path, "wb") as f:
            pickle.dump({
                "vectorizer": self.vectorizer,
                "tfidf_matrix": self.tfidf_matrix,
                "df": self.df,
            }, f)

    def load_index(self) -> bool:
        if not self.index_path.exists():
            return False

        try:
            with open(self.index_path, "rb") as f:
                data = pickle.load(f)

            self.vectorizer = data["vectorizer"]
            self.tfidf_matrix = data["tfidf_matrix"]
            self.df = data["df"]
            self.is_built = True
            return True

        except Exception:
            return False

    
    # STATS
     

    def get_index_stats(self) -> Dict:
        if not self.is_built:
            return {}

        return {
            "total_documents": len(self.df),
            "vocab_size": len(self.vectorizer.vocabulary_),
        }