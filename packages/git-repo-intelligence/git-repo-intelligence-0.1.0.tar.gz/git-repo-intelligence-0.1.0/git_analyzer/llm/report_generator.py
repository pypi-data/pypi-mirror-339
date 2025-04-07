from typing import Dict, Any, Optional, List
import json
import os
import datetime
import markdown
import re

class ReportGenerator:
    """
    Generates structured reports from repository analysis insights
    """
    
    def __init__(self, output_dir: str = './reports'):
        """
        Initialize the report generator
        
        Args:
            output_dir: Directory to save generated reports
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_markdown_report(self, 
                               repository_name: str,
                               commits_data: List[Dict[str, Any]],
                               milestones: List[Dict[str, Any]],
                               challenges: List[Dict[str, Any]],
                               contributor_data: Dict[str, Any],
                               impact_data: Dict[str, Any],
                               llm_insights: Dict[str, Any]) -> str:
        """
        Generate a comprehensive Markdown report
        
        Args:
            repository_name: Name of the repository
            commits_data: List of commit data
            milestones: List of milestone data
            challenges: List of technical challenge data
            contributor_data: Contributor analysis data
            impact_data: Impact analysis data
            llm_insights: LLM-generated insights
            
        Returns:
            Path to the generated report file
        """
        # Format current date for filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"{self.output_dir}/{self._clean_filename(repository_name)}_{timestamp}.md"
        
        # Build report content
        report_content = self._build_markdown_report(
            repository_name=repository_name,
            commits_data=commits_data,
            milestones=milestones,
            challenges=challenges,
            contributor_data=contributor_data,
            impact_data=impact_data,
            llm_insights=llm_insights
        )
        
        # Write report to file
        with open(report_filename, 'w') as f:
            f.write(report_content)
            
        return report_filename
    
    def generate_html_report(self, 
                           repository_name: str,
                           commits_data: List[Dict[str, Any]],
                           milestones: List[Dict[str, Any]],
                           challenges: List[Dict[str, Any]],
                           contributor_data: Dict[str, Any],
                           impact_data: Dict[str, Any],
                           llm_insights: Dict[str, Any]) -> str:
        """
        Generate an HTML report from the analysis data
        
        Args:
            Same as generate_markdown_report
            
        Returns:
            Path to the generated HTML report file
        """
        # Generate Markdown content first
        md_content = self._build_markdown_report(
            repository_name=repository_name,
            commits_data=commits_data,
            milestones=milestones,
            challenges=challenges,
            contributor_data=contributor_data,
            impact_data=impact_data,
            llm_insights=llm_insights
        )
        
        # Convert to HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        
        # Add CSS styling
        styled_html = self._add_html_styling(html_content)
        
        # Format current date for filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        html_filename = f"{self.output_dir}/{self._clean_filename(repository_name)}_{timestamp}.html"
        
        # Write HTML report to file
        with open(html_filename, 'w') as f:
            f.write(styled_html)
            
        return html_filename
    
    def _build_markdown_report(self,
                              repository_name: str,
                              commits_data: List[Dict[str, Any]],
                              milestones: List[Dict[str, Any]],
                              challenges: List[Dict[str, Any]],
                              contributor_data: Dict[str, Any],
                              impact_data: Dict[str, Any],
                              llm_insights: Dict[str, Any]) -> str:
        """Build the markdown report content"""
        # Report header
        report = f"# Git Repository Analysis: {repository_name}\n\n"
        report += f"*Report generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        report += "---\n\n"
        
        # Executive Summary section
        report += "## Executive Summary\n\n"
        report += llm_insights.get('overview', 'No overview available.') + "\n\n"
        
        # Add quality score and metrics
        quality_score = impact_data.get('quality_metrics', {}).get('quality_score', 0)
        report += f"**Repository Quality Score:** {quality_score}/5.0\n\n"
        
        # Key metrics table
        report += "### Key Metrics\n\n"
        report += "| Metric | Value |\n"
        report += "| ------ | ----- |\n"
        
        # Add metrics from impact data
        baseline = impact_data.get('baseline_metrics', {})
        report += f"| Total Commits | {baseline.get('total_commits', 0)} |\n"
        
        team_metrics = contributor_data.get('team_metrics', {})
        report += f"| Contributors | {team_metrics.get('total_contributors', 0)} |\n"
        report += f"| Avg. Commits per Contributor | {team_metrics.get('avg_commits_per_contributor', 0)} |\n"
        
        quality_metrics = impact_data.get('quality_metrics', {})
        report += f"| Bug Frequency | {quality_metrics.get('bug_frequency', 0)}% |\n"
        report += f"| Refactor Frequency | {quality_metrics.get('refactor_frequency', 0)}% |\n"
        
        # Development velocity
        velocity = baseline.get('development_velocity', {})
        report += f"| Development Velocity | {velocity.get('trend', 'Unknown')} |\n\n"
        
        # Key Milestones section
        report += "## Key Milestones\n\n"
        report += llm_insights.get('key_milestones', 'No milestone insights available.') + "\n\n"
        
        # Add milestone details
        if milestones:
            report += "### Milestone Details\n\n"
            
            # Sort milestones by date
            sorted_milestones = sorted(milestones, 
                                       key=lambda x: x.get('date', datetime.datetime.min))
            
            for i, milestone in enumerate(sorted_milestones[:5], 1):  # Top 5 milestones
                title = milestone.get('title', milestone.get('description', 'Untitled'))
                milestone_type = milestone.get('type', 'Unknown')
                date = milestone.get('date')
                summary = milestone.get('summary', 'No summary available.')
                
                if isinstance(date, datetime.datetime):
                    date_str = date.strftime('%Y-%m-%d')
                else:
                    date_str = str(date)
                
                report += f"**{i}. {title} ({milestone_type})**\n\n"
                report += f"- Date: {date_str}\n"
                report += f"- Summary: {summary}\n\n"
        
        # Technical Achievements section
        report += "## Technical Achievements\n\n"
        report += llm_insights.get('technical_achievements', 'No technical achievement insights available.') + "\n\n"
        
        # Technical Challenges section
        report += "## Technical Challenges\n\n"
        report += llm_insights.get('challenges', 'No challenge insights available.') + "\n\n"
        
        # Add challenge details
        if challenges:
            report += "### Challenge Details\n\n"
            
            for i, challenge in enumerate(challenges[:3], 1):  # Top 3 challenges
                problem = challenge.get('problem', {})
                title = problem.get('title', challenge.get('title', 'Untitled'))
                difficulty = problem.get('difficulty', challenge.get('difficulty', 'Unknown'))
                description = problem.get('description', 'No description available.')
                
                report += f"**{i}. {title} (Difficulty: {difficulty})**\n\n"
                report += f"{description}\n\n"
                
                # Add solutions if available
                solutions = challenge.get('solutions', [])
                if solutions:
                    report += "**Solutions:**\n\n"
                    for j, solution in enumerate(solutions[:2], 1):  # Top 2 solutions
                        solution_desc = solution.get('description', 'No description available.')
                        
                        # Include solution date if available
                        if solution.get('date'):
                            solution_date = solution.get('date')
                            if isinstance(solution_date, datetime.datetime):
                                date_str = solution_date.strftime('%Y-%m-%d')
                                solution_desc = f"({date_str}) {solution_desc}"
                        
                        report += f"{j}. {solution_desc}\n\n"
        
        # Team Dynamics section
        report += "## Team Dynamics\n\n"
        report += llm_insights.get('team_dynamics', 'No team dynamics insights available.') + "\n\n"
        
        # Add contributor details
        profiles = contributor_data.get('contributor_profiles', {})
        if profiles:
            report += "### Key Contributors\n\n"
            
            # Sort contributors by commit count
            sorted_contributors = sorted(profiles.items(), 
                                        key=lambda x: x[1].get('commit_count', 0), 
                                        reverse=True)
            
            for i, (name, profile) in enumerate(sorted_contributors[:3], 1):  # Top 3 contributors
                commit_count = profile.get('commit_count', 0)
                report += f"**{i}. {name} ({commit_count} commits)**\n\n"
                
                # Expertise areas
                expertise_areas = profile.get('expertise_areas', [])
                if expertise_areas:
                    report += "Expertise:\n"
                    for area in expertise_areas:
                        report += f"- {area.get('area', 'Unknown')} ({area.get('level', 'low')} level)\n"
                    report += "\n"
                
                # Activity timeline
                activity = profile.get('activity_by_month', {})
                if activity:
                    report += "Activity: "
                    report += ", ".join([f"{month}: {count}" for month, count in activity.items()]) + "\n\n"
        
        # Code Quality section
        report += "## Code Quality Assessment\n\n"
        report += llm_insights.get('code_quality', 'No code quality insights available.') + "\n\n"
        
        # Quality metrics details
        report += "### Quality Metrics\n\n"
        report += "| Metric | Value |\n"
        report += "| ------ | ----- |\n"
        report += f"| Quality Score | {quality_metrics.get('quality_score', 0)}/5.0 |\n"
        report += f"| Bug Frequency | {quality_metrics.get('bug_frequency', 0)}% |\n"
        report += f"| Refactor Frequency | {quality_metrics.get('refactor_frequency', 0)}% |\n"
        report += f"| Average Challenge Impact | {quality_metrics.get('avg_challenge_impact', 0)} |\n"
        report += f"| Churn Trend | {quality_metrics.get('churn_trend', 0)}% |\n\n"
        
        # Recommendations section
        report += "## Recommendations\n\n"
        report += llm_insights.get('recommendations', 'No recommendations available.') + "\n\n"
        
        # Appendix with data sources
        report += "## Appendix: Analysis Methods\n\n"
        report += "This report was generated using the Git Repository Intelligence Platform, " 
        report += "which analyzes git repositories to extract insights about development patterns, "
        report += "technical challenges, code quality, and team dynamics.\n\n"
        
        report += "The analysis leverages a combination of Git commit history analysis, natural language processing, "
        report += "and machine learning to identify patterns and generate insights. Large Language Models were used "
        report += "to synthesize the data and provide additional context and recommendations.\n\n"
        
        # Footer
        report += "---\n\n"
        report += "*Generated by Git Repository Intelligence Platform*\n"
        
        return report
    
    def _add_html_styling(self, html_content: str) -> str:
        """Add CSS styling to the HTML report"""
        # HTML document structure with CSS
        styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git Repository Analysis Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f8f9fa;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 2rem;
        }}
        h1 {{
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
        }}
        h2 {{
            border-bottom: 1px solid #ddd;
            padding-bottom: 0.3rem;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
        }}
        th, td {{
            text-align: left;
            padding: 0.75rem;
            border: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        code {{
            background-color: #f7f7f7;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: monospace;
        }}
        pre {{
            background-color: #f7f7f7;
            padding: 1rem;
            overflow-x: auto;
            border-radius: 4px;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 1rem;
            margin-left: 0;
            color: #555;
        }}
        hr {{
            border: 0;
            border-top: 1px solid #eee;
            margin: 2rem 0;
        }}
        .header {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .footer {{
            text-align: center;
            margin-top: 2rem;
            color: #777;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🔍 Git Repository Intelligence Platform</div>
    </div>
    
    {html_content}
    
    <div class="footer">
        <p>Generated by Git Repository Intelligence Platform | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
</body>
</html>
"""
        return styled_html
    
    def _clean_filename(self, filename: str) -> str:
        """Convert string to a valid filename"""
        # Replace invalid characters with underscores
        return re.sub(r'[^\w\-_.]', '_', filename) 