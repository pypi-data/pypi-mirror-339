```
   ██████╗ ██████╗ ██████╗ ███████╗    █████╗ ███╗   ██╗ █████╗ ██╗   ██╗   ██╗ ███████╗███████╗██████╗ 
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝   ██╔══██╗████╗  ██║██╔══██╗██║   ╚██╗ ██╔╝ ╚══███╔╝██╔════╝██╔══██╗
  ██║     ██║   ██║██║  ██║█████╗     ███████║██╔██╗ ██║███████║██║    ╚████╔╝    ███╔╝ █████╗  ██████╔╝
  ██║     ██║   ██║██║  ██║██╔══╝     ██╔══██║██║╚██╗██║██╔══██║██║      ██╔╝    ███╔╝  ██╔══╝  ██╔══██╗
  ╚██████╗╚██████╔╝██████╔╝███████╗██╗██║  ██║██║ ╚████║██║  ██║███████╗ ██║    ███████╗███████╗██║  ██║
   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚═╝    ╚══════╝╚══════╝╚═╝  ╚═╝
```

**Code Analyzer** 🛡️ is an open-source command-line tool designed to help developers and security professionals analyze code repositories for vulnerabilities 🐛 and bugs. By leveraging the power of AI 🤖 through the DeepSeek API, it provides detailed insights and recommendations to improve code quality and security.

**Version**: 0.2.x 🚀

---

## 📋 Table of Contents

- 📦 [Installation](#installation)
- 🕵️ [Usage](#usage)
- ⚙️ [CI/CD Integration](#cicd-integration)
- 🤝 [Contributing](#contributing)
- ⚖️ [License](#license)

---

## 📦 Installation

### Prerequisites

- 🐍 Python 3.6 or higher
- 🔑 A DeepSeek API key (obtainable from [DeepSeek](https://www.deepseek.com/))

### Install from PyPI

```bash
pip install code-analyzer
```

### Set Up API Key

```bash
code_analyzer setup
```
The key will be saved in `~/.code_analyzer/config.ini` 🔒

---

## 🕵️ Usage

### Analyzing a GitHub Repository 🌐

Public repo:
```bash
code_analyzer analyze https://github.com/user/repo
```

Private repo 🔐:
```bash
code_analyzer analyze https://github.com/user/private-repo --git-token YOUR_TOKEN
```

### Analyzing a Local Directory 📂

```bash
code_analyzer analyze /path/to/local/repo
```

Current directory 🔄:
```bash
code_analyzer analyze .
```

### ⚙️ Command-Line Options

- `-o, --output FILE` 💾: Save report (`.txt`, `.md`, `.html`, `.json`, `.sarif`)
- `-f, --format FORMAT` 🎨: Output format
- `--verbose` 📢: Debugging output
- `--no-details` 🚫: Minimal report
- `--lang LANG` 🌍: Language support
- `--no-stream` 🤐: Silent mode

Example 🧪:
```bash
code_analyzer analyze . --output report.sarif --format sarif --no-stream --lang uz
```

---

## ⚡ CI/CD Integration

### Example GitHub Actions Workflow 🤖

```yaml
name: Code Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code 
      uses: actions/checkout@v4
    
    - name: Set up Python 
      uses: actions/setup-python@v5
    
    - name: Install code-analyzer 
      run: pip install code-analyzer-b
    
    - name: Configure API key 
      env:
        DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
      run: mkdir -p ~/.code_analyzer && echo "[DEEPSEEK]\nAPI_KEY = $DEEPSEEK_API_KEY" > ~/.code_analyzer/config.ini
    
    - name: Run analysis 
      run: code_analyzer analyze . --output report.sarif --format sarif --no-stream --lang en
    
    - name: Upload SARIF 
      uses: github/codeql-action/upload-sarif@v3
```

---

## 🤝 Contributing

1. 🍴 Fork the repo
2. 🌱 Create a feature branch
3. 📤 Open a PR

**Found an issue?** 🐛 [Open an issue](https://github.com/BotirBakhtiyarov/code_analyzer-b/issues)

---

## ⚖️ License

MIT License - see [LICENSE](LICENSE) 📜