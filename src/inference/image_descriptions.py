from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from PIL import Image
from io import BytesIO
import base64

from src.app_settings import settings
from src.inference.utils import IMAGES_SYSTEM_PROMPT
import asyncio

class ImagesDescriptor:
    def __init__(self):
        self._model = None
        self._agent = None

    def _initialize(self):
        if self._model is None or self._agent is None:
            self._model = OpenAIModel(
                "opengvlab/internvl3-2b:free",
                provider=OpenRouterProvider(api_key=str(settings.chatbot_api_key))
            )
            self._agent = Agent(self._model)

    async def invoke_model(self, prompt: list):
        self._initialize()
        try:
            response = await self._agent.run(prompt) # type: ignore
            return response.output
        except asyncio.TimeoutError:
            raise RuntimeError("Model invocation timed out.")
        except ValueError as ve:
            raise RuntimeError(f"Invalid input: {ve}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during model invocation: {e}")
    
    
    async def generate_image_description(self, img_base64: str, context: str):
        self._initialize()

        image_data_uri = f"data:image/png;base64,{img_base64}"

        # Multimodal prompt format
        prompt = [
            {
                "role": "system",
                "content": IMAGES_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Given the following page text, describe the image:\n\n{context}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_uri
                        },
                    },
                ],
            },
        ]

        return await self.invoke_model(prompt)
    


llm_images = ImagesDescriptor()

# async def main():
#     client = ModelClient()
#     prompt = "What is the capital of France?"
#     try:
#         response = await client.invoke_model(prompt=prompt)
#         print("Model response:", response.output)
#     except Exception as e:
#         print("Error:", e)

# if __name__ == "__main__":
#     asyncio.run(main())