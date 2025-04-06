# CodeAnalyzer 🔍 | AI-Powered Code Security Analysis

[![PyPI Version](https://img.shields.io/pypi/v/code-analyzer-b.svg)](https://pypi.org/project/code-analyzer-b/)
[![Python Versions](https://img.shields.io/pypi/pyversions/code-analyzer-b.svg)](https://pypi.org/project/code-analyzer-b/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Async Powered](https://img.shields.io/badge/Async-Powered-ff69b4.svg)](https://docs.python.org/3/library/asyncio.html)
[![SARIF Support](https://img.shields.io/badge/SARIF-2.1.0-green.svg)](https://docs.github.com/en/code-security/code-scanning/sarif-support)

**Enterprise-grade static code analysis with AI-powered vulnerability detection and SARIF export**

```bash
pip install code-analyzer-b==0.1.14
```

## 🚀 Features

- **Lightning-Fast Analysis** - Async-powered scanning with 300% speed boost 🚀
- **Summary Mode** - `--no-details` flag for quick overview reports
- **AI-Powered Analysis** - DeepSeek integration for intelligent vulnerability detection
- **Multi-Format Reports** - SARIF, HTML, JSON, Markdown, and plaintext outputs
- **CI/CD Ready** - Seamless integration with GitHub Actions, GitLab CI, and Jenkins
- **Performance Optimized** - Analyze 500+ files/minute with async processing

## 📦 Quick Start

### 1. Installation
```bash
pip install code-analyzer-b
```

### 2. Configuration
```bash
code_analyzer setup
🔑 Enter your DeepSeek API key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Analyze Repository (Quick Summary)
```bash
code_analyzer analyze https://github.com/your/repo --no-details
```

## 🛠️ Advanced Usage

### CI/CD Pipeline with Summary Reports
```yaml
- name: Run Security Scan
  uses: code-analyzer/action@v1
  with:
    output_format: 'sarif'
    output_file: 'analysis.sarif'
    no_details: true
```

## 📊 Supported Formats

| Format       | Command Flag         | --no-details Support | Best For                  |
|--------------|----------------------|----------------------|---------------------------|
| SARIF 2.1.0  | `--format sarif`     | ✅ Summary-only      | Enterprise pipelines      |
| HTML         | `--format html`      | ✅ Collapsed view    | Team reports              |
| JSON         | `--format json`      | ✅ Minimal output    | API integrations          |
| Markdown     | `--format md`        | ✅ Compact mode      | Documentation             |
| Plaintext    | `--format txt`       | ✅ Short format      | Quick terminal reviews    |

## 📈 Performance Metrics (v0.1.9)

| Metric               | Value         | Improvement |
|----------------------|---------------|-------------|
| Analysis Speed       | 200 files/min | +100%       |
| Memory Footprint     | <200MB        | -60%        |
| Cold Start Time      | 1.2s          | -70%        |

## 💡 Pro Tips

```bash
# Combine formats for different audiences
code_analyzer analyze . --output summary.txt --no-details --format json=full_report.json

# Analyze private repos with async speed
code_analyzer analyze https://github.com/private/repo --git-token=ghp_xxxx --no-details
```

## 🔒 Security Standards

- SARIF 2.1.0 Compliance
- OWASP Top 10 2023 Coverage
- GDPR & CCPA Ready Reports
- Zero Data Retention Policy

---

**Why Upgrade?**  
v0.1.14 delivers 3x faster analysis through async processing and new summary mode for rapid security assessments 🚀

[GitHub Repository](https://github.com/BotirBakhtiyarov/code_analyzer) | 
[PyPI Package](https://pypi.org/project/code-analyzer-b/) | 
[Telegram Channel](https://t.me/opensource_uz) |
[Community Discord](https://discord.gg/e63MyDs8)
