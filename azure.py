import aiohttp
import asyncio
from aiohttp import ClientSession
import os
from dotenv import load_dotenv

load_dotenv()


async def azure_complete(prompt: str):
    azure_openai_base = os.environ.get('azureOpenaiBase')
    azure_openai_deployment = os.environ.get('azureOpenaiDeployment')
    azure_openai_key = os.environ.get('azureOpenaiKey')

    api_version = "2023-03-15-preview"
    model = "GPT_3_5_TURBO"

    url = f"{azure_openai_base}openai/deployments/{azure_openai_deployment}/completions?api-version={api_version}"
    headers = {
        "api-key": azure_openai_key,
    }
    json_data = {
        "prompt": prompt,
        "temperature": 0,
        "max_tokens": 1200,
        "stream": False,
        "model": model,
        "stop": '```'
    }

    async with ClientSession() as session:
        async with session.post(url, json=json_data, headers=headers, timeout=5.0) as response:
            if response.status != 200:
                raise Exception(f"Request failed with status {response.status}")
            
            return await response.json()
