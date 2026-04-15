import re
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MedicalEntity:
    text: str
    label: str       # DISEASE, SYMPTOM, TREATMENT, MEDICATION, ANATOMY, TEST
    start: int = 0
    end: int = 0
    confidence: float = 1.0


# ── Medical Vocabulary Dictionaries ──────────────────────────────────────────

DISEASES = {
    # Cardiovascular
    "heart disease", "coronary artery disease", "heart failure", "arrhythmia",
    "atrial fibrillation", "heart attack", "myocardial infarction", "stroke",
    "hypertension", "high blood pressure", "atherosclerosis", "angina",
    "cardiomyopathy", "pericarditis", "endocarditis",
    # Metabolic
    "diabetes", "type 1 diabetes", "type 2 diabetes", "obesity",
    "hyperlipidemia", "high cholesterol", "metabolic syndrome", "thyroid disease",
    "hyperthyroidism", "hypothyroidism", "cushing syndrome",
    # Respiratory
    "asthma", "copd", "chronic obstructive pulmonary disease", "pneumonia",
    "bronchitis", "emphysema", "pulmonary fibrosis", "lung cancer",
    "tuberculosis", "covid-19", "influenza", "sleep apnea",
    # Neurological
    "alzheimer", "alzheimer's disease", "parkinson", "parkinson's disease",
    "multiple sclerosis", "epilepsy", "migraine", "dementia", "stroke",
    "neuropathy", "meningitis", "encephalitis", "brain tumor",
    # Mental Health
    "depression", "anxiety", "schizophrenia", "bipolar disorder",
    "ptsd", "ocd", "adhd", "autism", "eating disorder",
    # Cancer
    "cancer", "tumor", "leukemia", "lymphoma", "melanoma",
    "breast cancer", "prostate cancer", "colon cancer", "lung cancer",
    "ovarian cancer", "cervical cancer", "pancreatic cancer",
    # Musculoskeletal
    "arthritis", "osteoarthritis", "rheumatoid arthritis", "osteoporosis",
    "fibromyalgia", "lupus", "gout", "scoliosis", "back pain",
    # Gastrointestinal
    "crohn's disease", "ulcerative colitis", "ibs", "irritable bowel syndrome",
    "celiac disease", "gastritis", "peptic ulcer", "acid reflux", "gerd",
    "hepatitis", "cirrhosis", "pancreatitis", "appendicitis",
    # Infectious
    "hiv", "aids", "hepatitis b", "hepatitis c", "lyme disease",
    "malaria", "pneumonia", "urinary tract infection", "uti",
    # Other
    "anemia", "kidney disease", "chronic kidney disease", "renal failure",
    "glaucoma", "cataracts", "macular degeneration", "psoriasis", "eczema",
    "allergies", "asthma", "fibromyalgia", "endometriosis",
}

SYMPTOMS = {
    # General
    "fever", "fatigue", "tiredness", "weakness", "weight loss", "weight gain",
    "night sweats", "chills", "loss of appetite", "nausea", "vomiting",
    "diarrhea", "constipation", "bloating",
    # Pain
    "pain", "chest pain", "abdominal pain", "back pain", "headache",
    "joint pain", "muscle pain", "pelvic pain", "neck pain", "stomach pain",
    # Respiratory
    "cough", "shortness of breath", "difficulty breathing", "wheezing",
    "sore throat", "runny nose", "congestion", "sneezing",
    # Neurological
    "dizziness", "vertigo", "confusion", "memory loss", "tremors",
    "numbness", "tingling", "seizures", "fainting", "blurred vision",
    # Cardiovascular
    "palpitations", "irregular heartbeat", "swelling", "edema",
    "rapid heartbeat", "slow heartbeat",
    # Skin
    "rash", "itching", "hives", "jaundice", "pale skin", "bruising",
    # Urinary
    "frequent urination", "painful urination", "blood in urine", "incontinence",
    # Digestive
    "heartburn", "indigestion", "difficulty swallowing", "blood in stool",
    # Mental
    "depression", "anxiety", "mood swings", "irritability", "insomnia",
    "trouble sleeping", "hallucinations",
}

TREATMENTS = {
    # Surgery
    "surgery", "surgical procedure", "operation", "transplant", "bypass surgery",
    "angioplasty", "appendectomy", "mastectomy", "colostomy",
    # Therapy types
    "chemotherapy", "radiation therapy", "radiotherapy", "immunotherapy",
    "targeted therapy", "hormone therapy", "gene therapy", "stem cell transplant",
    "dialysis", "physical therapy", "occupational therapy", "speech therapy",
    "psychotherapy", "cognitive behavioral therapy", "cbt", "behavioral therapy",
    # General
    "treatment", "therapy", "medication", "diet", "exercise", "lifestyle changes",
    "rehabilitation", "palliative care", "blood transfusion",
    # Specific
    "insulin therapy", "oxygen therapy", "phototherapy", "electrotherapy",
    "hydrotherapy", "acupuncture", "chiropractic",
}

