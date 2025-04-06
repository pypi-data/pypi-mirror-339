import requests
import json
from codeanalyzer.config import Config


class DeepSeekClient:
    @staticmethod
    def analyze_code(code):
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

        response = requests.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=Config.REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    @staticmethod
    def generate_summary_streaming(findings):
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

        response = requests.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=Config.REQUEST_TIMEOUT
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
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