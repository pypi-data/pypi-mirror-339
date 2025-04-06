import os
import tempfile
import zipfile
import io
import requests
from tqdm import tqdm
import json
from codeanalyzer.config import Config
from . import __version__


def download_repo(target, git_token=None):
    if os.path.exists(target):
        return target
    temp_dir = tempfile.mkdtemp(prefix="code_analyzer_")
    headers = {'User-Agent': 'CodeAnalyzer'}
    if git_token:
        headers['Authorization'] = f'token {git_token}'

    # Try both main and master branches
    branches = ['main', 'master']
    for branch in branches:
        zip_url = f"{target}/archive/refs/heads/{branch}.zip"
        response = requests.get(zip_url, headers=headers, stream=True)
        if response.status_code == 200:
            break
    else:
        error_msg = "Failed to download repository. Possible reasons:\n"
        error_msg += "- Invalid/Missing GitHub token for private repo\n"
        error_msg += "- Repository/branch doesn't exist"
        raise ValueError(error_msg)

    total_size = int(response.headers.get('content-length', 0))

    with tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            desc="Downloading Repository",
            bar_format="{desc}: {percentage:3.0f}%|{bar:20}| {n_fmt}/{total_fmt}",
            ascii="->="
    ) as progress_bar:
        zip_content = io.BytesIO()
        for data in response.iter_content(chunk_size=1024):
            zip_content.write(data)
            progress_bar.update(len(data))

    with zipfile.ZipFile(zip_content) as zip_ref:
        zip_ref.extractall(temp_dir)

    extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
    return extracted_dir


def scan_files(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) > Config.MAX_FILE_SIZE:
                continue
            ext = os.path.splitext(file_path)[1]
            if ext.lower() in Config.SUPPORTED_EXTENSIONS:
                file_list.append(file_path)
    return file_list


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def write_report(report, filename, format=None):
    if format:
        file_ext = f'.{format}'
    else:
        file_ext = os.path.splitext(filename)[1].lower()

    if file_ext == '.txt':
        _write_txt_report(report, filename)
    elif file_ext == '.md':
        _write_markdown_report(report, filename)
    elif file_ext == '.html':
        _write_html_report(report, filename)
    elif file_ext == '.json':
        _write_json_report(report, filename)
    elif file_ext == '.sarif' or format == 'sarif':
        _write_sarif_report(report, filename)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")


def _write_txt_report(report, filename):
    content = [
        "Code Analysis Report",
        "=" * 80,
        report['summary'],
        "\nDetailed Findings:"
    ]
    for finding in report['detailed_findings']:
        content.append(f"\nFile: {finding['file']}")
        content.append("-" * 60)
        content.append(finding['result'])

    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))


def _write_html_report(report, filename):
    findings_html = "".join(
        f"""
        <div class="finding">
            <h3>{finding['file']}</h3>
            <pre>{finding['result']}</pre>
        </div>
        """
        for finding in report['detailed_findings']
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Code Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .finding {{ margin-bottom: 30px; border-left: 4px solid #007bff; padding-left: 15px; }}
            pre {{ background: #f8f9fa; padding: 15px; border-radius: 4px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; }}
        </style>
    </head>
    <body>
        <h1>Code Analysis Report</h1>
        <h2>Summary</h2>
        <pre>{report['summary']}</pre>
        <h2>Detailed Findings</h2>
        {findings_html}
    </body>
    </html>
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)


def _write_json_report(report, filename):
    report_data = {
        "summary": report['summary'],
        "findings": [
            {
                "file": f['file'],
                "result": f['result'],
                "severity": _detect_severity(f['result'])
            } for f in report['detailed_findings']
        ]
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)


def _detect_severity(text):
    text = text.lower()
    if 'critical' in text:
        return "critical"
    elif 'high' in text:
        return "high"
    elif 'medium' in text:
        return "medium"
    return "low"


def _write_markdown_report(report, filename):
    content = [
        "# Code Analysis Report",
        f"**Summary**\n{report['summary']}",
        "## Detailed Findings"
    ]

    for idx, finding in enumerate(report['detailed_findings'], 1):
        content.append(
            f"\n### Finding {idx}\n"
            f"**File**: `{finding['file']}`\n\n"
            f"```\n{finding['result']}\n```"
        )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

def _write_sarif_report(report, filename):
    sarif_template = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "CodeAnalyzer",
                    "version": __version__,
                    "rules": []
                }
            },
            "results": []
        }]
    }

    for idx, finding in enumerate(report['detailed_findings']):
        sarif_template["runs"][0]["results"].append({
            "ruleId": f"CA{idx:04d}",
            "message": {
                "text": finding['result']
            },
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": finding['file']
                    }
                }
            }],
            "level": "error" if 'critical' in finding['result'].lower() else "warning"
        })

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sarif_template, f, indent=2)