from typing import List, Dict, Any, Optional
import datetime
import math
import statistics
from collections import defaultdict

class ImpactAnalyzer:
    """Analyzes the impact of changes and improvements in the repository"""
    
    def __init__(self):
        """Initialize impact analyzer"""
        pass
        
    def analyze_impact(self, 
                      commits: List[Dict[str, Any]], 
                      challenges: List[Dict[str, Any]],
                      milestones: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the impact of technical challenges and their solutions
        
        Args:
            commits: Full list of repository commits
            challenges: Technical challenges identified in the repository
            milestones: Project milestones
            
        Returns:
            Dict containing impact metrics and analysis
        """
        # Calculate baseline metrics
        baseline_metrics = self._calculate_baseline_metrics(commits)
        
        # Analyze challenge-specific impact
        challenge_impacts = self._analyze_challenge_impact(challenges, commits)
        
        # Estimate code quality metrics
        quality_metrics = self._estimate_quality_metrics(commits, challenges, milestones)
        
        return {
            'baseline_metrics': baseline_metrics,
            'challenge_impacts': challenge_impacts,
            'quality_metrics': quality_metrics
        }
    
    def _calculate_baseline_metrics(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate baseline repository metrics"""
        # Group commits by month
        monthly_commits = defaultdict(list)
        
        for commit in commits:
            date = commit['date']
            month_key = f"{date.year}-{date.month:02d}"
            monthly_commits[month_key].append(commit)
        
        # Calculate metrics
        metrics = {
            'total_commits': len(commits),
            'monthly_activity': {},
            'file_change_frequency': self._calculate_file_change_frequency(commits),
            'avg_changes_per_commit': self._calculate_avg_changes(commits),
            'development_velocity': self._calculate_development_velocity(monthly_commits)
        }
        
        # Calculate monthly activity
        for month, month_commits in monthly_commits.items():
            metrics['monthly_activity'][month] = {
                'commit_count': len(month_commits),
                'lines_added': sum(c.get('stats', {}).get('lines_added', 0) for c in month_commits),
                'lines_deleted': sum(c.get('stats', {}).get('lines_removed', 0) for c in month_commits),
                'files_changed': len(set(f['path'] for c in month_commits 
                                        for f in c.get('modified_files', [])))
            }
        
        return metrics
    
    def _calculate_file_change_frequency(self, commits: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate how frequently files are changed"""
        file_changes = defaultdict(int)
        
        for commit in commits:
            for file_info in commit.get('modified_files', []):
                file_path = file_info['path']
                file_changes[file_path] += 1
        
        # Return top 10 most frequently changed files
        most_changed_files = sorted(file_changes.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return dict(most_changed_files)
    
    def _calculate_avg_changes(self, commits: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate average changes per commit"""
        if not commits:
            return {'avg_additions': 0, 'avg_deletions': 0, 'avg_files_changed': 0}
            
        total_additions = sum(c.get('stats', {}).get('additions', 0) for c in commits)
        total_deletions = sum(c.get('stats', {}).get('deletions', 0) for c in commits)
        total_files_changed = sum(len(c.get('modified_files', [])) for c in commits)
        
        return {
            'avg_additions': round(total_additions / len(commits), 2),
            'avg_deletions': round(total_deletions / len(commits), 2),
            'avg_files_changed': round(total_files_changed / len(commits), 2)
        }
    
    def _calculate_development_velocity(self, monthly_commits: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Calculate development velocity metrics"""
        if not monthly_commits:
            return {'trend': 'steady', 'change_rate': 0}
            
        # Get monthly commit counts
        monthly_counts = {month: len(commits) for month, commits in monthly_commits.items()}
        
        # Sort by month
        sorted_months = sorted(monthly_counts.keys())
        counts = [monthly_counts[month] for month in sorted_months]
        
        # Calculate trend
        if len(counts) < 2:
            return {'trend': 'insufficient_data', 'change_rate': 0}
            
        # Simple linear regression to determine trend
        n = len(counts)
        x = list(range(n))
        
        # Calculate slope
        x_mean = sum(x) / n
        y_mean = sum(counts) / n
        
        numerator = sum((x[i] - x_mean) * (counts[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return {'trend': 'steady', 'change_rate': 0}
            
        slope = numerator / denominator
        
        # Determine trend
        if slope > 0.5:
            trend = 'accelerating'
        elif slope > 0.1:
            trend = 'increasing'
        elif slope < -0.5:
            trend = 'decelerating'
        elif slope < -0.1:
            trend = 'decreasing'
        else:
            trend = 'steady'
            
        # Calculate change rate
        change_rate = slope / (y_mean if y_mean > 0 else 1)
        
        return {
            'trend': trend,
            'change_rate': round(change_rate * 100, 2),  # as percentage
            'monthly_counts': {month: monthly_counts[month] for month in sorted_months}
        }
    
    def _analyze_challenge_impact(self, challenges: List[Dict[str, Any]], all_commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze the impact of resolving technical challenges"""
        impact_analyses = []
        
        for challenge in challenges:
            problem = challenge.get('problem')
            solutions = challenge.get('solutions', [])
            
            if not problem or not solutions:
                continue
                
            # Get problem date and solution date
            problem_date = problem['date']
            solution_date = max(solution['date'] for solution in solutions)
            
            # Get affected files
            affected_files = challenge.get('files_affected', [])
            
            # Look at commits before and after the challenge resolution
            before_period = self._get_period_commits(all_commits, problem_date, solution_date)
            after_period = self._get_period_commits(all_commits, solution_date,
                                                   solution_date + (solution_date - problem_date))
            
            # Check if there are enough commits to analyze
            if not before_period or not after_period:
                continue
                
            # Analyze code churn for affected files
            before_churn = self._analyze_file_churn(before_period, affected_files)
            after_churn = self._analyze_file_churn(after_period, affected_files)
            
            # Calculate change metrics
            churn_diff = self._calculate_churn_difference(before_churn, after_churn)
            
            # Create impact analysis
            impact = {
                'challenge_id': id(challenge),
                'problem_date': problem_date,
                'solution_date': solution_date,
                'affected_files': affected_files,
                'before_metrics': before_churn,
                'after_metrics': after_churn,
                'changes': churn_diff,
                'impact_score': self._calculate_impact_score(churn_diff)
            }
            
            impact_analyses.append(impact)
            
        return impact_analyses
    
    def _get_period_commits(self, commits: List[Dict[str, Any]], start_date: datetime.datetime, 
                           end_date: datetime.datetime) -> List[Dict[str, Any]]:
        """Get commits within a specified time period"""
        return [commit for commit in commits if start_date <= commit['date'] <= end_date]
    
    def _analyze_file_churn(self, commits: List[Dict[str, Any]], files: List[str]) -> Dict[str, Any]:
        """Analyze code churn for specific files"""
        total_additions = 0
        total_deletions = 0
        commit_count = 0
        
        for commit in commits:
            # Get file details from stats
            file_details = commit.get('stats', {}).get('file_details', {})
            
            for file_info in commit.get('modified_files', []):
                file_path = file_info['path']
                if file_path in files:
                    # Get changes from file_details if available
                    if file_path in file_details:
                        total_additions += file_details[file_path].get('insertions', 0)
                        total_deletions += file_details[file_path].get('deletions', 0)
                    commit_count += 1
                    
        return {
            'total_commits': commit_count,
            'total_additions': total_additions,
            'total_deletions': total_deletions,
            'total_churn': total_additions + total_deletions
        }
    
    def _calculate_churn_difference(self, before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate difference in code churn before and after"""
        # Avoid division by zero
        before_commits = before['total_commits'] or 1
        after_commits = after['total_commits'] or 1
        
        # Calculate per-commit metrics
        before_churn_per_commit = before['total_churn'] / before_commits
        after_churn_per_commit = after['total_churn'] / after_commits
        
        # Calculate percentage changes
        if before_churn_per_commit > 0:
            churn_change_pct = ((after_churn_per_commit - before_churn_per_commit) / before_churn_per_commit) * 100
        else:
            churn_change_pct = 0
            
        return {
            'churn_per_commit_before': round(before_churn_per_commit, 2),
            'churn_per_commit_after': round(after_churn_per_commit, 2),
            'churn_change_pct': round(churn_change_pct, 2)
        }
    
    def _calculate_impact_score(self, churn_diff: Dict[str, Any]) -> float:
        """Calculate impact score based on churn difference"""
        # A negative churn change is good (less churn after)
        churn_change_pct = churn_diff.get('churn_change_pct', 0)
        
        if churn_change_pct <= -50:  # Significant improvement (50%+ reduction)
            return 5.0
        elif churn_change_pct <= -20:  # Good improvement
            return 4.0
        elif churn_change_pct <= -5:  # Modest improvement
            return 3.0
        elif churn_change_pct <= 5:  # Minimal change
            return 2.0
        else:  # Worsened or no significant improvement
            return 1.0
    
    def _estimate_quality_metrics(self, commits: List[Dict[str, Any]], 
                                  challenges: List[Dict[str, Any]],
                                  milestones: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate code quality metrics based on commit history"""
        # Calculate bug frequency
        bug_commits = [c for c in commits if 'bugfix' in c.get('commit_type', [])]
        bug_frequency = len(bug_commits) / len(commits) if commits else 0
        
        # Analyze resolved challenges impact on code quality
        challenge_impacts = [c.get('impact_score', 0) for c in challenges]
        avg_challenge_impact = statistics.mean(challenge_impacts) if challenge_impacts else 0
        
        # Development stability (lower churn is better)
        avg_churn = sum(c.get('stats', {}).get('lines_added', 0) + c.get('stats', {}).get('lines_removed', 0) 
                       for c in commits) / len(commits) if commits else 0
                       
        # Check if recent commits have less churn than older ones
        if len(commits) >= 10:
            recent_commits = commits[-10:]
            older_commits = commits[:-10]
            
            recent_churn = sum(c.get('stats', {}).get('lines_added', 0) + c.get('stats', {}).get('lines_removed', 0) 
                            for c in recent_commits) / len(recent_commits)
            older_churn = sum(c.get('stats', {}).get('lines_added', 0) + c.get('stats', {}).get('lines_removed', 0) 
                           for c in older_commits) / len(older_commits) if older_commits else 0
            
            churn_trend = (older_churn - recent_churn) / older_churn if older_churn > 0 else 0
        else:
            churn_trend = 0
            
        # Calculate refactoring frequency
        refactor_commits = [c for c in commits if ('refactor' in c.get('commit_type', []) or 
                                                'refactor' in c.get('message', '').lower())]
        refactor_frequency = len(refactor_commits) / len(commits) if commits else 0
        
        # Overall quality score (1-5)
        quality_score = 3.0  # Start at neutral
        
        # Adjust based on metrics
        if bug_frequency < 0.1:  # Less than 10% bug fixes
            quality_score += 0.5
        elif bug_frequency > 0.3:  # More than 30% bug fixes
            quality_score -= 0.5
            
        if avg_challenge_impact >= 4.0:  # High impact from challenge resolutions
            quality_score += 0.5
        elif avg_challenge_impact <= 2.0:  # Low impact from challenge resolutions
            quality_score -= 0.5
            
        if churn_trend > 0.2:  # Significant reduction in churn
            quality_score += 0.5
        elif churn_trend < -0.2:  # Significant increase in churn
            quality_score -= 0.5
            
        if refactor_frequency > 0.15:  # Healthy amount of refactoring
            quality_score += 0.5
            
        # Clamp to 1-5 range
        quality_score = max(1.0, min(5.0, quality_score))
        
        return {
            'bug_frequency': round(bug_frequency * 100, 2),  # as percentage
            'refactor_frequency': round(refactor_frequency * 100, 2),  # as percentage
            'avg_challenge_impact': round(avg_challenge_impact, 2),
            'churn_trend': round(churn_trend * 100, 2),  # as percentage
            'quality_score': round(quality_score, 1)
        } 