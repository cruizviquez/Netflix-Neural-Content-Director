import numpy as np
from datetime import datetime
import json

class EngagementTracker:
    def __init__(self):
        self.tracking_history = []
        self.session_data = {}
    
    def calculate_engagement(self, data):
        """Calculate engagement score from user interaction data"""
        
        # Basic engagement calculation
        base_score = 0.7  # Default engagement
        
        action = data.get('action', 'viewing')
        video_time = data.get('video_time', 0)
        session_id = data.get('session_id', 'unknown')
        
        # Adjust score based on user actions
        if action == 'pause':
            score = max(0.3, base_score - 0.2)
        elif action == 'rewind':
            score = min(1.0, base_score + 0.1)  # Interest in content
        elif action == 'skip':
            score = max(0.1, base_score - 0.4)
        elif action == 'fast_forward':
            score = max(0.2, base_score - 0.3)
        elif action == 'play':
            score = min(1.0, base_score + 0.1)
        elif action == 'volume_up':
            score = min(1.0, base_score + 0.05)
        elif action == 'fullscreen':
            score = min(1.0, base_score + 0.15)  # High engagement indicator
        else:
            score = base_score
        
        # Add some randomness to simulate real engagement variation
        score += np.random.normal(0, 0.05)
        score = max(0, min(1, score))
        
        # Store tracking data
        tracking_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'action': action,
            'engagement_score': score,
            'video_time': video_time
        }
        
        self.tracking_history.append(tracking_entry)
        
        # Update session data
        if session_id not in self.session_data:
            self.session_data[session_id] = []
        self.session_data[session_id].append(tracking_entry)
        
        return score
    
    def get_engagement_trend(self, session_id):
        """Get engagement trend over time for a specific session"""
        if session_id not in self.session_data:
            return 'stable'
        
        session_scores = [entry['engagement_score'] for entry in self.session_data[session_id]]
        
        if len(session_scores) < 3:
            return 'stable'
        
        # Compare recent scores with earlier scores
        recent_avg = np.mean(session_scores[-3:])
        earlier_avg = np.mean(session_scores[-6:-3]) if len(session_scores) >= 6 else np.mean(session_scores[:-3])
        
        trend = recent_avg - earlier_avg
        
        if trend > 0.1:
            return 'increasing'
        elif trend < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def get_session_analytics(self, session_id):
        """Get detailed analytics for a session"""
        if session_id not in self.session_data:
            return {'error': 'Session not found'}
        
        session_entries = self.session_data[session_id]
        
        if not session_entries:
            return {'error': 'No data for session'}
        
        scores = [entry['engagement_score'] for entry in session_entries]
        actions = [entry['action'] for entry in session_entries]
        
        analytics = {
            'session_id': session_id,
            'total_interactions': len(session_entries),
            'avg_engagement': np.mean(scores),
            'max_engagement': np.max(scores),
            'min_engagement': np.min(scores),
            'engagement_trend': self.get_engagement_trend(session_id),
            'action_counts': {action: actions.count(action) for action in set(actions)},
            'session_duration': self._calculate_session_duration(session_entries),
            'engagement_stability': np.std(scores)
        }
        
        return analytics
    
    def _calculate_session_duration(self, session_entries):
        """Calculate session duration in minutes"""
        if len(session_entries) < 2:
            return 0
        
        start_time = datetime.fromisoformat(session_entries[0]['timestamp'])
        end_time = datetime.fromisoformat(session_entries[-1]['timestamp'])
        
        duration = (end_time - start_time).total_seconds() / 60  # Convert to minutes
        return round(duration, 2)
    
    def get_global_analytics(self):
        """Get analytics across all sessions"""
        if not self.tracking_history:
            return {'error': 'No tracking data available'}
        
        all_scores = [entry['engagement_score'] for entry in self.tracking_history]
        all_actions = [entry['action'] for entry in self.tracking_history]
        
        analytics = {
            'total_interactions': len(self.tracking_history),
            'unique_sessions': len(self.session_data),
            'avg_engagement_global': np.mean(all_scores),
            'engagement_distribution': {
                'high': sum(1 for score in all_scores if score > 0.7),
                'medium': sum(1 for score in all_scores if 0.4 <= score <= 0.7),
                'low': sum(1 for score in all_scores if score < 0.4)
            },
            'most_common_actions': self._get_top_actions(all_actions),
            'engagement_trends': self._analyze_global_trends()
        }
        
        return analytics
    
    def _get_top_actions(self, actions, top_n=5):
        """Get the most common actions"""
        action_counts = {}
        for action in actions:
            action_counts[action] = action_counts.get(action, 0) + 1
        
        # Sort by count and return top N
        sorted_actions = sorted(action_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_actions[:top_n]
    
    def _analyze_global_trends(self):
        """Analyze engagement trends across all sessions"""
        trends = {}
        
        for session_id in self.session_data:
            trend = self.get_engagement_trend(session_id)
            trends[trend] = trends.get(trend, 0) + 1
        
        return trends
    
    def clear_old_data(self, hours_to_keep=24):
        """Clear tracking data older than specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours_to_keep)
        
        # Filter tracking history
        self.tracking_history = [
            entry for entry in self.tracking_history 
            if datetime.fromisoformat(entry['timestamp']) > cutoff_time
        ]
        
        # Filter session data
        for session_id in list(self.session_data.keys()):
            self.session_data[session_id] = [
                entry for entry in self.session_data[session_id]
                if datetime.fromisoformat(entry['timestamp']) > cutoff_time
            ]
            
            # Remove empty sessions
            if not self.session_data[session_id]:
                del self.session_data[session_id]