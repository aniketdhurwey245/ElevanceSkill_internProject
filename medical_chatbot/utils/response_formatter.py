
from typing import List, Optional
from utils.retrieval_engine import RetrievalResult


DISCLAIMER = (
    "⚕️ *Medical Disclaimer: This information is for educational purposes only "
    "and does not constitute medical advice. Always consult a qualified healthcare "
    "professional for diagnosis, treatment, or medical decisions.*"
)

CONFIDENCE_LABELS = [
    (0.5, "🟢 High confidence", "The following answer closely matches your question."),
    (0.25, "🟡 Moderate confidence", "This answer may be related to your question."),
    (0.0,  "🔴 Low confidence",
     "I couldn't find a closely matching answer. Here's the best available result."),
]

NO_RESULT_MSG = (
    "I'm sorry, I couldn't find relevant information for your question in the "
    "MedQuAD dataset. Please try rephrasing your question or asking about a "
    "specific disease, symptom, or treatment. For medical concerns, always "
    "consult a healthcare professional."
)

SUGGESTED_TOPICS = [
    "What is diabetes?",
    "Symptoms of hypertension",
    "How is asthma treated?",
    "What causes depression?",
    "Alzheimer's disease information",
    "Heart disease treatment",
    "Cancer types and treatments",
    "COVID-19 symptoms",
]


def _confidence_tier(score: float):
    for threshold, label, message in CONFIDENCE_LABELS:
        if score >= threshold:
            return label, message
    return CONFIDENCE_LABELS[-1][1], CONFIDENCE_LABELS[-1][2]


def format_primary_response(results: List[RetrievalResult]) -> dict:
    """
    Format the primary chatbot response.
    Returns a dict with keys: answer, metadata, confidence_label,
    confidence_message, show_disclaimer, sources.
    """
    if not results:
        return {
            "answer": NO_RESULT_MSG,
            "metadata": None,
            "confidence_label": "❓ No results",
            "confidence_message": "No relevant results found.",
            "show_disclaimer": False,
            "sources": [],
        }

    top = results[0]
    conf_label, conf_msg = _confidence_tier(top.score)

    # Build metadata badge string
    badges = []
    if top.focus and top.focus.lower() not in ("general", "unknown", "nan"):
        badges.append(f"🏥 **Topic:** {top.focus}")
    if top.question_type and top.question_type.lower() not in ("general", "nan"):
        badges.append(f"📋 **Type:** {top.question_type.title()}")
    if top.source:
        badges.append(f"📚 **Source:** {top.source}")

    return {
        "answer": top.answer,
        "matched_question": top.question,
        "metadata": " &nbsp;|&nbsp; ".join(badges),
        "confidence_label": conf_label,
        "confidence_message": conf_msg,
        "confidence_score": round(top.score * 100, 1),
        "show_disclaimer": True,
        "disclaimer": DISCLAIMER,
        "sources": results,
    }


def format_alternative_results(results: List[RetrievalResult]) -> List[dict]:
    """Format secondary results for display in an expander."""
    formatted = []
    for r in results[1:]:
        conf_label, _ = _confidence_tier(r.score)
        formatted.append({
            "rank": r.rank,
            "question": r.question,
            "answer": r.answer[:400] + ("..." if len(r.answer) > 400 else ""),
            "focus": r.focus,
            "score": round(r.score * 100, 1),
            "confidence_label": conf_label,
        })
    return formatted


def get_suggested_topics() -> List[str]:
    return SUGGESTED_TOPICS