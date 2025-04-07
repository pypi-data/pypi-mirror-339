from collections import defaultdict
from datetime import datetime, timedelta
import re
from typing import List, Dict, Any, Optional

class MilestoneDetector:
    """Identifies significant milestones in repository history"""
    
    def __init__(self):
        """Initialize detector with pattern recognition rules"""
        # Version tag patterns (semantic versioning)
        self.version_pattern = re.compile(r'v?\d+\.\d+\.\d+')
        
        # Major feature patterns
        self.feature_patterns = [
            re.compile(r'(?i)add(?:ed)?\s+(?:new\s+)?feature'),
            re.compile(r'(?i)implement(?:ed)?\s+'),
            re.compile(r'(?i)introduce(?:d)?\s+'),
            re.compile(r'(?i)launch(?:ed)?\s+')
        ]
        
        # Release patterns
        self.release_patterns = [
            re.compile(r'(?i)release(?:d)?'),
            re.compile(r'(?i)version'),
            re.compile(r'(?i)milestone'),
            re.compile(r'(?i)tag(?:ged)?')
        ]
        
    def detect_milestones(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract milestone events from commit history
        
        Args:
            commits: List of commit dictionaries with metadata
            
        Returns:
            List of milestone events
        """
        # Sort commits chronologically (oldest first)
        sorted_commits = sorted(commits, key=lambda x: x['date'])
        
        milestones = []
        
        # Process version releases
        version_milestones = self._extract_version_releases(sorted_commits)
        milestones.extend(version_milestones)
        
        # Process major features
        feature_milestones = self._extract_major_features(sorted_commits)
        milestones.extend(feature_milestones)
        
        # Process significant code changes
        significant_changes = self._extract_significant_changes(sorted_commits)
        milestones.extend(significant_changes)
        
        # Group by month for timeline presentation
        monthly_milestones = self._group_by_month(milestones)
        
        return monthly_milestones
    
    def _extract_version_releases(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract version release milestones"""
        version_milestones = []
        
        for commit in commits:
            # Check for version tag in commit message
            version_match = self.version_pattern.search(commit['message'])
            
            # Check for release keywords
            is_release = any(pattern.search(commit['message']) for pattern in self.release_patterns)
            
            if version_match or is_release:
                version = version_match.group(0) if version_match else None
                
                # Generate a meaningful title
                title = self._generate_release_title(commit['message'], version)
                
                # Generate a summary
                summary = self._generate_release_summary(commit, version)
                
                milestone = {
                    'date': commit['date'],
                    'type': 'release',
                    'version': version,
                    'title': title,
                    'summary': summary,
                    'description': commit['message'].split('\n')[0],
                    'commit_hash': commit['short_hash'],
                    'significance': 'high' if version else 'medium',
                    'key_commits': [commit]
                }
                version_milestones.append(milestone)
                
        return version_milestones
    
    def _generate_release_title(self, message: str, version: Optional[str]) -> str:
        """Generate a meaningful title for the release milestone"""
        # Extract the first line of the commit message
        first_line = message.split('\n')[0].strip()
        
        # If there's a version, use it in the title
        if version:
            # Check if the version is already in the first line
            if version in first_line:
                return first_line
            else:
                return f"Release {version}: {first_line}"
                
        # If no version but has "release" in the message
        if "release" in first_line.lower():
            return first_line
            
        # Default title
        return f"Release: {first_line}"
    
    def _generate_release_summary(self, commit: Dict[str, Any], version: Optional[str]) -> str:
        """Generate a comprehensive summary for the release milestone"""
        message = commit['message']
        
        # Extract a more detailed description if available
        parts = message.split('\n\n', 1)
        if len(parts) > 1 and len(parts[1]) > 10:
            # There's a detailed description after the first line
            return parts[1].strip()
            
        # If no detailed description, generate one based on commit stats
        stats = commit['stats']
        summary = f"This release includes {stats['lines_added']} new lines of code"
        if stats['lines_removed'] > 0:
            summary += f" and removes {stats['lines_removed']} lines"
        
        # Add information about modified files
        modified_files = commit.get('modified_files', [])
        if modified_files:
            file_types = self._categorize_files([f['path'] for f in modified_files])
            summary += f". Changes include {', '.join(f'{count} {category} files' for category, count in file_types.items())}"
            
        return summary
        
    def _categorize_files(self, file_paths: List[str]) -> Dict[str, int]:
        """Categorize files by type for summary generation"""
        categories = defaultdict(int)
        
        for path in file_paths:
            if path.endswith(('.py', '.pyc')):
                categories['Python'] += 1
            elif path.endswith(('.js', '.jsx', '.ts', '.tsx')):
                categories['JavaScript/TypeScript'] += 1
            elif path.endswith(('.java', '.class')):
                categories['Java'] += 1
            elif path.endswith(('.c', '.cpp', '.h', '.hpp')):
                categories['C/C++'] += 1
            elif path.endswith(('.html', '.htm')):
                categories['HTML'] += 1
            elif path.endswith(('.css', '.scss', '.sass')):
                categories['CSS'] += 1
            elif path.endswith(('.md', '.txt', '.rst')):
                categories['documentation'] += 1
            elif path.endswith(('.json', '.yml', '.yaml', '.toml', '.ini')):
                categories['configuration'] += 1
            elif path.endswith(('.sql')):
                categories['database'] += 1
            elif path.endswith(('.xml')):
                categories['XML'] += 1
            elif path.endswith(('.sh', '.bash')):
                categories['shell script'] += 1
            elif 'test' in path.lower() or 'spec' in path.lower():
                categories['test'] += 1
            else:
                categories['other'] += 1
                
        return categories
    
    def _extract_major_features(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract major feature implementation milestones"""
        feature_milestones = []
        
        for commit in commits:
            # Skip merge commits
            if commit.get('is_merge', False):
                continue
                
            # Check for feature implementation patterns
            if any(pattern.search(commit['message']) for pattern in self.feature_patterns):
                if commit['stats']['lines_added'] > 100:  # Significant addition
                    # Generate title and summary
                    title = self._generate_feature_title(commit['message'])
                    summary = self._generate_feature_summary(commit)
                    
                    milestone = {
                        'date': commit['date'],
                        'type': 'feature',
                        'title': title,
                        'summary': summary,
                        'description': commit['message'].split('\n')[0],
                        'commit_hash': commit['short_hash'],
                        'significance': 'medium',
                        'lines_added': commit['stats']['lines_added'],
                        'key_commits': [commit]
                    }
                    feature_milestones.append(milestone)
                    
        return feature_milestones
    
    def _generate_feature_title(self, message: str) -> str:
        """Generate a meaningful title for the feature milestone"""
        # Extract the first line
        first_line = message.split('\n')[0].strip()
        
        # Remove common prefixes
        prefixes = ['add feature', 'add', 'feature', 'implement', 'add new feature', 'added', 'new feature']
        for prefix in prefixes:
            if first_line.lower().startswith(prefix):
                first_line = first_line[len(prefix):].strip()
                # If there's a colon after the prefix, remove it too
                if first_line.startswith(':'):
                    first_line = first_line[1:].strip()
                break
                
        # If we're left with nothing, use the original
        if not first_line:
            first_line = message.split('\n')[0].strip()
            
        # Add a better prefix
        return f"New Feature: {first_line}"
    
    def _generate_feature_summary(self, commit: Dict[str, Any]) -> str:
        """Generate a comprehensive summary for the feature milestone"""
        message = commit['message']
        
        # Extract a more detailed description if available
        parts = message.split('\n\n', 1)
        if len(parts) > 1 and len(parts[1]) > 10:
            # There's a detailed description after the first line
            return parts[1].strip()
            
        # If no detailed description, generate one based on commit
        modified_files = commit.get('modified_files', [])
        summary = f"This feature adds {commit['stats']['lines_added']} lines of code"
        
        # Identify components affected
        if modified_files:
            components = self._identify_components(modified_files)
            if components:
                summary += f" across {len(components)} components: {', '.join(components[:3])}"
                if len(components) > 3:
                    summary += f" and {len(components) - 3} others"
                    
        return summary
    
    def _identify_components(self, modified_files: List[Dict[str, Any]]) -> List[str]:
        """Identify components affected by changes based on file paths"""
        components = set()
        
        for file_info in modified_files:
            path = file_info['path']
            
            # Extract component from path
            parts = path.split('/')
            if len(parts) > 1:
                # Use first or second directory as component
                component = parts[0]
                if component in ['.', 'src', 'app', 'lib', 'modules']:
                    component = parts[1] if len(parts) > 1 else component
                components.add(component)
                
        return list(components)
    
    def _extract_significant_changes(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract commits representing significant code changes"""
        significant_milestones = []
        
        for commit in commits:
            # Skip merge commits
            if commit.get('is_merge', False):
                continue
                
            # Large code changes
            if (commit['stats']['lines_added'] + commit['stats']['lines_removed'] > 500 and 
                    'refactor' not in commit.get('commit_type', [])):
                # Generate title and summary
                title = self._generate_significant_change_title(commit['message'])
                summary = self._generate_significant_change_summary(commit)
                
                milestone = {
                    'date': commit['date'],
                    'type': 'significant_change',
                    'title': title,
                    'summary': summary,
                    'description': commit['message'].split('\n')[0],
                    'commit_hash': commit['short_hash'],
                    'significance': 'medium',
                    'lines_changed': commit['stats']['lines_added'] + commit['stats']['lines_removed'],
                    'key_commits': [commit]
                }
                significant_milestones.append(milestone)
                
        return significant_milestones
    
    def _generate_significant_change_title(self, message: str) -> str:
        """Generate a meaningful title for the significant change milestone"""
        # Extract the first line
        first_line = message.split('\n')[0].strip()
        
        # Determine the type of change based on keywords
        if any(term in first_line.lower() for term in ['architecture', 'restructure', 'structure']):
            return f"Architecture Change: {first_line}"
        elif any(term in first_line.lower() for term in ['overhaul', 'rewrite', 'reimplement']):
            return f"Major Overhaul: {first_line}"
        elif any(term in first_line.lower() for term in ['update', 'upgrade']):
            return f"Significant Update: {first_line}"
        else:
            return f"Major Change: {first_line}"
    
    def _generate_significant_change_summary(self, commit: Dict[str, Any]) -> str:
        """Generate a comprehensive summary for the significant change milestone"""
        message = commit['message']
        
        # Extract a more detailed description if available
        parts = message.split('\n\n', 1)
        if len(parts) > 1 and len(parts[1]) > 10:
            # There's a detailed description after the first line
            return parts[1].strip()
            
        # If no detailed description, generate one based on commit
        stats = commit['stats']
        summary = f"This significant change involves {stats['lines_added']} additions and {stats['lines_removed']} deletions"
        
        # Add information about modified files
        modified_files = commit.get('modified_files', [])
        if modified_files:
            file_count = len(modified_files)
            summary += f" across {file_count} files"
            
            # Check if it's a specific type of change
            if any('test' in f['path'].lower() for f in modified_files):
                summary += ", including test infrastructure"
            elif any('config' in f['path'].lower() or f['path'].endswith(('.json', '.yml', '.yaml', '.toml')) for f in modified_files):
                summary += ", including configuration changes"
            elif any('migrations' in f['path'].lower() or 'database' in f['path'].lower() for f in modified_files):
                summary += ", including database changes"
            
        return summary
    
    def _group_by_month(self, milestones: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Group milestones by month for timeline presentation"""
        if not milestones:
            return []
            
        # Sort by date
        sorted_milestones = sorted(milestones, key=lambda x: x['date'])
        
        # Group by month
        monthly_groups = defaultdict(list)
        for milestone in sorted_milestones:
            month_key = milestone['date'].strftime('%Y-%m')
            monthly_groups[month_key].append(milestone)
            
        # Format for timeline
        timeline = []
        for month, events in monthly_groups.items():
            date_obj = datetime.strptime(month, '%Y-%m')
            month_name = date_obj.strftime('%b %Y')
            
            # Select most significant event as representative
            significant_events = [e for e in events if e.get('significance') == 'high']
            if significant_events:
                representative = significant_events[0]
            else:
                representative = events[0]
                
            # Ensure the representative has a title
            if 'title' not in representative:
                representative['title'] = representative['description']
                
            timeline_item = {
                'month': month_name,
                'date': date_obj,
                'title': representative['title'],
                'summary': representative.get('summary', representative['description']),
                'type': representative['type'],
                'all_events': events,
                'event_count': len(events)
            }
            timeline.append(timeline_item)
            
        return timeline 