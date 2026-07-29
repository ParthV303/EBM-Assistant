import faiss
import numpy as np

print("Loading embeddings...")

embeddings = np.load("embeddings.npy")

print("Embeddings Shape:", embeddings.shape)

embeddings = embeddings.astype("float32")

dimension = embeddings.shape[1]

print("Vector Dimension:", dimension)

index = faiss.IndexFlatL2(dimension)

print("Adding vectors to FAISS...")

index.add(embeddings)

print("Total vectors in index:", index.ntotal)

faiss.write_index(
    index,
    "faiss_index.bin"
)

print("FAISS Index Saved Successfully!")