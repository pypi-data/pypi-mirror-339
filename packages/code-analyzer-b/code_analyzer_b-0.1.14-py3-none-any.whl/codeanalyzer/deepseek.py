import asyncio

import aiohttp
import json
from codeanalyzer.config import Config

class DeepSeekClient:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *exc_info):
        if self.session:
            await self.session.close()
        await asyncio.sleep(0)

    async def analyze_code(self, code):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a security expert analyzing code for vulnerabilities and bugs. "
                               "Identify and explain any issues found. Keep responses concise."
                },
                {
                    "role": "user",
                    "content": f"Analyze this code for security vulnerabilities and bugs:\n\n{code}"
                }
            ],
            "temperature": 0.2
        }

        async with self.session.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=Config.REQUEST_TIMEOUT
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data['choices'][0]['message']['content']

    async def generate_summary_streaming(self, findings):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Summarize security findings into a clear report. Highlight critical issues."
                },
                {
                    "role": "user",
                    "content": f"Summarize these findings:\n\n{findings}"
                }
            ],
            "temperature": 0.2,
            "stream": True
        }

        async with self.session.post(
                Config.DEEPSEEK_API_URL,
                headers=headers,
                json=payload,
                timeout=Config.REQUEST_TIMEOUT
        ) as response:
            response.raise_for_status()

            async for line in response.content:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    json_data = decoded_line[6:]
                    if json_data.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(json_data)
                        yield data['choices'][0]['delta'].get('content', '')
                    except json.JSONDecodeError:
                        continue