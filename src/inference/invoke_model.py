from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider


from src.app_settings import settings
import asyncio

class ModelClient:
    def __init__(self):
        self._model = None
        self._agent = None

    def _initialize(self):
        if self._model is None or self._agent is None:
            self._model = OpenAIModel(
                "deepseek/deepseek-r1-0528-qwen3-8b:free",
                provider=OpenRouterProvider(api_key=str(settings.chatbot_api_key))
            )
            self._agent = Agent(self._model)

    async def invoke_model(self, prompt: str):
        self._initialize()
        try:
            response = await self._agent.run(prompt) # type: ignore
            return response
        except asyncio.TimeoutError:
            raise RuntimeError("Model invocation timed out.")
        except ValueError as ve:
            raise RuntimeError(f"Invalid input: {ve}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during model invocation: {e}")
    

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