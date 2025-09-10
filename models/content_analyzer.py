import numpy as np
from datetime import datetime
import json

class ContentAnalyzer:
    def __init__(self):
        self.content_database = self._load_sample_content()
        self.analysis_history = []
    
    def _load_sample_content(self):
        """Load sample content data"""
        return {
            'content_001': {
                'title': 'Action Thriller Demo',
                'genre': 'action',
                'duration': 45,
                'rating': 'PG-13',
                'scenes': [
                    {'type': 'intro', 'engagement_potential': 0.6, 'duration': 3},
                    {'type': 'action', 'engagement_potential': 0.9, 'duration': 8},
                    {'type': 'dialogue', 'engagement_potential': 0.5, 'duration': 5},
                    {'type': 'chase', 'engagement_potential': 0.95, 'duration': 7},
                    {'type': 'climax', 'engagement_potential': 0.95, 'duration': 10},
                    {'type': 'resolution', 'engagement_potential': 0.4, 'duration': 12}
                ]
            },
            'content_002': {
                'title': 'Drama Series Demo',
                'genre': 'drama',
                'duration': 50,
                'rating': 'TV-14',
                'scenes': [
                    {'type': 'character_development', 'engagement_potential': 0.7, 'duration': 15},
                    {'type': 'conflict', 'engagement_potential': 0.8, 'duration': 20},
                    {'type': 'emotional_peak', 'engagement_potential': 0.85, 'duration': 10},
                    {'type': 'resolution', 'engagement_potential': 0.6, 'duration': 5}
                ]
            },
            'content_003': {
                'title': 'Comedy Special',
                'genre': 'comedy',
                'duration': 60,
                'rating': 'R',
                'scenes': [
                    {'type': 'opening', 'engagement_potential': 0.8, 'duration': 5},
                    {'type': 'main_act', 'engagement_potential': 0.9, 'duration': 45},
                    {'type': 'closing', 'engagement_potential': 0.75, 'duration': 10}
                ]
            }
        }
    
    def analyze_content(self, content_id):
        """Analyze content structure and engagement potential"""
        if content_id not in self.content_database:
            return {
                'error': 'Content not found',
                'content_id': content_id,
                'available_content': list(self.content_database.keys())
            }
        
        content = self.content_database[content_id]
        
        # Calculate overall engagement potential
        scene_scores = [scene['engagement_potential'] for scene in content['scenes']]
        scene_durations = [scene['duration'] for scene in content['scenes']]
        
        # Weighted average by scene duration
        total_duration = sum(scene_durations)
        weighted_engagement = sum(
            score * duration / total_duration 
            for score, duration in zip(scene_scores, scene_durations)
        )
        
        analysis = {
            'content_id': content_id,
            'title': content['title'],
            'genre': content['genre'],
            'duration': content['duration'],
            'rating': content['rating'],
            'predicted_engagement': weighted_engagement,
            'scene_count': len(content['scenes']),
            'optimization_opportunities': self._find_optimization_opportunities(content),
            'engagement_distribution': self._analyze_engagement_distribution(content['scenes']),
            'recommended_modifications': self._get_content_modifications(content, weighted_engagement)
        }
        
        # Store analysis
        self.analysis_history.append({
            'timestamp': datetime.now().isoformat(),
            'content_id': content_id,
            'analysis': analysis
        })
        
        return analysis
    
    def _find_optimization_opportunities(self, content):
        """Find scenes that could be optimized"""
        opportunities = []
        
        for i, scene in enumerate(content['scenes']):
            if scene['engagement_potential'] < 0.6:
                opportunities.append({
                    'scene_index': i,
                    'scene_type': scene['type'],
                    'current_potential': scene['engagement_potential'],
                    'duration': scene['duration'],
                    'suggestion': self._get_optimization_suggestion(scene)
                })
        
        return opportunities
    
    def _get_optimization_suggestion(self, scene):
        """Get specific optimization suggestion for a scene"""
        scene_type = scene['type']
        potential = scene['engagement_potential']
        
        suggestions = {
            'intro': 'Add more dynamic opening sequence',
            'dialogue': 'Increase dramatic tension or add visual elements',
            'resolution': 'Shorten or add surprise elements',
            'character_development': 'Add conflict or emotional stakes',
            'default': 'Consider pacing adjustments or content enhancement'
        }
        
        if potential < 0.3:
            return f"Consider replacing {scene_type} scene entirely"
        elif potential < 0.5:
            return f"Major revision needed: {suggestions.get(scene_type, suggestions['default'])}"
        else:
            return f"Minor optimization: {suggestions.get(scene_type, suggestions['default'])}"
    
    def _analyze_engagement_distribution(self, scenes):
        """Analyze how engagement is distributed across scenes"""
        potentials = [scene['engagement_potential'] for scene in scenes]
        
        return {
            'high_engagement_scenes': sum(1 for p in potentials if p > 0.8),
            'medium_engagement_scenes': sum(1 for p in potentials if 0.5 <= p <= 0.8),
            'low_engagement_scenes': sum(1 for p in potentials if p < 0.5),
            'engagement_variance': np.var(potentials),