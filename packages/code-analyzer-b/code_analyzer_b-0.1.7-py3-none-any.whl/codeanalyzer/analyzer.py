from tqdm import tqdm
from .deepseek import DeepSeekClient
from .utils import read_file


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

    def analyze_file(self, file_path):
        try:
            code = read_file(file_path)
            result = self.client.analyze_code(code)
            self.stats['total_files'] += 1

            # Track severity levels
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

        except Exception as e:
            pass
        finally:
            self.stats['analyzed_files'] += 1

    def analyze_project(self, file_list):
        with tqdm(
                total=len(file_list),
                desc="Analyzing Files",
                unit="file",
                bar_format="{l_bar}{bar:20}| {n_fmt}/{total_fmt} [{elapsed}]"
        ) as pbar:
            for file_path in file_list:
                self.analyze_file(file_path)
                pbar.update(1)

    def generate_report(self):
        # Generate statistical summary
        stats_summary = self._generate_stats_summary()

        # Generate AI-powered analysis
        ai_summary = self._generate_ai_summary()

        return {
            "summary": f"{stats_summary}\n\n{ai_summary}",
            "detailed_findings": self.findings,
            "stats": self.stats.copy()
        }

    def _generate_stats_summary(self):
        return (
            "Security Analysis Summary:\n"
            f"• Critical Issues: {self.stats['critical']}\n"
            f"• Warnings: {self.stats['warnings']}\n"
            f"• Files Processed: {self.stats['analyzed_files']}/{self.stats['total_files']}"
        )

    def _generate_ai_summary(self):
        if not self.findings:
            return "AI Analysis: No significant issues found"

        print("\nGenerating AI-powered analysis:")
        findings_text = "\n\n".join(
            f"File: {f['file']}\nFindings: {f['result']}"
            for f in self.findings
        )

        full_summary = []
        stream = self.client.generate_summary_streaming(findings_text)
        for chunk in stream:
            full_summary.append(chunk)
            print(chunk, end='', flush=True)

        return "AI Analysis:\n" + ''.join(full_summary)