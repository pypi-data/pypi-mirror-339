from typing import List, Dict, Any, Optional
import json
import os
import requests
from datetime import datetime

class LLMAnalyzer:
    """
    Analyzes repository data using Large Language Models to generate
    comprehensive insights and summaries.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the LLM analyzer
        
        Args:
            api_key: API key for the LLM service (defaults to env var)
            model: Model to use for analysis
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("No API key provided and OPENAI_API_KEY environment variable not set")
        
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze_repository(self, 
                          commits: List[Dict[str, Any]],
                          milestones: List[Dict[str, Any]],
                          challenges: List[Dict[str, Any]],
                          contributor_data: Dict[str, Any],
                          impact_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive repository insights using LLM
        
        Args:
            commits: List of commit data
            milestones: List of milestone data
            challenges: List of technical challenge data
            contributor_data: Contributor analysis data
            impact_data: Impact analysis data
            
        Returns:
            Dictionary containing generated insights
        """
        # Prepare context for the LLM
        context = self._prepare_context(commits, milestones, challenges, 
                                        contributor_data, impact_data)
        
        # Generate insights using LLM
        insights = self._run_llm_analysis(context)
        
        return insights
    
    def _prepare_context(self, 
                        commits: List[Dict[str, Any]],
                        milestones: List[Dict[str, Any]],
                        challenges: List[Dict[str, Any]],
                        contributor_data: Dict[str, Any],
                        impact_data: Dict[str, Any]) -> str:
        """
        Prepare repository data as context for the LLM
        """
        # Format repository summary statistics
        summary_stats = self._format_summary_stats(commits)
        
        # Format important milestones
        milestones_data = self._format_milestones_data(milestones)
        
        # Format technical challenges
        challenges_data = self._format_challenges_data(challenges)
        
        # Format commit patterns
        commit_data = self._format_commit_data(commits)
        
        # Combine all formatted data
        context = f"""
# Repository Analysis Summary

## Repository Statistics
{summary_stats}

## Development Timeline and Milestones
{milestones_data}

## Technical Challenges and Solutions
{challenges_data}

## Commit Patterns
{commit_data}

## Team Collaboration Insights
Team Size: {contributor_data.get('team_metrics', {}).get('total_contributors', 0)} contributors
Average Commits per Contributor: {contributor_data.get('team_metrics', {}).get('avg_commits_per_contributor', 0)}
Collaboration Density: {contributor_data.get('team_metrics', {}).get('collaboration_density', 0)}

## Code Quality Metrics
Quality Score: {impact_data.get('quality_metrics', {}).get('quality_score', 0)}/5.0
Bug Frequency: {impact_data.get('quality_metrics', {}).get('bug_frequency', 0)}%
Refactor Frequency: {impact_data.get('quality_metrics', {}).get('refactor_frequency', 0)}%
Churn Trend: {impact_data.get('quality_metrics', {}).get('churn_trend', 0)}%
"""
        
        return context
    
    def _format_summary_stats(self, commits: List[Dict[str, Any]]) -> str:
        """Format repository summary statistics"""
        if not commits:
            return "No commits available."
            
        # Calculate date range
        dates = [commit['date'] for commit in commits if isinstance(commit.get('date'), datetime)]
        if dates:
            first_date = min(dates)
            last_date = max(dates)
            date_range = f"{first_date.strftime('%Y-%m-%d')} to {last_date.strftime('%Y-%m-%d')}"
        else:
            date_range = "Unknown"
            
        # Count unique contributors
        contributors = set(commit.get('author_name', 'Unknown') for commit in commits)
        
        # Count modified files
        files = set()
        for commit in commits:
            for file in commit.get('modified_files', []):
                files.add(file.get('path', ''))
                
        # Calculate statistics
        stats = f"""
- Total Commits: {len(commits)}
- Date Range: {date_range}
- Contributors: {len(contributors)}
- Files Modified: {len(files)}
- Average Lines per Commit: {sum(commit.get('stats', {}).get('lines_added', 0) + commit.get('stats', {}).get('lines_removed', 0) for commit in commits) / len(commits) if commits else 0:.1f}
"""
        return stats
    
    def _format_commit_data(self, commits: List[Dict[str, Any]]) -> str:
        """Format commit patterns data"""
        if not commits:
            return "No commits available."
            
        # Count commit types
        commit_types = {}
        for commit in commits:
            ctypes = commit.get('commit_type', [])
            if isinstance(ctypes, str):
                ctypes = [ctypes]
                
            for ctype in ctypes:
                if ctype in commit_types:
                    commit_types[ctype] += 1
                else:
                    commit_types[ctype] = 1
                    
        # Format commit type distribution
        commit_type_str = "\n".join([f"- {ctype}: {count} ({count/len(commits)*100:.1f}%)" 
                                    for ctype, count in sorted(commit_types.items(), 
                                                             key=lambda x: x[1], 
                                                             reverse=True)])
        
        # Sample important commits (first, last and some in between)
        sample_size = min(5, len(commits))
        sample_indices = [0]  # First commit
        
        if len(commits) > 1:
            sample_indices.append(len(commits) - 1)  # Last commit
            
            # Add some commits in between if there are more than 2 commits
            if len(commits) > 2:
                step = len(commits) // (sample_size - 1)
                for i in range(1, sample_size - 1):
                    sample_indices.append(i * step)
                    
        # Remove duplicates and sort
        sample_indices = sorted(set(sample_indices))
        
        # Format sample commits
        sample_commits = []
        for idx in sample_indices:
            commit = commits[idx]
            date_str = commit['date'].strftime('%Y-%m-%d') if isinstance(commit.get('date'), datetime) else 'Unknown'
            sample_commits.append(f"- {date_str}: {commit.get('message', 'No message')[:100]}")
            
        sample_commits_str = "\n".join(sample_commits)
        
        return f"""
### Commit Type Distribution
{commit_type_str}

### Sample Key Commits
{sample_commits_str}
"""
    
    def _format_challenges_data(self, challenges: List[Dict[str, Any]]) -> str:
        """Format technical challenges data"""
        if not challenges:
            return "No significant technical challenges detected."
            
        challenges_text = []
        
        for i, challenge in enumerate(challenges[:5], 1):  # Limit to top 5 challenges
            problem = challenge.get('problem', {})
            solutions = challenge.get('solutions', [])
            
            challenge_text = f"### Challenge {i}: {problem.get('title', 'Untitled')}\n"
            challenge_text += f"- Difficulty: {problem.get('difficulty', 'Unknown')}\n"
            challenge_text += f"- First Identified: {problem.get('date').strftime('%Y-%m-%d') if isinstance(problem.get('date'), datetime) else 'Unknown'}\n"
            challenge_text += f"- Description: {problem.get('description', 'No description')}\n"
            
            # Add solutions if available
            if solutions:
                challenge_text += "\nSolutions:\n"
                for j, solution in enumerate(solutions[:3], 1):  # Limit to top 3 solutions
                    solution_date = solution.get('date')
                    date_str = solution_date.strftime('%Y-%m-%d') if isinstance(solution_date, datetime) else 'Unknown'
                    challenge_text += f"- Solution {j} ({date_str}): {solution.get('description', 'No description')[:100]}\n"
            
            challenges_text.append(challenge_text)
            
        return "\n".join(challenges_text)
    
    def _format_milestones_data(self, milestones: List[Dict[str, Any]]) -> str:
        """Format milestones data"""
        if not milestones:
            return "No significant milestones detected."
            
        milestones_text = []
        
        # Sort milestones by date
        sorted_milestones = sorted(milestones, 
                                 key=lambda x: x.get('date', datetime.min),
                                 reverse=False)
        
        for i, milestone in enumerate(sorted_milestones, 1):
            date = milestone.get('date')
            date_str = date.strftime('%Y-%m-%d') if isinstance(date, datetime) else 'Unknown'
            
            milestone_text = f"### Milestone {i}: {milestone.get('title', 'Untitled')}\n"
            milestone_text += f"- Date: {date_str}\n"
            milestone_text += f"- Type: {milestone.get('type', 'Unknown')}\n"
            milestone_text += f"- Summary: {milestone.get('summary', 'No summary')}\n"
            
            # Add key commits if available
            key_commits = milestone.get('key_commits', [])
            if key_commits:
                milestone_text += "\nKey Commits:\n"
                for j, commit in enumerate(key_commits[:3], 1):  # Limit to top 3 commits
                    milestone_text += f"- {commit.get('hash', '')[:7]}: {commit.get('message', 'No message')[:80]}\n"
            
            milestones_text.append(milestone_text)
            
        return "\n".join(milestones_text)
    
    def _run_llm_analysis(self, context: str) -> Dict[str, Any]:
        """
        Run LLM analysis on the prepared context
        
        Args:
            context: Formatted repository data context
            
        Returns:
            Dictionary containing generated insights
        """
        # Create prompts for different aspects of analysis
        prompts = {
            "overview": "Provide a concise 2-3 paragraph overview of the repository based on the analysis. Focus on the most important patterns, trends, and metrics.",
            
            "key_milestones": """Analyze the commit history to identify and describe the 3-5 most significant milestones in the project's development.
            
For each milestone, please:
1. Create a descriptive title based on the commit messages and code changes
2. Infer the milestone type (feature release, major refactoring, infrastructure update, etc.)
3. Provide an estimated date or date range when the milestone occurred
4. Describe its significance to the project's evolution

If milestone information is limited, infer them from patterns in the commit history, commit clusters, and file changes.""",
            
            "technical_achievements": """Identify the 3-5 most impressive technical achievements in the repository. 
            
For each achievement:
1. Create a descriptive title that captures the essence of the achievement
2. Explain what technical problem it solved
3. Describe why it's significant (performance improvement, better architecture, etc.)
4. Mention which files or components were impacted

Focus on the most impressive technical feats rather than routine development work. Look for large refactorings, optimizations, architecture improvements, and complex feature implementations.""",
            
            "challenges": """Identify and describe the main technical challenges the team faced during development based on commit messages, file changes, and code patterns.
            
For each significant challenge:
1. Create a descriptive title that captures the problem
2. Assess its difficulty level based on time to resolution and number of related commits
3. Explain what the challenge was and why it was difficult
4. Describe how it was eventually resolved

Pay special attention to commits with terms like 'fix', 'solve', 'workaround', 'issue', 'problem', etc., and examine sequences of commits that modify the same files.""",
            
            "team_dynamics": """Based on the contributor data, describe the team dynamics and collaboration patterns. Specifically address:
            
1. Team structure (core group vs. occasional contributors)
2. Collaboration patterns (who works on what, co-editing patterns)
3. Knowledge specialization and expertise areas
4. Communication and handoffs visible through commit patterns
5. Strengths and potential improvement areas in team dynamics""",
            
            "code_quality": """Assess the code quality and maintenance practices based on the metrics provided. Include analysis of:
            
1. Overall code quality score and what it indicates
2. Bug patterns and what they might reveal about testing practices
3. Refactoring practices and technical debt management
4. Code churn patterns and what they suggest about stability
5. Architectural decisions evident from the code and commits""",
            
            "recommendations": """Provide 3-5 specific, actionable recommendations to improve the codebase and development process. For each recommendation:
            
1. Clearly state what should be done
2. Explain why it would help based on the data you've analyzed
3. Suggest how the team might implement the recommendation
4. Describe the expected benefits

Focus on the most impactful improvements rather than minor issues."""
        }
        
        insights = {}
        
        # Generate insights for each prompt
        for aspect, prompt in prompts.items():
            full_prompt = f"{context}\n\n{prompt}"
            insights[aspect] = self._call_llm_api(full_prompt)
            
        return insights
    
    def _call_llm_api(self, prompt: str) -> str:
        """
        Call the LLM API with the given prompt
        
        Args:
            prompt: The prompt to send to the LLM API
            
        Returns:
            Generated text from the LLM
        """
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": """You are an expert software engineer and data scientist analyzing a git repository. Your task is to provide clear, insightful, and specific analysis based on commit history, code patterns, and development metrics.

Important guidelines:
1. When information is missing (like untitled milestones or challenges), use the context clues from commit messages, dates, and file changes to make reasonable inferences and provide descriptive titles and explanations.
2. Focus on patterns and trends rather than individual commits unless they're especially significant.
3. Be specific and practical in your insights - avoid vague generalizations.
4. When analyzing technical aspects, consider both the code and the development process.
5. Look for connections between different data points to tell a cohesive story about the repository's evolution.
6. Prioritize actionable insights that would be valuable to the development team."""},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1500
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"Error calling LLM API: {e}")
            return f"Error: Failed to generate insights - {str(e)}" 