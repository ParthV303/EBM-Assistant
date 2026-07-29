import faiss
import pandas as pd
import numpy as np
import re

from sentence_transformers import SentenceTransformer
from gradio_client import Client


CANCER_KEYWORDS = [
    "cancer", "oncology", "oncologist", "tumor", "tumour", "malignant",
    "malignancy", "carcinoma", "sarcoma", "lymphoma", "leukemia", "leukaemia",  
    "melanoma", "myeloma", "blastoma", "glioma", "mesothelioma", "neoplasm",
    "metastasis", "metastatic", "metastases", "biopsy", "remission",
    "chemotherapy", "radiotherapy", "immunotherapy", "targeted therapy",
    "radiation therapy", "bone marrow transplant", "stem cell transplant",
    "checkpoint inhibitor", "car-t", "cart cell", "anti-tumor", "antitumor",
    "cytotoxic", "adjuvant", "neoadjuvant",
    "breast cancer", "lung cancer", "colorectal", "colon cancer",
    "prostate cancer", "ovarian cancer", "cervical cancer", "pancreatic cancer",
    "liver cancer", "hepatocellular", "renal cell", "kidney cancer",
    "bladder cancer", "thyroid cancer", "brain tumor", "glioblastoma",
    "hodgkin", "non-hodgkin", "myelodysplastic",
    "pdl1", "pd-l1", "her2", "brca", "egfr", "kras", "vegf", "tp53",
    "tumor marker", "biomarker", "ctdna", "circulating tumor",
    "tumor suppressor", "oncogene", "apoptosis", "angiogenesis",
    "staging", "tnm", "grade", "differentiation", "pathology",
    "histology", "cytology", "immunohistochemistry", "ihc",
    "palliative", "hospice", "survivorship", "cancer screening",
    "mammogram", "colonoscopy", "psa test",
]

CANCER_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(kw) for kw in CANCER_KEYWORDS) + r")\b",
    re.IGNORECASE,
)

OFF_TOPIC_REPLY = (
    "⚠️ **Out of Scope**\n\n"
    "This assistant is specialised exclusively in **Cancer & Oncology** "
    "Evidence-Based Medicine.\n\n"
    "Please ask a question related to cancer types, oncology treatments, "
    "tumour biology, chemotherapy, radiotherapy, immunotherapy, "
    "cancer biomarkers, staging, or related clinical topics."
)

df = pd.read_csv(
    "../dataset/EBM.csv",
    sep=";"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "faiss_index.bin"
)

client = None

def ask_ebm(question):

    if not CANCER_PATTERN.search(question):
        return OFF_TOPIC_REPLY

    global client

    if client is None:

        try:
            client = Client(
                "parth2612/EBM-Assistant"
            )

        except Exception as e:

            return (
                "Unable to connect to Hugging Face Space.\n\n"
                f"{str(e)}"
            )

    query_embedding = model.encode(
        [question]
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        3
    )

    context = ""
    references = []

    for rank, i in enumerate(indices[0], start=1):

        title = df.iloc[i]["Title"]
        summary = df.iloc[i]["Summary"]
        source = df.iloc[i]["Source"]
        link = df.iloc[i]["Link"]

        context += f"""
Title: {title}

Summary:
{summary}

"""

        references.append(
            f"[{rank}] {title}\n"
            f"Source: {source}\n"
            f"Link: {link}"
        )

    prompt = f"""
You are a strict Cancer and Oncology Evidence-Based Medicine Assistant.

Answer ONLY using the papers below.

Question:
{question}

Research Papers:
{context}

Format:

Direct Answer:
(2-4 sentence answer)

Key Findings:
- finding 1
- finding 2
- finding 3

Clinical Implications:
- implication 1
- implication 2

Do NOT include references.
Do NOT include source names.
Do NOT include URLs.
"""

    try:
        print("Calling BioMistral...")

        answer = client.predict(
            prompt=prompt,
            api_name="/generate"
        )

        print("BioMistral Finished")

    except Exception as e:

        client = None

        return (
            f"API Error:\n\n{str(e)}"
        )

    if "REFERENCES" in answer:
        answer = answer.split("REFERENCES")[0]

    if "Source:" in answer:
        answer = answer.split("Source:")[0]

    final_response = (
        answer.strip()
        + "\n\nReferences:\n\n"
        + "\n\n".join(references)
    )

    return final_response