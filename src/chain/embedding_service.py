from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.embedding_model = SentenceTransformer("thenlper/gte-small")
        
    async def get_embedding(self, text: str):
        embedding = self.embedding_model.encode(text, convert_to_tensor=True)
        return embedding.tolist()


embedding_service = EmbeddingService()



# async def main():
#     txt = ["ciao", "hello"]
#     embedding = await embedding_service.get_embedding(txt)
#     print(f"type(embedding): {type(embedding)}")
#     print(f"len(embedding): {len(embedding)}")
#     # print(f"embedding: {embedding}")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())