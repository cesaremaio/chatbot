from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

import asyncio

from src.app_settings import settings
async def main():
    model = OpenAIModel(
        "deepseek/deepseek-r1-0528-qwen3-8b:free",  # or any other OpenRouter model
        provider=OpenRouterProvider(api_key=str(settings.chatbot_api_key)))

    agent = Agent(model)
    result = await agent.run("What is the meaning of life?")
    print(result.output)

if __name__ == '__main__':
    asyncio.run(main())