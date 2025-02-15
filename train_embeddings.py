from sentence_transformers import SentenceTransformer
import json
import faiss
import numpy as np


def embed_code(context, save_path="embeddings/"):
    """Embeds code context using SentenceTransformer."""
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Checks if context is a list of dictionaries with correct structure
    if not all(
        isinstance(item, dict) and "type" in item and "name" in item for item in context
    ):
        raise ValueError(
            "Context must be a list of dictionaries with 'type' and 'name' keys."
        )

    # Prepare snippets for embedding
    snippets = [
        f"{item['type']} {item['name']}:\n{item.get('docstring', 'No docstring provided')}"
        for item in context
    ]

    # Generate embeddings for all the snippets
    embeddings = model.encode(snippets)
    embeddings = np.array(embeddings)  # Convert embeddings to numpy array

    # Create and save FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])  # Use L2 distance metric
    index.add(embeddings)  # Add embeddings to the FAISS index
    faiss.write_index(index, f"{save_path}code_index.bin")  # Save FAISS index to file

    # Save metadata
    with open(f"{save_path}metadata.json", "w") as f:
        json.dump(context, f)

    print("Embeddings and metadata saved.")
