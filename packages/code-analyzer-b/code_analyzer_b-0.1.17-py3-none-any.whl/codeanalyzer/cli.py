import argparse
import sys
import os
import shutil
import configparser
import asyncio
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


async def analyze_command_async(args):
    repo_path = args.target
    is_temp_dir = False
    try:
        if not os.path.exists(repo_path):
            repo_path = download_repo(repo_path, git_token=args.git_token)
            is_temp_dir = True
        else:
            if not args.stream:  # Only show this when not streaming
                print(f"Scanning local directory: {repo_path}")

        files = scan_files(repo_path)
        if not args.stream:  # Only show count when not streaming
            print(f"📁 Found {len(files)} files to analyze")

        async with CodeAnalyzer() as analyzer:
            await analyzer.analyze_project(files, max_concurrent=4)

            if analyzer.stats.get('errors', 0) > 0:
                print(f"::warning::{analyzer.stats['errors']} files had analysis errors")

            report = await analyzer.generate_report(
                include_details=not args.no_details,
                stream=args.stream  # Pass stream flag to report generation
            )

            if args.output:
                write_report(report, args.output, args.format, include_details=not args.no_details)
                if not args.stream:  # Only show success message when not streaming
                    print(f"\n✅ Report saved to {args.output}")
            else:
                if args.stream:  # Only print details when streaming
                    print("\n📝 Final Summary:")
                    print("=" * 80)
                    print(report['summary'])
                    if report.get('detailed_findings'):
                        print("\n🔍 Detailed Findings:")
                        for finding in report['detailed_findings']:
                            print(f"\nFile: {finding['file']}")
                            print("-" * 80)
                            print(finding['result'])
                    else:
                        print("\n✅ No significant issues found")

    except Exception as e:
        print(f"::error::{str(e)}")
        sys.exit(1)
    finally:
        if is_temp_dir and repo_path and os.path.exists(os.path.dirname(repo_path)):
            shutil.rmtree(os.path.dirname(repo_path), ignore_errors=True)

def analyze_command(args):
    print(f"\n🔍 Starting analysis of {args.target}")
    asyncio.run(analyze_command_async(args))


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
    analyze_parser.add_argument(
        '--no-details',
        action='store_true',
        help='Disable detailed findings in report (summary only)'
    )
    analyze_parser.add_argument(
        '-s', '--stream',
        action='store_true',
        help='Enable real-time streaming of analysis results'
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