from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import numpy as np
from typing import List, Dict, Any, Tuple
from collections import Counter
import re

class CommitClusterer:
    """Clusters commits based on semantic similarity"""
    
    def __init__(self, min_cluster_size: int = 3, max_distance: float = 0.7):
        """
        Initialize the clusterer with parameters
        
        Args:
            min_cluster_size: Minimum number of commits to form a cluster
            max_distance: Maximum distance for commits to be considered related
        """
        self.min_cluster_size = min_cluster_size
        self.max_distance = max_distance
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        
        # Preprocessing patterns
        self.cleanup_pattern = re.compile(r'[^a-zA-Z0-9\s]')
        
    def preprocess_commit_messages(self, commits: List[Dict[str, Any]]) -> List[str]:
        """Clean and normalize commit messages for analysis"""
        processed_messages = []
        
        for commit in commits:
            message = commit['message']
            
            # Extract first line (summary)
            first_line = message.split('\n')[0]
            
            # Remove special characters, except spaces
            cleaned = self.cleanup_pattern.sub(' ', first_line)
            
            # Convert to lowercase and normalize whitespace
            normalized = ' '.join(cleaned.lower().split())
            
            processed_messages.append(normalized)
            
        return processed_messages
    
    def cluster_commits(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cluster commits based on message similarity
        
        Args:
            commits: List of commit dictionaries
            
        Returns:
            List of clusters, each containing related commits
        """
        if len(commits) < self.min_cluster_size:
            # Not enough commits to cluster
            return [{'id': 0, 'commits': commits, 'theme': 'all_commits', 'size': len(commits)}]
            
        # Preprocess messages
        processed_messages = self.preprocess_commit_messages(commits)
        
        # Create TF-IDF vectors
        try:
            X = self.vectorizer.fit_transform(processed_messages)
        except ValueError:
            # If vectorization fails, return all commits as single cluster
            return [{'id': 0, 'commits': commits, 'theme': 'all_commits', 'size': len(commits)}]
            
        # Cluster using DBSCAN
        clusterer = DBSCAN(
            eps=self.max_distance,
            min_samples=self.min_cluster_size,
            metric='cosine'
        )
        
        labels = clusterer.fit_predict(X)
        
        # Process clustering results
        clusters = []
        unique_labels = set(labels)
        
        for label_id in unique_labels:
            # Skip noise (-1)
            if label_id == -1:
                continue
                
            # Get commits in this cluster
            cluster_indices = np.where(labels == label_id)[0]
            cluster_commits = [commits[i] for i in cluster_indices]
            
            # Extract cluster theme (most common words)
            cluster_theme = self._extract_cluster_theme(cluster_commits)
            
            cluster = {
                'id': int(label_id),
                'commits': cluster_commits,
                'theme': cluster_theme,
                'size': len(cluster_commits)
            }
            clusters.append(cluster)
            
        # Handle unclustered commits (noise)
        noise_indices = np.where(labels == -1)[0]
        if len(noise_indices) > 0:
            noise_commits = [commits[i] for i in noise_indices]
            clusters.append({
                'id': -1,
                'commits': noise_commits,
                'theme': 'uncategorized',
                'size': len(noise_commits)
            })
            
        return clusters
    
    def _extract_cluster_theme(self, commits: List[Dict[str, Any]]) -> str:
        """Extract common theme from cluster commits"""
        try:
            # Combine all messages
            all_text = ' '.join(commit['message'].split('\n')[0] for commit in commits)
            
            # Clean up
            all_text = self.cleanup_pattern.sub(' ', all_text.lower())
            
            # Count word frequencies
            words = all_text.split()
            word_counts = Counter(words)
            
            # Remove common English stop words and short words
            stop_words = set(['the', 'and', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i', 'you', 'it'])
            filtered_counts = Counter()
            for word, count in word_counts.items():
                if word not in stop_words and len(word) > 2:
                    filtered_counts[word] = count
            
            # Get most common words
            common_words = []
            for word, count in filtered_counts.most_common(3):
                common_words.append(word)
            
            # Use most common words as theme, or default if none found
            if common_words:
                return '_'.join(common_words)
            else:
                return 'misc_changes'
        except Exception as e:
            print(f"Error extracting theme: {str(e)}")
            return 'error_theme' 