MEDICATIONS = {
    # Drug classes
    "antibiotic", "antiviral", "antifungal", "antihistamine", "analgesic",
    "anti-inflammatory", "nsaid", "steroid", "corticosteroid",
    "antidepressant", "antipsychotic", "anxiolytic", "sedative",
    "diuretic", "beta-blocker", "ace inhibitor", "arb", "statin",
    "calcium channel blocker", "anticoagulant", "blood thinner",
    "antihypertensive", "bronchodilator", "insulin", "metformin",
    "ssri", "snri", "maoi", "tca",
    # Common drugs
    "aspirin", "ibuprofen", "acetaminophen", "paracetamol", "morphine",
    "penicillin", "amoxicillin", "metformin", "lisinopril", "atorvastatin",
    "omeprazole", "warfarin", "prednisone", "levothyroxine",
    # Vaccine
    "vaccine", "vaccination", "immunization",
}

ANATOMY = {
    "heart", "lungs", "liver", "kidney", "kidneys", "brain", "stomach",
    "intestine", "colon", "pancreas", "thyroid", "adrenal gland", "spleen",
    "bladder", "uterus", "ovaries", "prostate", "testes", "bone marrow",
    "lymph node", "lymph nodes", "blood vessel", "artery", "vein", "capillary",
    "muscle", "bone", "joint", "spine", "skin", "nerve", "neuron",
    "immune system", "respiratory system", "digestive system",
    "cardiovascular system", "nervous system", "endocrine system",
}

MEDICAL_TESTS = {
    "blood test", "urine test", "mri", "ct scan", "x-ray", "ultrasound",
    "echocardiogram", "electrocardiogram", "ekg", "ecg", "biopsy",
    "colonoscopy", "endoscopy", "mammogram", "pap smear", "bone density",
    "glucose test", "cholesterol test", "complete blood count", "cbc",
    "liver function test", "kidney function test", "thyroid test",
    "genetic test", "allergy test", "stress test", "pulmonary function test",
}

# Label → color for UI display
LABEL_COLORS = {
    "DISEASE":    "#ff6b6b",
    "SYMPTOM":    "#ffa94d",
    "TREATMENT":  "#69db7c",
    "MEDICATION": "#74c0fc",
    "ANATOMY":    "#da77f2",
    "TEST":       "#ffd43b",
}

LABEL_ICONS = {
    "DISEASE":    "🦠",
    "SYMPTOM":    "⚠️",
    "TREATMENT":  "💊",
    "MEDICATION": "💉",
    "ANATOMY":    "🫀",
    "TEST":       "🔬",
}


class MedicalEntityRecognizer:
    """Rule-based medical entity recognizer using curated vocabulary."""

    def __init__(self):
        # Compile sorted (longest-first) keyword lists for greedy matching
        self._vocab: Dict[str, List[str]] = {
            "DISEASE":    sorted(DISEASES,    key=len, reverse=True),
            "SYMPTOM":    sorted(SYMPTOMS,    key=len, reverse=True),
            "TREATMENT":  sorted(TREATMENTS,  key=len, reverse=True),
            "MEDICATION": sorted(MEDICATIONS, key=len, reverse=True),
            "ANATOMY":    sorted(ANATOMY,     key=len, reverse=True),
            "TEST":       sorted(MEDICAL_TESTS, key=len, reverse=True),
        }
        # Pre-compile regex patterns
        self._patterns: Dict[str, List[re.Pattern]] = {}
        for label, terms in self._vocab.items():
            self._patterns[label] = [
                re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
                for term in terms
            ]

    def recognize(self, text: str) -> List[MedicalEntity]:
        """Extract medical entities from text."""
        entities: List[MedicalEntity] = []
        covered = set()   # character positions already matched

        for label, patterns in self._patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    start, end = match.start(), match.end()
                    span = set(range(start, end))
                    if not span & covered:
                        entities.append(MedicalEntity(
                            text=match.group(),
                            label=label,
                            start=start,
                            end=end,
                        ))
                        covered |= span

        return sorted(entities, key=lambda e: e.start)

    def annotate_html(self, text: str) -> str:
        """Return HTML string with entity spans highlighted."""
        entities = self.recognize(text)
        if not entities:
            return text

        result = []
        prev = 0
        for ent in entities:
            result.append(text[prev:ent.start])
            color = LABEL_COLORS.get(ent.label, "#ccc")
            icon  = LABEL_ICONS.get(ent.label, "")
            result.append(
                f'<mark style="background:{color}20;border:1px solid {color};'
                f'border-radius:3px;padding:1px 4px;font-weight:600;" '
                f'title="{ent.label}">{icon} {ent.text}</mark>'
            )
            prev = ent.end
        result.append(text[prev:])
        return "".join(result)

    def get_entity_summary(self, text: str) -> Dict[str, List[str]]:
        """Return a dict mapping label → list of matched entity texts."""
        summary: Dict[str, List[str]] = {}
        for ent in self.recognize(text):
            summary.setdefault(ent.label, [])
            if ent.text not in summary[ent.label]:
                summary[ent.label].append(ent.text)
        return summary

    @staticmethod
    def get_label_colors() -> Dict[str, str]:
        return LABEL_COLORS

    @staticmethod
    def get_label_icons() -> Dict[str, str]:
        return LABEL_ICONS