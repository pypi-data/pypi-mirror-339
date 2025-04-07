from git import Repo, Git
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime
import re
from typing import List, Dict, Any, Tuple, Optional

class EnhancedGitAnalyzer:
    """Enhanced analyzer for Git repositories with advanced pattern recognition"""
    
    def __init__(self, repo_path: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """Initialize with repository path and optional date range"""
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        
        # Patterns for analysis
        self.version_pattern = re.compile(r'v?\d+\.\d+\.\d+')
        self.feature_pattern = re.compile(r'(?i)add|feature|implement|support')
        self.bugfix_pattern = re.compile(r'(?i)fix|bug|issue|error|crash|problem')
        self.refactor_pattern = re.compile(r'(?i)refactor|clean|improve|optimize|simplify')
        
    def extract_all_commits(self) -> List[Dict[str, Any]]:
        """Extract detailed information from all commits in the specified range"""
        commits_data = []
        for commit in self.repo.iter_commits():
            commit_date = datetime.fromtimestamp(commit.committed_date)
            
            # Apply date filtering if specified
            if self.start_date and commit_date < self.start_date:
                continue
            if self.end_date and commit_date > self.end_date:
                continue
                
            # Extract basic commit info
            commit_info = {
                'hash': commit.hexsha,
                'short_hash': commit.hexsha[:7],
                'author_name': commit.author.name,
                'author_email': commit.author.email,
                'date': commit_date,
                'message': commit.message,
                'is_merge': len(commit.parents) > 1,
                'parent_count': len(commit.parents),
                'stats': self._extract_commit_stats(commit),
                'modified_files': self._get_modified_files(commit),
                'commit_type': self._classify_commit(commit.message)
            }
            
            # Extract version if present in commit message
            version_match = self.version_pattern.search(commit.message)
            if version_match:
                commit_info['version'] = version_match.group(0)
            
            commits_data.append(commit_info)
            
        return commits_data
    
    def _extract_commit_stats(self, commit) -> Dict[str, Any]:
        """Extract detailed statistics from a commit"""
        try:
            stats = commit.stats.total
            files_stats = commit.stats.files
            
            # Count file types
            file_types = defaultdict(int)
            for file_path in files_stats.keys():
                ext = self._get_file_extension(file_path)
                file_types[ext] += 1
                
            return {
                'lines_added': stats['insertions'],
                'lines_removed': stats['deletions'],
                'files_changed': stats['files'],
                'file_types': dict(file_types),
                'file_details': files_stats
            }
        except Exception as e:
            print(f"Error extracting stats for commit {commit.hexsha}: {str(e)}")
            return {
                'lines_added': 0,
                'lines_removed': 0,
                'files_changed': 0,
                'file_types': {},
                'file_details': {}
            }
    
    def _get_file_extension(self, file_path: str) -> str:
        """Extract file extension from path"""
        if '.' not in file_path:
            return 'no_extension'
        return file_path.split('.')[-1].lower()
    
    def _get_modified_files(self, commit) -> List[Dict[str, str]]:
        """Get detailed information about modified files"""
        if len(commit.parents) == 0:  # Initial commit
            return []
            
        parent = commit.parents[0]
        diffs = parent.diff(commit)
        
        modified_files = []
        for diff in diffs:
            change_type = 'added'
            if diff.deleted_file:
                change_type = 'deleted'
            elif diff.renamed:
                change_type = 'renamed'
            elif diff.a_path and diff.b_path:
                change_type = 'modified'
                
            file_info = {
                'path': diff.b_path or diff.a_path,
                'change_type': change_type
            }
            modified_files.append(file_info)
            
        return modified_files
    
    def _classify_commit(self, message: str) -> List[str]:
        """Classify commit by type based on message patterns"""
        types = []
        if self.feature_pattern.search(message):
            types.append('feature')
        if self.bugfix_pattern.search(message):
            types.append('bugfix')
        if self.refactor_pattern.search(message):
            types.append('refactor')
        
        # Default classification if none matched
        if not types:
            types.append('other')
            
        return types 