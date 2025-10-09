# ----------------- Using CPU -------------------


# from sentence_transformers import SentenceTransformer
# from typing import List

# class Embedder:
#     def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
#         # This will download the model on first run
#         self.model = SentenceTransformer(model_name)

#     def embed_texts(self, texts: List[str]) -> List[List[float]]:
#         """
#         Generates embeddings for a list of texts.
#         """
#         embeddings = self.model.encode(texts, convert_to_tensor=False)
#         return embeddings.tolist()

# # Initialize a singleton instance
# embedder = Embedder()


# ----------------- Using GPU -------------------

# backend/app/rag/embedder.py
from typing import List

import torch
from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Automatically detect and use GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🔥 Embedder using device: {self.device}")

        # Load model on GPU if available
        self.model = SentenceTransformer(model_name, device=self.device)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts.
        Uses GPU automatically if available.
        """
        # convert_to_tensor=True uses GPU acceleration
        embeddings = self.model.encode(
            texts,
            convert_to_tensor=True,  # ← Enables GPU tensors
            show_progress_bar=True,
        )
        # Convert back to CPU numpy for storage
        return embeddings.cpu().numpy().tolist()


# Initialize a singleton instance
embedder = Embedder()
