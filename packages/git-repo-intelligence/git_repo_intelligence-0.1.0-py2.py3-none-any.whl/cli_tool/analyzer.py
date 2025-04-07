"""
Core analyzer for GitHub commit log analyzer.

This module provides functionality to analyze git repositories
and extract useful information from their commit history.
"""

import os
import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from collections import Counter, defaultdict

import git

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Regular expressions for keyword extraction
KEYWORD_PATTERNS = {
    "feature": r'\b(?:feature|feat|add|implement|new)\b',
    "bugfix": r'\b(?:fix|bug|issue|problem|error|resolve)\b',
    "refactor": r'\b(?:refactor|clean|improve|enhance|optimization)\b',
    "documentation": r'\b(?:doc|documentation|comment|readme)\b',
    "test": r'\b(?:test|spec|check|verify)\b',
    "chore": r'\b(?:chore|maintenance|housekeeping|update|upgrade|dependency|version)\b',
    "style": r'\b(?:style|format|lint|prettier|eslint|typo)\b',
    "performance": r'\b(?:performance|perf|speed|optimize|fast)\b',
    "ci": r'\b(?:ci|build|jenkins|github action|workflow|pipeline|travis|circle)\b',
    "security": r'\b(?:security|secure|vulnerability|auth|privacy|encrypt)\b'
}


