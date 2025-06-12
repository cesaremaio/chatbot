import os
from typing import List
import pymupdf4llm
from qdrant_client import QdrantClient
from src.vectordb.service import qdrant_service
from src.ingestion.splitter import hybrid_splitter

class PDFIngestionService:
    def __init__(self, collection_name: str, batch_size: int = 8):
        self.collection_name = collection_name
        self.batch_size = batch_size
        

    def get_markdown(self, pdf_path: str):
        doc = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
        return doc
    
    def get_text(self, pdf_path: str) -> list[str]:
        doc = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
        texts  = [page["text"] for page in doc]
        return texts
    

    async def extract_metadata(self, pdf_path: str):
        doc = self.get_markdown(pdf_path)
        for page in doc:
            title = page["metadata"]["title"]
            author = page["metadata"]["author"]
            keywords = page["metadata"]["keywords"]
            text = page["text"]
            tables = page["tables"]
            images = page["images"]
        

        



    # def upload_chunks(self, chunks: List[str]):
    #     batch = []
    #     for idx, chunk in enumerate(chunks):
    #         payload = {"text": chunk}
    #         batch.append(payload)
    #         if len(batch) == self.batch_size or idx == len(chunks) - 1:
    #             self.qdrant.upload_collection(
    #                 collection_name=self.collection_name,
    #                 payload=batch
    #             )
    #             batch = []

    # def ingest_pdf(self, pdf_path: str, chunk_size: int = 500):
    #     chunks = self.extract_text_chunks(pdf_path, chunk_size)
    #     self.upload_chunks(chunks)


import asyncio
async def main():
    pdf_ingestion_service = PDFIngestionService(collection_name="chatbot_qdrant")
    # pdf_path = "/home/cesare/chatbot/CesareMaioCV_latex.pdf"
    pdf_path = "/home/cesare/chatbot/attention.pdf"

    # ## GET MARKDOWN
    # def test_get_markdown(pdf_path: str):
    #     markdown = pdf_ingestion_service.get_markdown(pdf_path)

    #     # for key in markdown[0].keys():
    #     #     print(f"{key}: {markdown[0][f"{key}"]} \n")

    #     for doc in markdown:
    #         title = doc["metadata"]["title"]
    #         author = doc["metadata"]["author"]
    #         keywords = doc["metadata"]["keywords"]
    #         text = doc["text"]
    #         tables = doc["tables"]
    #         images = doc["images"]
        
    #         print(f"title: {title}")
    #         print(f"author: {author}")
    #         print(f"keywords: {keywords}")
    #         print(f"text: {text}")
    #         print(f"tables: {tables}")
    #         print(f"images: {images}")
    # test_get_markdown(pdf_path)


    ## GET TEXT
    # def get_texts(pdf_path: str):
    #     texts = pdf_ingestion_service.get_text(pdf_path)
    #     for i, text in enumerate(texts): 
    #         print(f"{i}: {text}")
        
    # get_texts(pdf_path)

    texts = pdf_ingestion_service.get_text(pdf_path)
    for page_text in texts:
        splitted_text = await hybrid_splitter.recursive_split(page_text)

        # for i, chunk in enumerate(splitted_text):
        #     print(f"\033[92mchunk {i}\033[0m: {chunk}\n\n\n")
        
        final_chunks = await hybrid_splitter.semantic_merge(splitted_text)
        
        for i, chunk in enumerate(final_chunks):
            print(f"\033[92mchunk {i}\033[0m: {chunk}\n\n\n")

if __name__ == "__main__":
    asyncio.run(main())