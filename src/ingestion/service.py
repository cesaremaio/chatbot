import os
import pymupdf4llm
from fitz import Rect

from src.vectordb.service import qdrant_service
from src.ingestion.splitter import hybrid_splitter
from src.ingestion.models import QdrantDocument
from src.vectordb.models import QdrantItems
from src.chain.embedding_service import embedding_service
from loguru import logger
import uuid

from src.app_settings import settings

class PDFIngestionService:
    def __init__(self, collection_name: str, batch_size: int = 8):
        self.collection_name = collection_name
        self.batch_size = batch_size
        

    def get_markdown(self, pdf_path: str):
        image_path = os.path.join(os.getcwd(), "images")
        os.makedirs(image_path, exist_ok=True)
        doc = pymupdf4llm.to_markdown(pdf_path, 
                    page_chunks=True, 
                    write_images=True,
                    image_path=image_path,
                    image_format="png",
                    dpi=300)

        return doc
    
    def get_text(self, pdf_path: str) -> list[str]:
        doc = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
        texts  = [page["text"] for page in doc]  # type: ignore
        return texts
    

    async def extract_metadata(self, pdf_path: str):
        doc = self.get_markdown(pdf_path)
        for page in doc:
            title = page["metadata"]["title"] # type: ignore
            author = page["metadata"]["author"] # type: ignore
            keywords = page["metadata"]["keywords"] # type: ignore
            text = page["text"] # type: ignore
            tables = page["tables"] # type: ignore
            images = page["images"] # type: ignore
        
        return title, author, keywords, text, tables, images

    async def serialize_rects(self, obj):
        if isinstance(obj, Rect):
            return [obj.x0, obj.y0, obj.x1, obj.y1]
        elif isinstance(obj, dict):
            return {k: await self.serialize_rects(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [await self.serialize_rects(i) for i in obj]
        else:
            return obj
        
    async def extract_qdrant_documents(self, pdf_path: str) -> list[QdrantDocument]:
        doc = self.get_markdown(pdf_path)        
        logger.info(f"doc: {doc}")

        qdrant_points = []
        for page in doc:
            title = page["metadata"]["title"] # type: ignore
            author = page["metadata"]["author"] # type: ignore
            keywords = page["metadata"]["keywords"] # type: ignore
            # tables = await self.serialize_rects( page["tables"] )
            # images = await self.serialize_rects( page["images"] )

            page_text = page["text"] # type: ignore
            splitted_text = await hybrid_splitter.recursive_split(page_text)
            final_chunks = await hybrid_splitter.semantic_merge(splitted_text)

            for chunk in final_chunks:
                # logger.info(f"title: {title}")
                # logger.info(f"author: {author}")
                # logger.info(f"keywords: {keywords}")

                qdrant_points.append(
                    QdrantDocument(
                        title=title,
                        author=author,
                        keywords=keywords,
                        text=chunk,
                        full_text=page_text
                    )
                )
        
        return qdrant_points
    
    async def ingestion(self, pdf_path: str):
        qdrant_documents = await self.extract_qdrant_documents(pdf_path)

        items = [
            QdrantItems(
                id = str( uuid.uuid4() ),
                vector = await embedding_service.get_embedding(qdrant_document.text), 
                payload = qdrant_document
            ) 
            for qdrant_document in qdrant_documents
        ]

        await qdrant_service.put_items(collection_name=settings.qdrant_collection,  # type: ignore
                                        items=items)
        
        return

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

pdf_ingestion_service = PDFIngestionService(collection_name="chatbot_qdrant")


async def main():
    pdf_ingestion_service = PDFIngestionService(collection_name="chatbot_qdrant")
    # pdf_path = "/home/cesare/chatbot/CesareMaioCV_latex.pdf"
    # pdf_path = "/home/cesare/chatbot/ItaldesignCoverLetter.pdf"
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

    # texts = pdf_ingestion_service.get_text(pdf_path)
    # for page_text in texts:
    #     splitted_text = await hybrid_splitter.recursive_split(page_text)

    #     # for i, chunk in enumerate(splitted_text):
    #     #     print(f"\033[92mchunk {i}\033[0m: {chunk}\n\n\n")
        
    #     final_chunks = await hybrid_splitter.semantic_merge(splitted_text)
        
    #     for i, chunk in enumerate(final_chunks):
    #         print(f"\033[92mchunk {i}\033[0m: {chunk}\n\n\n")
    

    # qdrant_docs = await pdf_ingestion_service.extract_qdrant_documents(pdf_path)
    # print(len(qdrant_docs))


    await pdf_ingestion_service.ingestion(pdf_path)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())