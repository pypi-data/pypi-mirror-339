#!/usr/bin/env python3
"""
GitHub Commit Log Analyzer CLI Tool

A command-line tool for analyzing Git repository commit logs,
generating reports, and providing AI-powered insights.
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

from cli_tool.analyzer import GitAnalyzer
from cli_tool.report_generator import generate_report
from cli_tool.ai_analyzer import init_openai_client, analyze_with_ai

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def setup_argparser() -> argparse.ArgumentParser:
    """Set up the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="GitHub Commit Log Analyzer - Analyze commit history and generate reports",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        "--repo-path", 
        type=str, 
        default=".", 
        help="Path to the Git repository (defaults to current directory)"
    )
    
    # Date range filtering
    parser.add_argument(
        "--start-date", 
        type=str, 
        help="Start date for commit analysis (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date", 
        type=str, 
        help="End date for commit analysis (YYYY-MM-DD)"
    )
    
    # Output configuration
    parser.add_argument(
        "--output-format", 
        type=str, 
        choices=["text", "markdown", "html", "pdf"], 
        default="text", 
        help="Output format for the report"
    )
    parser.add_argument(
        "--output-file", 
        type=str, 
        help="Path to save the output report (default: print to stdout for text/markdown)"
    )
    parser.add_argument(
        "--simple-output", 
        action="store_true", 
        help="Generate a simplified report (for large repositories)"
    )
    
    # AI analysis options
    parser.add_argument(
        "--prompt-config", 
        type=str, 
        help="Path to JSON file with custom prompt configurations for AI analysis"
    )
    parser.add_argument(
        "--openai-api-key", 
        type=str, 
        help="OpenAI API key (can also be set via OPENAI_API_KEY environment variable)"
    )
    
    # Advanced options
    advanced_group = parser.add_argument_group("Advanced Options")
    advanced_group.add_argument(
        "--max-commits", 
        type=int, 
        help="Maximum number of commits to analyze (for large repositories)"
    )
    
    return parser


def load_prompt_config(config_file: str) -> Dict[str, str]:
    """
    Load prompt configuration from a JSON file.
    
    Args:
        config_file: Path to the JSON configuration file
        
    Returns:
        Dictionary containing prompt configurations
    """
    if not os.path.exists(config_file):
        logger.error(f"Prompt configuration file not found: {config_file}")
        return {}
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"Loaded prompt configuration from {config_file}")
        return config
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in prompt configuration file: {config_file}")
        return {}
    except Exception as e:
        logger.error(f"Error loading prompt configuration: {str(e)}")
        return {}


def main():
    """Main entry point for the command-line tool."""
    # Set up and parse command-line arguments
    parser = setup_argparser()
    args = parser.parse_args()
    
    try:
        # Validate repository path
        if not os.path.exists(args.repo_path):
            logger.error(f"Repository path does not exist: {args.repo_path}")
            sys.exit(1)
        
        # Initialize the Git analyzer
        logger.info(f"Analyzing repository at {args.repo_path}")
        try:
            analyzer = GitAnalyzer(
                repo_path=args.repo_path,
                start_date=args.start_date,
                end_date=args.end_date
            )
        except ValueError as e:
            logger.error(f"Error initializing Git analyzer: {str(e)}")
            sys.exit(1)
        
        # Analyze commit history
        commit_data = analyzer.analyze_commits(max_commits=args.max_commits)
        if not commit_data:
            logger.error("No commits found in the specified date range")
            sys.exit(1)
        
        logger.info(f"Analyzed {len(commit_data)} commits")
        
        # Generate repository statistics
        stats = analyzer.generate_stats(commit_data)
        if "error" in stats:
            logger.error(f"Error generating statistics: {stats['error']}")
            sys.exit(1)
        
        # Load prompt configuration if provided
        prompt_config = {}
        if args.prompt_config:
            prompt_config = load_prompt_config(args.prompt_config)
        
        # Initialize OpenAI client if API key provided
        ai_analysis = None
        if args.openai_api_key or "OPENAI_API_KEY" in os.environ:
            if init_openai_client(args.openai_api_key):
                # Run AI analysis
                logger.info("Running AI analysis on commit data")
                ai_analysis = analyze_with_ai(commit_data, prompt_config)
        else:
            logger.warning("No OpenAI API key provided. AI analysis will be unavailable.")
        
        # Generate the report
        output_format = args.output_format.lower()
        result = generate_report(commit_data=commit_data, prompts=prompt_config)
        
        # Save to file if output file specified
        if args.output_file:
            try:
                with open(args.output_file, 'w', encoding='utf-8') as f:
                    f.write(result)
                logger.info(f"Report saved to {args.output_file}")
            except Exception as e:
                logger.error(f"Error writing report to {args.output_file}: {str(e)}")
                sys.exit(1)
        else:
            # Print to stdout if no output file specified
            print(result)
    
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 