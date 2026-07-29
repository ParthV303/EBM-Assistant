import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

current_dir = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(
    current_dir,
    "..",
    "dataset",
    "EBM.csv"
)

print("Loading dataset...")

df = pd.read_csv(
    csv_path,
    sep=";"
)

print("Dataset loaded successfully!")
print("Shape:", df.shape)

print("\nColumns:")
print(df.columns)

texts = (
    df["Title"].fillna("").astype(str)
    + " "
    + df["Summary"].fillna("").astype(str)
).tolist()

print(f"\nTotal documents: {len(texts)}")

print("\nLoading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model loaded!")

print("\nGenerating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True
)

print("\nEmbeddings generated!")
print("Shape:", embeddings.shape)

np.save(
    "embeddings.npy",
    embeddings
)

print("\nEmbeddings saved successfully!")