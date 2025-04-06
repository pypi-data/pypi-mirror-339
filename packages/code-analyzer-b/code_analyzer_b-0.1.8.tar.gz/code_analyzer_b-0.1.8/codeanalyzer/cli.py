import argparse
import sys
import os
import shutil
import configparser
from .utils import download_repo, scan_files, write_report
from .analyzer import CodeAnalyzer
from . import __version__


def setup_command(args):
    print("Initializing code analyzer setup...")
    api_key = input("Please enter your DeepSeek API key: ").strip()
    if not api_key:
        print("Error: API key cannot be empty.")
        sys.exit(1)

    config_dir = os.path.expanduser("~/.code_analyzer")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.ini")

    config = configparser.ConfigParser()
    config["DEEPSEEK"] = {"API_KEY": api_key}

    with open(config_path, "w") as f:
        config.write(f)

    print(f"Setup complete. API key saved to {config_path}")


def analyze_command(args):
    print(f"\n🔍 Starting analysis of {args.target}")
    repo_path = args.target
    try:
        if not os.path.exists(repo_path):
            repo_path = download_repo(repo_path, git_token=args.git_token)
        else:
            print(f"Scanning local directory: {repo_path}")

        files = scan_files(repo_path)
        print(f"📁 Found {len(files)} files to analyze")

        analyzer = CodeAnalyzer()
        analyzer.analyze_project(files)
        report = analyzer.generate_report()

        if args.output:
            write_report(report, args.output, args.format)
            print(f"\n✅ Report saved to {args.output}")
        else:
            print("\n📝 Final Summary:")
            print("=" * 80)
            print(report['summary'])
            if report['detailed_findings']:
                print("\n🔍 Detailed Findings:")
                for finding in report['detailed_findings']:
                    print(f"\nFile: {finding['file']}")
                    print("-" * 80)
                    print(finding['result'])
            else:
                print("\n✅ No significant issues found")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    finally:
        if repo_path and os.path.exists(os.path.dirname(repo_path)):
            shutil.rmtree(os.path.dirname(repo_path))

def main():
    parser = argparse.ArgumentParser(prog="code_analyzer")
    subparsers = parser.add_subparsers()

    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Initial setup')
    setup_parser.set_defaults(func=setup_command)

    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze a repository',
        formatter_class=argparse.RawTextHelpFormatter,
        description="Analyze a GitHub repository for security vulnerabilities"
    )
    analyze_parser.add_argument(
        'target',
        help='GitHub repository URL or local directory path'
    )
    analyze_parser.add_argument(
        '--git-token',
        help='GitHub access token for private repositories\n'
             '(create at: https://github.com/settings/tokens)'
    )
    analyze_parser.add_argument(
        '-o', '--output',
        help='Output file path for report\n'
             '(supports .txt, .md, .html, .json, .sarif)'
    )
    analyze_parser.add_argument(
        '-f', '--format',
        choices=['txt', 'md', 'html', 'json', 'sarif'],
        default='txt',
        help='Output format for the report\n'
             '(default: autodetect from output file extension)'
    )

    # Version and main help
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    analyze_parser.set_defaults(func=analyze_command)
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()