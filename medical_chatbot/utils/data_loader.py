"""
data_loader.py - MedQuAD Dataset Loader and Parser
Fetches and parses XML files from the MedQuAD GitHub repository
"""

import os
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import json
from pathlib import Path
import time

# MedQuAD GitHub raw content base URL
MEDQUAD_BASE_URL = "https://raw.githubusercontent.com/abachaa/MedQuAD/master"

# Key MedQuAD folders (subset for faster loading)
MEDQUAD_FOLDERS = [
    "1_CancerGov_QA",
    "2_GARD_QA", 
    "3_GHR_QA",
    "4_MedlineplusGov_QA",
    "5_NIDDK_QA",
    "6_NINDS_QA",
    "7_SeniorHealth_QA",
    "8_NHLBI_QA",
    "9_CDC_QA",
    "10_MedlineplusDrugs_QA"
]

# Fallback embedded sample data (used if GitHub fetch fails)
SAMPLE_QA_DATA = [
    {
        "question": "What is diabetes?",
        "answer": "Diabetes is a chronic disease that occurs when the pancreas is no longer able to make insulin, or when the body cannot make good use of the insulin it produces. Insulin is a hormone made by the pancreas that acts like a key to let glucose from the food we eat pass from the blood stream into the cells in the body to produce energy.",
        "focus": "Diabetes",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "What are the symptoms of diabetes?",
        "answer": "Common symptoms of diabetes include: frequent urination, excessive thirst, unexplained weight loss, extreme hunger, sudden vision changes, tingling or numbness in hands or feet, feeling very tired, very dry skin, sores that are slow to heal, and more infections than usual.",
        "focus": "Diabetes",
        "type": "Symptoms",
        "source": "Sample"
    },
    {
        "question": "How is diabetes treated?",
        "answer": "Diabetes treatment includes lifestyle changes such as healthy eating, physical activity, and weight management. Medical treatments include oral medications for type 2 diabetes, insulin therapy (especially for type 1 diabetes), and blood sugar monitoring. Regular check-ups to monitor for complications are also essential.",
        "focus": "Diabetes",
        "type": "Treatment",
        "source": "Sample"
    },
    {
        "question": "What is hypertension?",
        "answer": "Hypertension, or high blood pressure, is a common condition where the long-term force of the blood against your artery walls is high enough that it may eventually cause health problems, such as heart disease. Blood pressure is determined both by the amount of blood your heart pumps and the amount of resistance to blood flow in your arteries.",
        "focus": "Hypertension",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "What are symptoms of hypertension?",
        "answer": "Most people with high blood pressure have no signs or symptoms, even if blood pressure readings reach dangerously high levels. Some people may have headaches, shortness of breath or nosebleeds, but these signs and symptoms aren't specific and usually don't occur until blood pressure has reached a severe or life-threatening stage.",
        "focus": "Hypertension",
        "type": "Symptoms",
        "source": "Sample"
    },
    {
        "question": "How is hypertension treated?",
        "answer": "High blood pressure treatment includes lifestyle modifications like DASH diet, reduced sodium intake, regular physical activity, limiting alcohol, and not smoking. Medications include diuretics, ACE inhibitors, angiotensin II receptor blockers (ARBs), calcium channel blockers, and beta-blockers.",
        "focus": "Hypertension",
        "type": "Treatment",
        "source": "Sample"
    },
    {
        "question": "What is asthma?",
        "answer": "Asthma is a condition in which your airways narrow and swell and may produce extra mucus. This can make breathing difficult and trigger coughing, a whistling sound (wheezing) when you breathe out and shortness of breath. For some people, asthma is a minor nuisance. For others, it can be a major problem that interferes with daily activities.",
        "focus": "Asthma",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "What are the symptoms of asthma?",
        "answer": "Asthma symptoms include shortness of breath, chest tightness or pain, wheezing when exhaling, trouble sleeping caused by shortness of breath, coughing or wheezing attacks that are worsened by a respiratory virus such as cold or flu.",
        "focus": "Asthma",
        "type": "Symptoms",
        "source": "Sample"
    },
    {
        "question": "What causes asthma?",
        "answer": "The exact cause of asthma is not known, but it's thought to be a combination of genetic and environmental factors. Triggers include airborne allergens (pollen, dust, pet dander), respiratory infections, physical activity, cold air, air pollutants, certain medications, stress, and sulfites in foods.",
        "focus": "Asthma",
        "type": "Causes",
        "source": "Sample"
    },
    {
        "question": "What is Alzheimer's disease?",
        "answer": "Alzheimer's disease is a progressive neurologic disorder that causes the brain to shrink (atrophy) and brain cells to die. Alzheimer's disease is the most common cause of dementia — a continuous decline in thinking, behavioral and social skills that affects a person's ability to function independently.",
        "focus": "Alzheimer's disease",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "What are early signs of Alzheimer's disease?",
        "answer": "Early signs of Alzheimer's include memory loss that disrupts daily life, challenges in planning or solving problems, difficulty completing familiar tasks, confusion with time or place, trouble understanding visual images, new problems with words in speaking or writing, misplacing things, decreased or poor judgment, withdrawal from social activities, and changes in mood and personality.",
        "focus": "Alzheimer's disease",
        "type": "Symptoms",
        "source": "Sample"
    },
    {
        "question": "What is cancer?",
        "answer": "Cancer is a disease in which some of the body's cells grow uncontrollably and spread to other parts of the body. Cancer can start almost anywhere in the human body, which is made up of trillions of cells. Normally, human cells grow and multiply through a process called cell division to form new cells as the body needs them.",
        "focus": "Cancer",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "What are the treatments for cancer?",
        "answer": "Cancer treatments include surgery to remove tumors, radiation therapy using high-energy rays, chemotherapy using drugs to kill cancer cells, immunotherapy to help the immune system fight cancer, targeted therapy attacking specific cancer cell features, hormone therapy, stem cell transplants, and precision medicine based on genetic makeup.",
        "focus": "Cancer",
        "type": "Treatment",
        "source": "Sample"
    },
    {
        "question": "What is depression?",
        "answer": "Depression (major depressive disorder) is a common and serious medical illness that negatively affects how you feel, the way you think and how you act. Depression causes feelings of sadness and/or a loss of interest in activities you once enjoyed. It can lead to a variety of emotional and physical problems.",
        "focus": "Depression",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "What are symptoms of depression?",
        "answer": "Symptoms of depression include persistent sad, anxious, or 'empty' mood, feelings of hopelessness or pessimism, irritability, feelings of guilt, worthlessness, or helplessness, loss of interest in hobbies and activities, decreased energy or fatigue, difficulty concentrating or making decisions, difficulty sleeping, appetite and weight changes, and thoughts of death or suicide.",
        "focus": "Depression",
        "type": "Symptoms",
        "source": "Sample"
    },
    {
        "question": "How is depression treated?",
        "answer": "Depression is treated with psychotherapy (talk therapy) such as cognitive behavioral therapy (CBT), medications including antidepressants (SSRIs, SNRIs, TCAs, MAOIs), or a combination of both. Brain stimulation therapies like electroconvulsive therapy (ECT) may be used for severe cases. Lifestyle changes including exercise, proper sleep, and social support are also important.",
        "focus": "Depression",
        "type": "Treatment",
        "source": "Sample"
    },
    {
        "question": "What is arthritis?",
        "answer": "Arthritis is inflammation of one or more joints, causing pain and stiffness that can worsen with age. The most common types of arthritis are osteoarthritis and rheumatoid arthritis. Osteoarthritis causes cartilage to break down, while rheumatoid arthritis is an autoimmune disorder that first targets the joint lining.",
        "focus": "Arthritis",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "What are symptoms of arthritis?",
        "answer": "The most common signs and symptoms of arthritis involve the joints including pain, stiffness, swelling, redness, and decreased range of motion. Symptoms may come and go, and can be mild, moderate, or severe. They may stay about the same for years but can progress or get worse over time.",
        "focus": "Arthritis",
        "type": "Symptoms",
        "source": "Sample"
    },
    {
        "question": "What is COVID-19?",
        "answer": "COVID-19 is an infectious disease caused by the SARS-CoV-2 virus. Most people who fall sick with COVID-19 will experience mild to moderate symptoms and recover without special treatment. However, some will become seriously ill and require medical attention.",
        "focus": "COVID-19",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "What are the symptoms of COVID-19?",
        "answer": "COVID-19 affects people differently. Most infected people will develop mild to moderate illness and recover without hospitalization. Most common symptoms include fever, dry cough, and tiredness. Less common symptoms include aches and pains, sore throat, diarrhoea, conjunctivitis, headache, loss of taste or smell, and a rash on skin.",
        "focus": "COVID-19",
        "type": "Symptoms",
        "source": "Sample"
    },
    {
        "question": "What is heart disease?",
        "answer": "Heart disease describes a range of conditions that affect your heart. Diseases under the heart disease umbrella include blood vessel diseases, such as coronary artery disease; heart rhythm problems (arrhythmias); and heart defects you're born with (congenital heart defects).",
        "focus": "Heart disease",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "What are the symptoms of a heart attack?",
        "answer": "Heart attack symptoms include pressure, tightness, pain, or a squeezing sensation in your chest or arms that may spread to your neck, jaw or back, nausea, indigestion, heartburn or abdominal pain, shortness of breath, cold sweat, fatigue, and lightheadedness or sudden dizziness.",
        "focus": "Heart attack",
        "type": "Symptoms",
        "source": "Sample"
    },
    {
        "question": "What is stroke?",
        "answer": "A stroke occurs when the blood supply to part of your brain is interrupted or reduced, preventing brain tissue from getting oxygen and nutrients. Brain cells begin to die in minutes. A stroke is a medical emergency, and prompt treatment is crucial.",
        "focus": "Stroke",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "What are the warning signs of stroke?",
        "answer": "Use the FAST acronym: Face drooping, Arm weakness, Speech difficulty, Time to call emergency services. Other stroke symptoms include sudden numbness or weakness in the face, arm or leg, especially on one side; sudden confusion or trouble understanding; sudden trouble seeing; sudden severe headache with no known cause.",
        "focus": "Stroke",
        "type": "Symptoms",
        "source": "Sample"
    },
    {
        "question": "What is obesity?",
        "answer": "Obesity is a complex disease involving an excessive amount of body fat. Obesity isn't just a cosmetic concern. It's a medical problem that increases the risk of other diseases and health problems, such as heart disease, diabetes, high blood pressure and certain cancers.",
        "focus": "Obesity",
        "type": "Information",
        "source": "Sample"
    },
    {
        "question": "How is obesity treated?",
        "answer": "Obesity treatment focuses on achieving and maintaining a healthier weight through dietary changes, increased physical activity, behavior changes, prescription medications, endoscopic procedures, or surgery. Even modest weight loss of 5 to 10 percent of total body weight can provide significant health benefits.",
        "focus": "Obesity",
        "type": "Treatment",
        "source": "Sample"
    }
]