class GitAnalyzer:
    """Analyzer for Git repositories"""

    def __init__(self, repo_path: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """
        Initialize the Git analyzer.
        
        Args:
            repo_path: Path to the git repository
            start_date: Optional start date for filtering commits (YYYY-MM-DD)
            end_date: Optional end date for filtering commits (YYYY-MM-DD)
        """
        self.repo_path = os.path.abspath(repo_path)
        self.start_date = self._parse_date(start_date) if start_date else None
        self.end_date = self._parse_date(end_date, end_of_day=True) if end_date else None
        self.repo = None
        
        try:
            self.repo = git.Repo(self.repo_path)
            logger.info(f"Successfully opened repository at {self.repo_path}")
        except git.exc.InvalidGitRepositoryError:
            logger.error(f"Invalid git repository: {self.repo_path}")
            raise ValueError(f"Invalid git repository: {self.repo_path}")
        except git.exc.NoSuchPathError:
            logger.error(f"Repository path does not exist: {self.repo_path}")
            raise ValueError(f"Repository path does not exist: {self.repo_path}")
        except Exception as e:
            logger.error(f"Error opening repository: {str(e)}")
            raise

    @staticmethod
    def _parse_date(date_string: str, end_of_day: bool = False) -> datetime:
        """
        Parse date string in YYYY-MM-DD format.
        
        Args:
            date_string: Date string to parse
            end_of_day: If True, set time to 23:59:59
            
        Returns:
            datetime object
        """
        try:
            date = datetime.strptime(date_string, "%Y-%m-%d")
            if end_of_day:
                date = date.replace(hour=23, minute=59, second=59)
            return date
        except ValueError:
            raise ValueError(f"Invalid date format: {date_string}. Expected format: YYYY-MM-DD")

    def analyze_commits(self, max_commits: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Analyze the commit history of the repository.
        
        Args:
            max_commits: Optional maximum number of commits to analyze
            
        Returns:
            List of dictionaries with commit information
        """
        if not self.repo:
            logger.error("Repository is not initialized")
            return []

        try:
            commit_data = []
            commits = self._get_filtered_commits(max_commits)
            
            logger.info(f"Analyzing {len(commits)} commits")
            
            # Process each commit
            for commit in commits:
                commit_info = self._process_commit(commit)
                if commit_info:
                    commit_data.append(commit_info)
            
            logger.info(f"Analyzed {len(commit_data)} commits")
            return commit_data
            
        except Exception as e:
            logger.error(f"Error analyzing commits: {str(e)}")
            raise

    def _get_filtered_commits(self, max_commits: Optional[int] = None) -> List[git.Commit]:
        """
        Get commits filtered by date range.
        
        Args:
            max_commits: Optional maximum number of commits to return
            
        Returns:
            List of git.Commit objects
        """
        try:
            # Get all commits
            all_commits = list(self.repo.iter_commits())
            
            # Apply date filters if provided
            filtered_commits = []
            for commit in all_commits:
                commit_date = datetime.fromtimestamp(commit.committed_date)
                
                # Check if commit is within date range
                if self.start_date and commit_date < self.start_date:
                    continue
                if self.end_date and commit_date > self.end_date:
                    continue
                    
                filtered_commits.append(commit)
            
            # Apply max_commits limit if provided
            if max_commits and len(filtered_commits) > max_commits:
                filtered_commits = filtered_commits[:max_commits]
            
            return filtered_commits
            
        except Exception as e:
            logger.error(f"Error filtering commits: {str(e)}")
            raise

    def _process_commit(self, commit: git.Commit) -> Dict[str, Any]:
        """
        Process a single commit to extract information.
        
        Args:
            commit: git.Commit object to process
            
        Returns:
            Dictionary with commit information
        """
        try:
            # Extract basic commit info
            commit_date = datetime.fromtimestamp(commit.committed_date)
            
            # Get commit stats
            stats = self._extract_commit_stats(commit)
            
            # Extract keywords from commit message
            keywords = self._extract_keywords(commit.message)
            
            # Build the commit information dictionary
            commit_info = {
                "hash": str(commit.hexsha),
                "short_hash": str(commit.hexsha)[:7],
                "author": f"{commit.author.name} <{commit.author.email}>",
                "date": commit_date,
                "message": commit.message,
                "stats": stats,
                "keywords": keywords
            }
            
            return commit_info
            
        except Exception as e:
            logger.warning(f"Error processing commit {commit.hexsha}: {str(e)}")
            return None

    def _extract_commit_stats(self, commit: git.Commit) -> Dict[str, Any]:
        """
        Extract statistics from a commit.
        
        Args:
            commit: git.Commit object
            
        Returns:
            Dictionary with commit statistics
        """
        try:
            # Initialize stats
            stats = {
                "lines_added": 0,
                "lines_removed": 0,
                "files_changed": 0,
                "file_types": defaultdict(int)
            }
            
            # Get the commit diff
            try:
                diff_index = commit.diff(commit.parents[0] if commit.parents else git.NULL_TREE)
            except (IndexError, git.exc.GitCommandError):
                # For initial commit or other special cases
                diff_index = commit.diff(git.NULL_TREE)
            
            # Process each file in the diff
            for diff in diff_index:
                stats["files_changed"] += 1
                
                # Extract file extension
                if diff.a_path:
                    ext = os.path.splitext(diff.a_path)[1].lower() or "no_extension"
                    stats["file_types"][ext] += 1
                elif diff.b_path:
                    ext = os.path.splitext(diff.b_path)[1].lower() or "no_extension"
                    stats["file_types"][ext] += 1
                
                # Get lines added/removed
                try:
                    if hasattr(diff, "stats"):
                        file_stats = diff.stats
                        stats["lines_added"] += file_stats.get("insertions", 0)
                        stats["lines_removed"] += file_stats.get("deletions", 0)
                except:
                    pass  # Skip if we can't get stats for this file
            
            return stats
            
        except Exception as e:
            logger.warning(f"Error extracting stats from commit {commit.hexsha}: {str(e)}")
            return {
                "lines_added": 0,
                "lines_removed": 0,
                "files_changed": 0,
                "file_types": {}
            }

    def _extract_keywords(self, commit_message: str) -> List[str]:
        """
        Extract keywords from commit message.
        
        Args:
            commit_message: Commit message text
            
        Returns:
            List of keywords found in the message
        """
        keywords = []
        
        # Check each keyword pattern against the commit message
        for category, pattern in KEYWORD_PATTERNS.items():
            if re.search(pattern, commit_message, re.IGNORECASE):
                keywords.append(category)
        
        return keywords

    def generate_stats(self, commit_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate statistics from commit data.
        
        Args:
            commit_data: List of commit dictionaries from analyze_commits()
            
        Returns:
            Dictionary with repository statistics
        """
        if not commit_data:
            return {
                "error": "No commit data provided or no commits found in the specified date range."
            }

        try:
            stats = {
                "total_commits": len(commit_data),
                "date_range": {
                    "start": min(c["date"] for c in commit_data),
                    "end": max(c["date"] for c in commit_data)
                },
                "authors": self._count_authors(commit_data),
                "keywords": self._count_keywords(commit_data),
                "file_types": self._aggregate_file_types(commit_data),
                "activity": self._analyze_activity(commit_data),
                "lines_changed": {
                    "added": sum(c["stats"]["lines_added"] for c in commit_data),
                    "removed": sum(c["stats"]["lines_removed"] for c in commit_data),
                    "total": sum(c["stats"]["lines_added"] + c["stats"]["lines_removed"] for c in commit_data)
                },
                "files_changed": sum(c["stats"]["files_changed"] for c in commit_data)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error generating statistics: {str(e)}")
            return {"error": f"Error generating statistics: {str(e)}"}

    def _count_authors(self, commit_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count commits by author."""
        author_counts = Counter()
        for commit in commit_data:
            author = commit["author"].split('<')[0].strip()
            author_counts[author] += 1
        
        # Convert to regular dict for better json serialization
        return dict(author_counts)

    def _count_keywords(self, commit_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count keyword occurrences across all commits."""
        keyword_counts = Counter()
        for commit in commit_data:
            for keyword in commit["keywords"]:
                keyword_counts[keyword] += 1
        
        return dict(keyword_counts)

    def _aggregate_file_types(self, commit_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Aggregate file types across all commits."""
        file_types = Counter()
        for commit in commit_data:
            for ext, count in commit["stats"]["file_types"].items():
                file_types[ext] += count
        
        return dict(file_types)

    def _analyze_activity(self, commit_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze commit activity by date."""
        activity_by_date = Counter()
        for commit in commit_data:
            date_str = commit["date"].strftime("%Y-%m-%d")
            activity_by_date[date_str] += 1
        
        return dict(activity_by_date) 