# Git Repository Intelligence Platform

A powerful tool for analyzing Git repositories and extracting meaningful insights about development patterns, technical challenges, and team dynamics.

## Overview

The Git Repository Intelligence Platform is a comprehensive solution for understanding software development processes through Git commit history analysis. It extracts valuable intelligence from your repositories to help:

- Track development progression and identify key milestones
- Discover technical challenges and their solutions
- Analyze contributor dynamics and team collaboration patterns
- Evaluate code quality and development impact
- Generate comprehensive, easy-to-understand reports

## Features

- **Enhanced Git Analysis**: Advanced parsing of Git commits, with detailed extraction of changes, messages, and metadata
- **Milestone Detection**: Identification of significant project milestones and releases
- **Commit Clustering**: Grouping of related commits to understand development themes
- **Technical Challenge Detection**: Discovery of problems and their solutions within the codebase
- **Contributor Analysis**: Insights into team dynamics, contributions, and collaboration
- **Impact Analysis**: Measurement of code quality, development velocity, and improvement trends
- **LLM-Powered Insights**: Optional AI-generated observations and recommendations
- **Comprehensive Reports**: Generation of detailed Markdown and HTML reports

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/git-repo-intelligence.git
cd git-repo-intelligence
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Set up API key (optional for LLM insights):
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Quick Start

Use the provided quick demo script:

```bash
./quick_demo.sh /path/to/your/git/repository
```

Or run the main script directly:

```bash
./git_repo_intelligence.py --repo-path /path/to/your/repository --mock-llm --generate-html
```

## Usage Options

```
usage: git_repo_intelligence.py [-h] --repo-path REPO_PATH [--repo-name REPO_NAME]
                              [--start-date START_DATE] [--end-date END_DATE]
                              [--max-commits MAX_COMMITS]
                              [--min-cluster-size MIN_CLUSTER_SIZE]
                              [--cluster-distance CLUSTER_DISTANCE]
                              [--output-dir OUTPUT_DIR] [--save-json]
                              [--json-dir JSON_DIR] [--generate-html]
                              [--report-title REPORT_TITLE] [--api-key API_KEY]
                              [--model MODEL] [--mock-llm] [--skip-milestones]
                              [--skip-clustering] [--skip-challenges]
                              [--skip-contributors] [--skip-impact] [--verbose]
```

### Key Arguments

- `--repo-path`: Path to the Git repository (required)
- `--max-commits`: Maximum number of commits to analyze (default: 100)
- `--generate-html`: Generate HTML report in addition to Markdown
- `--mock-llm`: Use mock data instead of calling the OpenAI API
- `--save-json`: Save intermediate analysis results as JSON files

## Example Reports

After running the analysis, check the `reports` directory for generated reports:

- Markdown report: `reports/repository_name_date.md`
- HTML report: `reports/repository_name_date.html`

If `--save-json` is enabled, intermediate data is saved to the `data` directory.

## Components

The platform consists of several integrated components:

- **EnhancedGitAnalyzer**: Core Git data extraction
- **MilestoneDetector**: Project milestone identification
- **CommitClusterer**: Related commit grouping
- **TechnicalChallengeDetector**: Problem and solution analysis
- **ContributorAnalyzer**: Team and collaboration assessment
- **ImpactAnalyzer**: Development impact measurement
- **LLMAnalyzer**: AI-powered insights generation
- **ReportGenerator**: Comprehensive report creation

## Requirements

- Python 3.7+
- Git
- Required Python packages (see requirements.txt)
- OpenAI API key (optional for LLM insights)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.