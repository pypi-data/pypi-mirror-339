import aiohttp
import json
from contextlib import asynccontextmanager
from codeanalyzer.config import Config
import asyncio


class DeepSeekClient:
    def __init__(self):
        self._session = None
        self._semaphore = asyncio.Semaphore(5)  # Limit concurrent requests

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=Config.REQUEST_TIMEOUT)
        )
        return self

    async def __aexit__(self, *exc_info):
        await self._session.close()

    async def get_session(self):
        """Lazy initialization of session"""
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=Config.REQUEST_TIMEOUT)
            )
        return self._session

    async def close(self):
        """Explicit close method"""
        if self._session and not self._session.closed:
            await self._session.close()

    @asynccontextmanager
    async def session_context(self):
        """Manage the aiohttp session lifecycle"""
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=Config.REQUEST_TIMEOUT)
        )
        try:
            yield
        finally:
            await self._session.close()
            self._session = None

    async def analyze_code(self, code):
        """Analyze code with concurrency control and proper error handling"""
        async with self._semaphore:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}"
            }

            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a security expert analyzing code for vulnerabilities..."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this code:\n\n{code}"
                    }
                ],
                "temperature": 0.2
            }

            try:
                async with self._session.post(
                        Config.DEEPSEEK_API_URL,
                        headers=headers,
                        json=payload
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data['choices'][0]['message']['content']
            except aiohttp.ClientError as e:
                print(f"Request failed: {str(e)}")
                return "Analysis unavailable"

    async def generate_summary_streaming(self, findings):
        """Stream summary with proper cleanup"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Summarize security findings..."
                },
                {
                    "role": "user",
                    "content": f"Summarize:\n\n{findings}"
                }
            ],
            "temperature": 0.2,
            "stream": True
        }

        try:
            async with self._session.post(
                    Config.DEEPSEEK_API_URL,
                    headers=headers,
                    json=payload
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
        except aiohttp.ClientError as e:
            print(f"Streaming failed: {str(e)}")
            yield "Summary unavailable"
