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
        if self.session and not self.session.closed:
            await self.session.close()
        await asyncio.sleep(0)

    async def analyze_code(self, code):
        """Non-streaming code analysis"""
        payload = self._create_payload(code)
        return await self._make_request(payload)

    async def analyze_code_stream(self, code):
        """Streaming code analysis generator"""
        payload = self._create_payload(code, stream=True)
        async for chunk in self._make_stream_request(payload):
            yield chunk

    async def generate_summary(self, findings_text):
        """Non-streaming summary generation"""
        payload = self._create_summary_payload(findings_text)
        return await self._make_request(payload)

    async def generate_summary_stream(self, findings_text):
        """Streaming summary generation generator"""
        payload = self._create_summary_payload(findings_text, stream=True)
        async for chunk in self._make_stream_request(payload):
            yield chunk

    def _create_payload(self, code, stream=False):
        return {
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
            "temperature": 0.2,
            "stream": stream
        }

    def _create_summary_payload(self, findings_text, stream=False):
        return {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Summarize security findings into a clear report. Highlight critical issues."
                },
                {
                    "role": "user",
                    "content": f"Summarize these findings:\n\n{findings_text}"
                }
            ],
            "temperature": 0.2,
            "stream": stream
        }

    async def _make_request(self, payload):
        """Handle non-streaming requests"""
        headers = self._get_headers()
        try:
            async with self.session.post(
                Config.DEEPSEEK_API_URL,
                headers=headers,
                json=payload,
                timeout=Config.REQUEST_TIMEOUT
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data['choices'][0]['message']['content']
        except aiohttp.ClientError as e:
            raise Exception(f"API connection error: {str(e)}")

    async def _make_stream_request(self, payload):
        """Handle streaming requests"""
        headers = self._get_headers()
        try:
            async with self.session.post(
                Config.DEEPSEEK_API_URL,
                headers=headers,
                json=payload,
                timeout=Config.REQUEST_TIMEOUT
            ) as response:
                response.raise_for_status()
                async for line in response.content:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        json_data = decoded_line[6:]
                        if json_data == "[DONE]":
                            break
                        try:
                            data = json.loads(json_data)
                            yield data['choices'][0]['delta'].get('content', '')
                        except json.JSONDecodeError:
                            continue
        except aiohttp.ClientError as e:
            raise Exception(f"API connection error: {str(e)}")

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}"
        }