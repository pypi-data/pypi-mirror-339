# CodeAnalyzer🔍 | AI-Powered Code Security Analysis

[![PyPI Version](https://img.shields.io/pypi/v/code-analyzer-b.svg)](https://pypi.org/project/code-analyzer-b/)
[![Python Versions](https://img.shields.io/pypi/pyversions/code-analyzer-b.svg)](https://pypi.org/project/code-analyzer-b/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Async Powered](https://img.shields.io/badge/Async-Powered-ff69b4.svg)](https://docs.python.org/3/library/asyncio.html)
[![SARIF Support](https://img.shields.io/badge/SARIF-2.1.0-green.svg)](https://docs.github.com/en/code-security/code-scanning/sarif-support)

**Enterprise-grade static analysis with AI-powered vulnerability detection and async-powered performance**

```bash
pip install code-analyzer-b
```

## ✨ Key Features

- **Lightning-Fast Analysis** - Async-powered scanning with 3x speed boost ⚡
- **Summary Mode** - `--no-details` for quick security overviews
- **AI-Powered Insights** - DeepSeek integration for intelligent vulnerability detection
- **Smart Reporting** - SARIF, HTML, JSON, Markdown outputs
- **CI/CD Optimized** - GitHub Actions, GitLab CI, Jenkins integration
- **Security Compliance** - OWASP Top 10, CWE/SANS Top 25 coverage

![Architecture Diagram](diagram.png)

## 🚀 Quick Start

### Installation
```bash
pip install code-analyzer-b
```

### Basic Usage
```bash
# Initialize configuration
code_analyzer setup

# Quick analysis with summary report
code_analyzer analyze https://github.com/your/repo --no-details

# Full analysis with HTML report
code_analyzer analyze . --output full_report.html
```

## 🛠️ Advanced Features

### CI/CD Integration
```yaml
- name: Run Security Scan
  uses: code-analyzer/action@v1
  with:
    output_format: 'sarif'
    output_file: 'results.sarif'
    no_details: true  # Enable summary mode

```

## 📊 Report Types

| Option          | Command               | Best For                  | Speed   |
|-----------------|-----------------------|---------------------------|---------|
| Full Report     | `--output report.html`| Detailed audits           | Standard|
| Summary Mode    | `--no-details`        | Quick status checks       | 2x Faster|
| SARIF Export    | `--format sarif`      | GitHub Code Scanning      | Async   |

## ⚡ Performance Benchmarks

| Scenario        | Files | v0.1.8 | v0.1.9 (Async) | Improvement |
|-----------------|-------|--------|----------------|-------------|
| Standard Scan   | 500   | 68s    | 22s            | 3.1x        |
| Summary Mode    | 500   | -      | 14s            | 4.8x        |
| CI/CD Pipeline  | 1000  | 143s   | 39s            | 3.7x        |

## 💡 Pro Tips

```bash
# Generate multiple report formats
code_analyzer analyze . --output summary.txt --no-details --format json=full.json

# Analyze private repos with async speed
code_analyzer analyze private-repo/ --git-token=ghp_xxxx --no-details
```

## 🌐 Supported Languages

| Language       | Extensions           | Async Support      |
|----------------|----------------------|--------------------|
| Python         | `.py`                | ✅ Full           |
| JavaScript/TS  | `.js`, `.ts`         | ✅ Concurrent     |
| Java           | `.java`              | ✅ Batch          |
| C/C++          | `.c`, `.cpp`         | ✅ Parallel       |
| Go             | `.go`                | ✅ Optimized      |
| Rust           | `.rs`                | ✅ Streamlined    |

## 🚨 Security Compliance

- SARIF 2.1.0 Standard
- OWASP Top 10 2023
- GDPR/CCPA Ready
- Zero Data Retention

---

**Why Upgrade?**  
v0.1.9 delivers 3x faster scans through async processing and new summary mode for rapid security assessments 🚀

[GitHub Repository](https://github.com/BotirBakhtiyarov/code_analyzer) | 
[PyPI Package](https://pypi.org/project/code-analyzer-b/) | 
[Telegram Channel](https://t.me/opensource_uz) |
[Community Discord](https://discord.gg/e63MyDs8)