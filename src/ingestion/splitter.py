from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.chain.embedding_service import embedding_service

class HybridSplitter:
    def __init__(self, delimiter=None, maxsplit=-1):
        self.delimiter = delimiter
        self.maxsplit = maxsplit


    async def recursive_split(self, text_to_split: str) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        recursive_splitted = splitter.split_text(text_to_split)
        return recursive_splitted

            
    async def semantic_merge(self, split_texts: list[str]) -> list[str]:
        if len(split_texts) < 2:
            return split_texts  # Nothing to merge

        # Compute embeddings asynchronously
        embeddings = [await embedding_service.get_embedding(text) for text in split_texts]

        # Compute pairwise similarities
        similarities = [
            cosine_similarity([embeddings[i]], [embeddings[i + 1]])[0][0]
            for i in range(len(embeddings) - 1)
        ]

        if not similarities:
            return split_texts  # Fallback in case similarity list is empty

        # Compute similarity threshold (e.g. 10th percentile)
        threshold = np.percentile(similarities, 10)

        # Identify semantic breakpoints
        breakpoints = [i for i, sim in enumerate(similarities) if sim < threshold]

        # Merge chunks based on semantic similarity
        chunks = []
        start = 0
        for idx in breakpoints:
            chunk = " ".join(split_texts[start:idx + 1])
            chunks.append(chunk)
            start = idx + 1
        if start < len(split_texts):
            chunks.append(" ".join(split_texts[start:]))

        return chunks



hybrid_splitter = HybridSplitter()