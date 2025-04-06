from tqdm import tqdm
from .deepseek import DeepSeekClient
from .utils import read_file
import concurrent.futures
import asyncio

class CodeAnalyzer:
    def __init__(self):
        self.client = DeepSeekClient()
        self.findings = []
        self.stats = {
            'total_files': 0,
            'critical': 0,
            'warnings': 0,
            'analyzed_files': 0
        }

    async def __aenter__(self):
        self.client = DeepSeekClient()
        return self

    async def __aexit__(self, *exc_info):
        if self.client:
            await self.client.session.close()

    async def analyze_file(self, file_path):
        try:
            code = read_file(file_path)
            async with self.client as client:
                result = await client.analyze_code(code)
            self.stats['total_files'] += 1

            result_lower = result.lower()
            if 'critical' in result_lower:
                self.stats['critical'] += 1
            elif 'warning' in result_lower:
                self.stats['warnings'] += 1

            if "no issues" not in result_lower:
                self.findings.append({
                    "file": file_path,
                    "result": result
                })


        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"Error analyzing {file_path}: {str(e)}")
        finally:
            self.stats['analyzed_files'] += 1

    async def analyze_project(self, file_list, max_concurrent=8):
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_file(file_path):
            async with semaphore:
                await self.analyze_file(file_path)
            pbar.update(1)

        with tqdm(
                total=len(file_list),
                desc="Analyzing Files",
                unit="file",
                bar_format="{l_bar}{bar:20}| {n_fmt}/{total_fmt} [{elapsed}]"
        ) as pbar:
            tasks = [process_file(file_path) for file_path in file_list]
            await asyncio.gather(*tasks)

    async def generate_report(self, include_details=True):
        stats_summary = self._generate_stats_summary()
        ai_summary = await self._generate_ai_summary()

        report = {
            "summary": f"{stats_summary}\n\n{ai_summary}",
            "stats": self.stats.copy()
        }

        if include_details:
            report["detailed_findings"] = self.findings

        return report

    def _generate_stats_summary(self):
        return (
            "Security Analysis Summary:\n"
            f"• Critical Issues: {self.stats['critical']}\n"
            f"• Warnings: {self.stats['warnings']}\n"
            f"• Files Processed: {self.stats['analyzed_files']}/{self.stats['total_files']}"
        )

    async def _generate_ai_summary(self):
        if not self.findings:
            return "AI Analysis: No significant issues found"

        print("\nGenerating AI-powered analysis:")
        findings_text = "\n\n".join(
            f"File: {f['file']}\nFindings: {f['result']}"
            for f in self.findings
        )

        full_summary = []
        async with self.client as client:
            stream = client.generate_summary_streaming(findings_text)
            async for chunk in stream:
                full_summary.append(chunk)
                print(chunk, end='', flush=True)

        return "AI Analysis:\n" + ''.join(full_summary)