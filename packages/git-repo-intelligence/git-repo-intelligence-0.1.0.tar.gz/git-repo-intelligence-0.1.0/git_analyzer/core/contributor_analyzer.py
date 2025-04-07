from typing import List, Dict, Any
from collections import defaultdict, Counter
import datetime
import math
import re

class ContributorAnalyzer:
    """Analyzes contributor activities and expertise"""
    
    def __init__(self):
        """Initialize the contributor analyzer"""
        pass
        
    def analyze_contributors(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze contributor activities and patterns
        
        Args:
            commits: List of commit dictionaries
            
        Returns:
            Dict containing contributor profiles and team metrics
        """
        # Extract contributor profiles
        contributor_profiles = self._extract_contributor_profiles(commits)
        
        # Analyze file ownership
        file_ownership = self._analyze_file_ownership(commits)
        
        # Analyze collaboration patterns
        collaboration_patterns = self._analyze_collaboration_patterns(commits, contributor_profiles)
        
        # Calculate team metrics
        team_metrics = self._calculate_team_metrics(contributor_profiles, collaboration_patterns)
        
        return {
            'contributor_profiles': contributor_profiles,
            'file_ownership': file_ownership,
            'collaboration_patterns': collaboration_patterns,
            'team_metrics': team_metrics
        }
    
    def _extract_contributor_profiles(self, commits: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Extract detailed profiles for each contributor"""
        profiles = {}
        
        # Group commits by author
        author_commits = defaultdict(list)
        for commit in commits:
            author_name = commit.get('author_name', 'Unknown')
            author_commits[author_name].append(commit)
        
        # Process each author's commits
        for author_name, author_commit_list in author_commits.items():
            # Count commit types
            commit_types = Counter()
            for commit in author_commit_list:
                # commit_type can be a list or a string
                types = commit.get('commit_type', ['unknown'])
                if isinstance(types, list):
                    for ctype in types:
                        commit_types[ctype] += 1
                else:
                    commit_types[types] += 1
            
            # Calculate active timeline
            commit_dates = [commit['date'] for commit in author_commit_list]
            first_commit = min(commit_dates)
            last_commit = max(commit_dates)
            active_days = (last_commit - first_commit).days + 1
            
            # Identify files changed
            modified_files = set()
            language_usage = Counter()
            
            for commit in author_commit_list:
                for file_info in commit.get('modified_files', []):
                    file_path = file_info['path']
                    modified_files.add(file_path)
                    
                    # Determine file language from extension
                    extension = file_path.split('.')[-1].lower() if '.' in file_path else 'unknown'
                    language_usage[extension] += 1
            
            # Calculate areas of expertise
            expertise_areas = self._identify_expertise_areas(author_commit_list, modified_files)
            
            # Calculate contribution metrics
            total_additions = sum(commit.get('stats', {}).get('lines_added', 0) for commit in author_commit_list)
            total_deletions = sum(commit.get('stats', {}).get('lines_removed', 0) for commit in author_commit_list)
            
            # Create profile
            profile = {
                'name': author_name,
                'commit_count': len(author_commit_list),
                'first_commit': first_commit,
                'last_commit': last_commit,
                'active_days': active_days,
                'commit_types': dict(commit_types),
                'files_modified': len(modified_files),
                'languages': dict(language_usage.most_common(5)),  # Top 5 languages
                'expertise_areas': expertise_areas,
                'total_additions': total_additions,
                'total_deletions': total_deletions,
                'activity_by_month': self._calculate_monthly_activity(author_commit_list)
            }
            
            profiles[author_name] = profile
            
        return profiles
    
    def _calculate_monthly_activity(self, commits: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate monthly activity for a contributor"""
        monthly_activity = defaultdict(int)
        
        for commit in commits:
            date = commit['date']
            month_key = f"{date.year}-{date.month:02d}"
            monthly_activity[month_key] += 1
            
        # Sort by month
        return {month: monthly_activity[month] for month in sorted(monthly_activity.keys())}
    
    def _identify_expertise_areas(self, commits: List[Dict[str, Any]], 
                                 modified_files: set) -> List[Dict[str, Any]]:
        """Identify areas of expertise for a contributor"""
        # Count file modifications by directory
        dir_counts = defaultdict(int)
        
        for file_path in modified_files:
            # Extract directory path
            dir_path = '/'.join(file_path.split('/')[:-1])
            if not dir_path:
                dir_path = 'root'
                
            dir_counts[dir_path] += 1
            
        # Identify expertise by directory concentration
        expertise_areas = []
        
        # Convert to list of (dir, count) tuples and sort
        sorted_dirs = sorted(dir_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Take top 3 directories as expertise areas
        for dir_path, count in sorted_dirs[:3]:
            expertise_level = 'high' if count >= 10 else 'medium' if count >= 5 else 'low'
            
            expertise_areas.append({
                'area': dir_path,
                'level': expertise_level,
                'file_count': count,
                'percentage': round((count / len(modified_files)) * 100, 1)
            })
            
        return expertise_areas
    
    def _analyze_file_ownership(self, commits: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Analyze which contributors 'own' which files"""
        # Track file modifications
        file_authors = defaultdict(Counter)
        
        for commit in commits:
            author = commit.get('author_name', 'Unknown')
            
            for file_info in commit.get('modified_files', []):
                file_path = file_info['path']
                file_authors[file_path][author] += 1
                
        # Determine ownership
        ownership = {}
        
        for file_path, authors in file_authors.items():
            total_changes = sum(authors.values())
            
            # Sort authors by number of changes
            sorted_authors = authors.most_common()
            primary_author = sorted_authors[0][0]
            primary_changes = sorted_authors[0][1]
            
            # Calculate ownership percentage
            ownership_pct = (primary_changes / total_changes) * 100
            
            # Define ownership level
            if ownership_pct >= 75:
                ownership_level = 'strong'
            elif ownership_pct >= 50:
                ownership_level = 'moderate'
            else:
                ownership_level = 'shared'
                
            # Create ownership record
            ownership[file_path] = {
                'primary_author': primary_author,
                'ownership_percentage': round(ownership_pct, 1),
                'level': ownership_level,
                'total_changes': total_changes,
                'contributors': len(authors),
                'contributor_breakdown': [
                    {'name': author, 'changes': changes, 'percentage': round((changes / total_changes) * 100, 1)}
                    for author, changes in sorted_authors[:3]  # Top 3 contributors
                ]
            }
            
        return ownership
    
    def _analyze_collaboration_patterns(self, commits: List[Dict[str, Any]], 
                                       contributor_profiles: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how contributors collaborate"""
        # Track which contributors modify the same files
        collaboration_matrix = defaultdict(Counter)
        
        # Map files to their modifiers
        file_modifiers = defaultdict(set)
        
        for commit in commits:
            author = commit.get('author_name', 'Unknown')
            
            for file_info in commit.get('modified_files', []):
                file_path = file_info['path']
                file_modifiers[file_path].add(author)
                
        # Build collaboration matrix
        for file_path, authors in file_modifiers.items():
            if len(authors) <= 1:
                continue
                
            # For each pair of authors, increment their collaboration count
            author_list = list(authors)
            for i in range(len(author_list)):
                for j in range(i + 1, len(author_list)):
                    author_a = author_list[i]
                    author_b = author_list[j]
                    
                    collaboration_matrix[author_a][author_b] += 1
                    collaboration_matrix[author_b][author_a] += 1
        
        # Extract collaboration pairs
        collaboration_pairs = []
        
        for author_a, collaborators in collaboration_matrix.items():
            for author_b, count in collaborators.most_common():
                # Skip if we've already processed this pair in reverse
                if any(p for p in collaboration_pairs if p['authors'] == [author_b, author_a]):
                    continue
                    
                collaboration_pairs.append({
                    'authors': [author_a, author_b],
                    'file_count': count,
                    'strength': 'high' if count >= 10 else 'medium' if count >= 5 else 'low'
                })
                
        # Calculate primary collaboration groups
        collaboration_groups = self._identify_collaboration_groups(collaboration_matrix)
        
        return {
            'pairs': sorted(collaboration_pairs, key=lambda x: x['file_count'], reverse=True),
            'groups': collaboration_groups
        }
    
    def _identify_collaboration_groups(self, collaboration_matrix: Dict[str, Counter]) -> List[Dict[str, Any]]:
        """Identify primary collaboration groups"""
        # Simple approach: groups are based on collaboration strength
        groups = []
        processed_authors = set()
        
        for author, collaborators in collaboration_matrix.items():
            if author in processed_authors:
                continue
                
            # Get strong collaborators
            strong_collaborators = [a for a, count in collaborators.items() if count >= 5]
            
            if not strong_collaborators:
                continue
                
            # Form a group
            group = {
                'members': [author] + strong_collaborators,
                'size': len(strong_collaborators) + 1,
                'total_collaborations': sum(collaborators[a] for a in strong_collaborators)
            }
            
            groups.append(group)
            processed_authors.add(author)
            processed_authors.update(strong_collaborators)
            
        return groups
    
    def _calculate_team_metrics(self, contributor_profiles: Dict[str, Dict[str, Any]], 
                               collaboration_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall team metrics"""
        # Basic counts
        total_contributors = len(contributor_profiles)
        
        # Activity distribution
        commit_counts = [profile['commit_count'] for profile in contributor_profiles.values()]
        
        # Calculate distribution statistics
        if commit_counts:
            avg_commits = sum(commit_counts) / len(commit_counts)
            median_commits = sorted(commit_counts)[len(commit_counts) // 2]
            max_commits = max(commit_counts)
            min_commits = min(commit_counts)
        else:
            avg_commits = median_commits = max_commits = min_commits = 0
        
        # Calculate activity balance (Gini coefficient-like measure)
        activity_balance = self._calculate_activity_balance(commit_counts)
        
        # Calculate collaboration density
        total_possible_pairs = (total_contributors * (total_contributors - 1)) // 2
        actual_pairs = len(collaboration_patterns.get('pairs', []))
        collaboration_density = actual_pairs / total_possible_pairs if total_possible_pairs > 0 else 0
        
        return {
            'total_contributors': total_contributors,
            'avg_commits_per_contributor': round(avg_commits, 1),
            'median_commits': median_commits,
            'activity_distribution': {
                'min': min_commits,
                'max': max_commits,
                'balance': round(activity_balance, 2)  # 0 = perfectly balanced, 1 = imbalanced
            },
            'collaboration_density': round(collaboration_density, 2),
            'collaboration_groups': len(collaboration_patterns.get('groups', []))
        }
    
    def _calculate_activity_balance(self, commit_counts: List[int]) -> float:
        """
        Calculate activity balance using Gini coefficient approach
        0 = perfectly balanced, 1 = completely imbalanced
        """
        if not commit_counts:
            return 0
            
        n = len(commit_counts)
        if n <= 1:
            return 0
            
        # Sort commit counts
        sorted_counts = sorted(commit_counts)
        
        # Calculate Gini coefficient
        numerator = sum((i + 1) * count for i, count in enumerate(sorted_counts))
        denominator = sum(sorted_counts) * n
        
        if denominator == 0:
            return 0
            
        gini = (2 * numerator / denominator) - (n + 1) / n
        
        return gini 