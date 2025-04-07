from typing import List, Dict, Any, Tuple, Optional
import re
from collections import defaultdict

class TechnicalChallengeDetector:
    """Identifies technical challenges and their solutions from commit history"""
    
    def __init__(self):
        """Initialize detector with pattern recognition for challenges"""
        # Challenge indicator patterns
        self.challenge_patterns = [
            re.compile(r'(?i)fix(?:ed)?\s+(?:a|the)?\s*(?:critical|major|security)?\s*(?:bug|issue|problem|error)'),
            re.compile(r'(?i)workaround\s+for'),
            re.compile(r'(?i)struggling\s+with'),
            re.compile(r'(?i)resolv(?:e|ed|ing)\s+(?:a|the)\s*(?:critical|major)?\s*(?:bug|issue|problem)'),
            re.compile(r'(?i)address(?:ed|ing)\s+(?:performance|memory|scaling|loading)\s+(?:issue|problem|bottleneck)'),
            re.compile(r'(?i)mitigat(?:e|ed|ing)'),
            re.compile(r'(?i)prevent(?:ed|ing)?(?:\s+future)?\s+(?:crash|failure|bug|issue)'),
            re.compile(r'(?i)finally\s+(?:fix|solv)(?:ed|ing)'),
            re.compile(r'(?i)(?:bug|issue|ticket|problem)\s*(?::|#|fix)')
        ]
        
        # Solution indicator patterns
        self.solution_patterns = [
            re.compile(r'(?i)implement(?:ed)?\s+(?:a|the|new)?\s*(?:better|improved|optimized)?\s*(?:solution|approach|method)'),
            re.compile(r'(?i)(?:performance|memory|speed)\s+(?:improvement|optimization|boost)'),
            re.compile(r'(?i)refactor(?:ed|ing)?(?:\s+to\s+(?:improve|fix|solve))?'),
            re.compile(r'(?i)rewrite\s+(?:of|to)'),
            re.compile(r'(?i)(?:better|cleaner|more efficient)\s+implementation')
        ]
        
    def identify_challenges(self, commits: List[Dict[str, Any]], clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identify technical challenges and their solutions
        
        Args:
            commits: List of commit dictionaries
            clusters: List of commit clusters
            
        Returns:
            List of technical challenges with related commits
        """
        # First pass: identify challenge indicators
        initial_challenges = self._identify_initial_challenges(commits)
        
        # Second pass: connect fixes with problems
        connected_challenges = self._connect_problems_with_solutions(initial_challenges, commits)
        
        # Third pass: enrich with cluster information
        enriched_challenges = self._enrich_with_clusters(connected_challenges, clusters)
        
        # Fourth pass: prioritize and filter challenges
        significant_challenges = self._prioritize_challenges(enriched_challenges)
        
        return significant_challenges
    
    def _identify_initial_challenges(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """First pass: identify commits indicating challenges"""
        challenges = []
        
        for commit in commits:
            message = commit['message']
            
            # Check for challenge patterns
            is_challenge = any(pattern.search(message) for pattern in self.challenge_patterns)
            is_solution = any(pattern.search(message) for pattern in self.solution_patterns)
            
            if is_challenge or is_solution:
                challenge_type = 'problem' if is_challenge else 'solution'
                
                challenge = {
                    'type': challenge_type,
                    'commit': commit,
                    'date': commit['date'],
                    'message': message.split('\n')[0],  # First line only
                    'related_commits': [commit],
                    'solution_commits': [] if is_challenge else [commit],
                    'problem_commits': [commit] if is_challenge else []
                }
                challenges.append(challenge)
                
        return challenges
    
    def _connect_problems_with_solutions(self, challenges: List[Dict[str, Any]], all_commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Connect problem commits with their solution commits"""
        # Group challenges by affected files
        file_to_challenges = defaultdict(list)
        
        # First, map files to challenges
        for challenge in challenges:
            commit = challenge['commit']
            for file_info in commit.get('modified_files', []):
                file_path = file_info['path']
                file_to_challenges[file_path].append(challenge)
        
        # Connect problems with solutions
        connected_challenges = []
        processed_ids = set()
        
        for challenge in challenges:
            if id(challenge) in processed_ids:
                continue
                
            if challenge['type'] == 'problem':
                # Look for solutions to this problem
                connected = self._find_solutions(challenge, challenges, file_to_challenges)
                if connected:
                    processed_ids.update(id(c) for c in connected['component_challenges'])
                    connected_challenges.append(connected)
            elif challenge['type'] == 'solution':
                # Look for the problem this solves
                connected = self._find_problems(challenge, challenges, file_to_challenges)
                if connected:
                    processed_ids.update(id(c) for c in connected['component_challenges'])
                    connected_challenges.append(connected)
        
        return connected_challenges
    
    def _find_solutions(self, problem: Dict[str, Any], all_challenges: List[Dict[str, Any]], file_map: Dict[str, List[Dict[str, Any]]]) -> Optional[Dict[str, Any]]:
        """Find solution commits for a problem commit"""
        problem_commit = problem['commit']
        problem_date = problem_commit['date']
        
        # Get files modified in the problem commit
        problem_files = [f['path'] for f in problem_commit.get('modified_files', [])]
        
        # Potential solutions: later commits that touch the same files
        potential_solutions = []
        
        for file_path in problem_files:
            for challenge in file_map.get(file_path, []):
                if challenge['type'] == 'solution' and challenge['date'] >= problem_date:
                    potential_solutions.append(challenge)
        
        if not potential_solutions:
            return None
        
        # Sort by date and take the closest ones
        potential_solutions.sort(key=lambda x: x['date'])
        solutions = potential_solutions[:3]  # Limit to 3 most relevant
        
        # Generate a title for the challenge based on the problem commit message
        title = self._generate_challenge_title(problem_commit['message'])
        
        # Generate description for the problem
        description = self._generate_problem_description(problem_commit)
        
        # Generate descriptions for solutions
        solution_descriptions = []
        for solution in solutions:
            solution_descriptions.append({
                'date': solution['date'],
                'description': self._generate_solution_description(solution['commit']),
                'commit': solution['commit']
            })
        
        # Combine into a single challenge
        combined = {
            'type': 'technical_challenge',
            'title': title,
            'problem': {
                'commit': problem_commit,
                'date': problem_date,
                'title': title,
                'description': description
            },
            'solutions': solution_descriptions,
            'all_commits': [problem_commit] + [s['commit'] for s in solutions],
            'component_challenges': [problem] + solutions,
            'start_date': problem_date,
            'end_date': max(s['date'] for s in solutions),
            'files_affected': problem_files,
            'difficulty': self._estimate_challenge_difficulty(problem_date, max(s['date'] for s in solutions), len(solutions))
        }
        
        return combined
    
    def _generate_challenge_title(self, message: str) -> str:
        """Generate a descriptive title for the challenge based on commit message"""
        # Extract the first line and clean it up
        first_line = message.split('\n')[0].strip()
        
        # Remove prefixes like "Fix:", "Bugfix:", etc.
        prefixes = ['fix:', 'fix', 'bugfix:', 'bugfix', 'issue:', 'problem:', 'bug:']
        for prefix in prefixes:
            if first_line.lower().startswith(prefix):
                first_line = first_line[len(prefix):].strip()
                
        # If message is too long, truncate it
        if len(first_line) > 60:
            first_line = first_line[:57] + '...'
            
        # If message is too short or generic, enhance it
        if len(first_line) < 10 or first_line.lower() in ['bug', 'issue', 'problem', 'fix']:
            return "Issue requiring technical solution"
            
        return first_line.capitalize()
    
    def _generate_problem_description(self, commit: Dict[str, Any]) -> str:
        """Generate a description for the problem based on commit data"""
        message = commit.get('message', '')
        
        # Extract a more detailed description if available
        parts = message.split('\n\n', 1)
        if len(parts) > 1 and len(parts[1]) > 10:
            # There's a detailed description after the first line
            return parts[1].strip()
            
        # If no detailed description, use the modified files and message
        modified_files = commit.get('modified_files', [])
        file_paths = [f['path'] for f in modified_files[:3]]
        
        if file_paths:
            file_desc = ", ".join(file_paths)
            if len(modified_files) > 3:
                file_desc += f" and {len(modified_files) - 3} other files"
            
            # Use string splitting without backslash in f-string
            first_line = message.split('\n')[0]
            return f"Problem affecting {file_desc}. {first_line}"
        
        # Fallback to just the message first line
        return message.split('\n')[0]
    
    def _generate_solution_description(self, commit: Dict[str, Any]) -> str:
        """Generate a description for the solution based on commit data"""
        message = commit.get('message', '')
        
        # Clean up the message
        description = message.split('\n')[0].strip()
        
        # Look for solution-oriented terms
        solution_terms = ['implement', 'solve', 'fix', 'address', 'resolve', 
                         'improve', 'optimize', 'refactor', 'update']
                         
        if not any(term in description.lower() for term in solution_terms):
            description = f"Fix implemented: {description}"
            
        return description
    
    def _estimate_challenge_difficulty(self, start_date, end_date, solution_count: int) -> str:
        """Estimate the difficulty of a challenge based on time to resolve and solution count"""
        # Calculate days to resolve
        days_to_resolve = (end_date - start_date).days
        
        if days_to_resolve > 14 or solution_count > 2:
            return "High"
        elif days_to_resolve > 3 or solution_count > 1:
            return "Medium"
        else:
            return "Low"
    
    def _find_problems(self, solution: Dict[str, Any], all_challenges: List[Dict[str, Any]], file_map: Dict[str, List[Dict[str, Any]]]) -> Optional[Dict[str, Any]]:
        """Find problem commits that a solution addresses"""
        solution_commit = solution['commit']
        solution_date = solution_commit['date']
        
        # Get files modified in the solution commit
        solution_files = [f['path'] for f in solution_commit.get('modified_files', [])]
        
        # Potential problems: earlier commits that touch the same files
        potential_problems = []
        
        for file_path in solution_files:
            for challenge in file_map.get(file_path, []):
                if challenge['type'] == 'problem' and challenge['date'] <= solution_date:
                    potential_problems.append(challenge)
        
        if not potential_problems:
            return None
        
        # Sort by date and take the closest ones
        potential_problems.sort(key=lambda x: x['date'], reverse=True)
        problems = potential_problems[:2]  # Limit to 2 most relevant
        
        # Generate title based on solution's commit message
        title = self._generate_challenge_title(solution_commit['message'])
        
        # Generate solution description
        solution_description = self._generate_solution_description(solution_commit)
        
        # Generate descriptions for problems
        problem_description = ""
        if problems:
            problem_description = self._generate_problem_description(problems[0]['commit'])
        
        # Combine into a single challenge
        combined = {
            'type': 'technical_challenge',
            'title': title,
            'problem': {
                'commit': problems[0]['commit'] if problems else None,
                'date': min(p['date'] for p in problems) if problems else solution_date,
                'title': title,
                'description': problem_description
            } if problems else None,
            'solutions': [{
                'date': solution_date,
                'description': solution_description,
                'commit': solution_commit
            }],
            'all_commits': [p['commit'] for p in problems] + [solution_commit],
            'component_challenges': problems + [solution],
            'start_date': min(p['date'] for p in problems) if problems else solution_date,
            'end_date': solution_date,
            'files_affected': solution_files,
            'difficulty': self._estimate_challenge_difficulty(
                min(p['date'] for p in problems) if problems else solution_date, 
                solution_date, 
                len(problems)
            )
        }
        
        return combined
    
    def _enrich_with_clusters(self, challenges: List[Dict[str, Any]], clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich challenges with cluster information"""
        # Create a map of commit hash to cluster
        commit_to_cluster = {}
        for cluster in clusters:
            for commit in cluster['commits']:
                commit_to_cluster[commit['hash']] = cluster
        
        # Enrich each challenge
        for challenge in challenges:
            # Find clusters for all commits in this challenge
            related_clusters = set()
            for commit in challenge['all_commits']:
                cluster = commit_to_cluster.get(commit['hash'])
                if cluster:
                    related_clusters.add(cluster['id'])
            
            # Add cluster information
            challenge['related_clusters'] = list(related_clusters)
            
            # Get theme from most relevant cluster
            if related_clusters:
                most_common_cluster_id = max(related_clusters, key=lambda cid: 
                                         sum(1 for c in challenge['all_commits'] 
                                             if commit_to_cluster.get(c['hash'], {}).get('id') == cid))
                                             
                most_common_cluster = next((c for c in clusters if c['id'] == most_common_cluster_id), None)
                if most_common_cluster:
                    challenge['theme'] = most_common_cluster['theme']
            
        return challenges
    
    def _prioritize_challenges(self, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize challenges based on significance"""
        if not challenges:
            return []
            
        # Calculate significance scores
        for challenge in challenges:
            # Factors for significance
            commits_count = len(challenge['all_commits'])
            files_count = len(challenge['files_affected'])
            solutions_count = len(challenge['solutions'])
            
            # Calculate a significance score
            significance = (commits_count * 2) + (files_count * 1.5) + (solutions_count * 3)
            
            # Check commit messages for indicators of importance
            important_terms = ['critical', 'major', 'significant', 'important', 'security', 'crash', 'fix']
            for commit in challenge['all_commits']:
                if any(term in commit['message'].lower() for term in important_terms):
                    significance += 5
            
            challenge['significance'] = significance
        
        # Sort by significance
        sorted_challenges = sorted(challenges, key=lambda x: x.get('significance', 0), reverse=True)
        
        # Take top challenges (maximum 5)
        return sorted_challenges[:5] 