def parse_medquad_xml(xml_content: str, source: str = "MedQuAD") -> list:
    """Parse a single MedQuAD XML file and extract QA pairs."""
    qa_pairs = []
    try:
        root = ET.fromstring(xml_content)
        focus = root.findtext("Focus", default="General")
        
        for qa_pair in root.findall(".//QAPair"):
            question_elem = qa_pair.find("Question")
            answer_elem = qa_pair.find("Answer")
            
            if question_elem is not None and answer_elem is not None:
                question_text = question_elem.text
                answer_text = answer_elem.text
                q_type = question_elem.get("qtype", "General")
                
                if question_text and answer_text:
                    qa_pairs.append({
                        "question": question_text.strip(),
                        "answer": answer_text.strip(),
                        "focus": focus,
                        "type": q_type,
                        "source": source
                    })
    except ET.ParseError:
        pass
    return qa_pairs


def fetch_github_file_list(folder: str) -> list:
    """Fetch list of XML files from a MedQuAD GitHub folder via API."""
    api_url = f"https://api.github.com/repos/abachaa/MedQuAD/contents/{folder}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"   # ✅ prevents blocking
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            files = response.json()
            return [f["download_url"] for f in files if f["name"].endswith(".xml")]
    except Exception:
        pass
    return []


def load_medquad_data(cache_path: str = "data/medquad_cache.json", 
                      max_files_per_folder: int = 5,
                      use_cache: bool = True) -> pd.DataFrame:
    """
    Load MedQuAD data from GitHub or cache.
    Falls back to sample data if GitHub is unavailable.
    """
    cache_file = Path(cache_path)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Try loading from cache first
    if use_cache and cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                data = json.load(f)
            if data:
                return pd.DataFrame(data)
        except Exception:
            pass
    
    all_qa_pairs = []
    print("Fetching MedQuAD data from GitHub...")
    
    for folder in MEDQUAD_FOLDERS:
        try:
            file_urls = fetch_github_file_list(folder)
            fetched = 0
            
            for url in file_urls[:max_files_per_folder]:
                try:
                    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
                    if resp.status_code == 200:
                        pairs = parse_medquad_xml(resp.text, source=folder)
                        all_qa_pairs.extend(pairs)
                        fetched += 1
                    time.sleep(0.1)  # Rate limiting
                except Exception as e:
                 print(f"Error loading {url}: {e}")
                 continue
                    
            print(f"  ✓ {folder}: {fetched} files loaded")
        except Exception as e:
            print(f"  ✗ {folder}: Failed ({str(e)[:50]})")
    
    # Fallback to sample data if insufficient data fetched
    if len(all_qa_pairs) < 20:
        print("Using built-in sample data as fallback...")
        all_qa_pairs = SAMPLE_QA_DATA
    
    # Save cache
    try:
        with open(cache_file, "w") as f:
            json.dump(all_qa_pairs, f)
    except Exception:
        pass
    
    df = pd.DataFrame(all_qa_pairs)
    df.drop_duplicates(subset=["question"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def get_dataset_stats(df: pd.DataFrame) -> dict:
    """Return statistics about the loaded dataset."""
    return {
        "total_qa_pairs": len(df),
        "unique_topics": df["focus"].nunique() if "focus" in df.columns else 0,
        "question_types": df["type"].value_counts().to_dict() if "type" in df.columns else {},
        "sources": df["source"].value_counts().to_dict() if "source" in df.columns else {},
        "avg_answer_length": int(df["answer"].str.len().mean()) if "answer" in df.columns else 0,
    }