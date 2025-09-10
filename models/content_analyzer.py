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
            'engagement_variance': float(np.var(potentials)),
            'avg_engagement': float(np.mean(potentials)),
            'engagement_range': float(max(potentials) - min(potentials))
        }
    
    def _get_content_modifications(self, content, current_engagement):
        """Get recommended content modifications"""
        modifications = []
        
        if current_engagement < 0.5:
            modifications.extend([
                {
                    'type': 'major_restructure',
                    'priority': 'high',
                    'description': 'Content needs significant restructuring',
                    'actions': ['Reorder scenes', 'Cut low-engagement scenes', 'Add action sequences']
                },
                {
                    'type': 'pacing_adjustment',
                    'priority': 'high', 
                    'description': 'Dramatically increase pacing',
                    'actions': ['Speed up transitions', 'Reduce dialogue scenes', 'Increase visual interest']
                }
            ])
        elif current_engagement < 0.7:
            modifications.extend([
                {
                    'type': 'scene_optimization',
                    'priority': 'medium',
                    'description': 'Optimize individual scenes',
                    'actions': ['Enhance audio', 'Improve transitions', 'Add visual effects']
                },
                {
                    'type': 'content_highlighting',
                    'priority': 'medium',
                    'description': 'Highlight best content',
                    'actions': ['Promote high-engagement scenes', 'Add teaser elements']
                }
            ])
        else:
            modifications.append({
                'type': 'enhancement',
                'priority': 'low',
                'description': 'Content is performing well',
                'actions': ['Minor optimizations', 'A/B test variations']
            })
        
        return modifications
    
    def get_content_recommendations(self, user_engagement_history):
        """Recommend content based on user's engagement history"""
        if not user_engagement_history:
            return list(self.content_database.keys())[:2]  # Default recommendations
        
        # Analyze user preferences
        avg_engagement = np.mean([entry.get('engagement_score', 0.5) for entry in user_engagement_history])
        preferred_genres = self._extract_preferred_genres(user_engagement_history)
        
        recommendations = []
        
        for content_id, content in self.content_database.items():
            content_analysis = self.analyze_content(content_id)
            
            # Score content based on user preferences
            score = self._calculate_recommendation_score(
                content_analysis, avg_engagement, preferred_genres
            )
            
            recommendations.append({
                'content_id': content_id,
                'title': content['title'],
                'genre': content['genre'],
                'score': score,
                'predicted_engagement': content_analysis['predicted_engagement']
            })
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:3]
    
    def _extract_preferred_genres(self, engagement_history):
        """Extract preferred genres from engagement history"""
        # This is a simplified version - in practice, you'd track content IDs
        # and map them to genres based on what content the user engaged with
        return ['action', 'drama']  # Default preferences
    
    def _calculate_recommendation_score(self, content_analysis, user_avg_engagement, preferred_genres):
        """Calculate recommendation score for content"""
        base_score = content_analysis['predicted_engagement']
        
        # Boost score if genre matches preferences
        if content_analysis['genre'] in preferred_genres:
            base_score *= 1.2
        
        # Adjust based on user's typical engagement level
        engagement_match = 1 - abs(base_score - user_avg_engagement)
        
        return base_score * 0.7 + engagement_match * 0.3
    
    def get_analytics_summary(self):
        """Get summary analytics of all content analysis"""
        if not self.analysis_history:
            return {'message': 'No analysis data available'}
        
        all_engagements = [
            analysis['analysis']['predicted_engagement'] 
            for analysis in self.analysis_history
        ]
        
        genres = [
            analysis['analysis']['genre']
            for analysis in self.analysis_history
        ]
        
        return {
            'total_analyses': len(self.analysis_history),
            'avg_content_engagement': float(np.mean(all_engagements)),
            'genre_distribution': {genre: genres.count(genre) for genre in set(genres)},
            'engagement_trends': {
                'high': sum(1 for e in all_engagements if e > 0.7),
                'medium': sum(1 for e in all_engagements if 0.4 <= e <= 0.7), 
                'low': sum(1 for e in all_engagements if e < 0.4)
            }
        }