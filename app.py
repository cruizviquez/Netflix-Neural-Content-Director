from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import json
import numpy as np
from datetime import datetime
from models.neural_director import NeuralDirector
from models.engagement_tracker import EngagementTracker
from models.content_analyzer import ContentAnalyzer
import uuid
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'neural-content-director-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize ML models
print("🧠 Initializing Neural Content Director...")
neural_director = NeuralDirector()
engagement_tracker = EngagementTracker()
content_analyzer = ContentAnalyzer()

# Store active user sessions
active_sessions = {}

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/viewer')
def viewer():
    """Video viewer with real-time optimization"""
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    
    # Initialize user session
    active_sessions[session_id] = {
        'start_time': datetime.now(),
        'engagement_score': 0.8,
        'viewing_pattern': [],
        'content_modifications': [],
        'total_optimizations': 0
    }
    
    print(f"🎬 New viewer session: {session_id}")
    return render_template('viewer.html', session_id=session_id)

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    return render_template('dashboard.html')

@app.route('/analytics')
def analytics():
    """Detailed analytics page"""
    return render_template('analytics.html')

@app.route('/api/content/<content_id>')
def get_content(content_id):
    """Get optimized content based on user preferences"""
    session_id = session.get('session_id')
    
    if session_id not in active_sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    # Get user's current engagement data
    user_data = active_sessions[session_id]
    
    # Analyze and optimize content
    optimized_content = neural_director.optimize_content(
        content_id, 
        user_data['engagement_score'],
        user_data['viewing_pattern']
    )
    
    return jsonify(optimized_content)

@socketio.on('connect')
def handle_connect():
    print('🔗 Client connected')
    emit('status', {'msg': 'Connected to Neural Content Director'})

@socketio.on('engagement_data')
def handle_engagement_data(data):
    """Handle real-time engagement tracking"""
    session_id = data.get('session_id')
    
    if session_id in active_sessions:
        # Process engagement data
        engagement_score = engagement_tracker.calculate_engagement(data)
        
        # Update user session
        active_sessions[session_id]['engagement_score'] = engagement_score
        active_sessions[session_id]['viewing_pattern'].append({
            'timestamp': datetime.now().isoformat(),
            'engagement': engagement_score,
            'user_action': data.get('action', 'viewing'),
            'video_time': data.get('video_time', 0)
        })
        
        # Get real-time recommendations
        recommendations = neural_director.get_realtime_recommendations(
            session_id, engagement_score
        )
        
        # Emit recommendations back to client
        emit('content_optimization', {
            'engagement_score': engagement_score,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat(),
            'session_stats': {
                'total_interactions': len(active_sessions[session_id]['viewing_pattern']),
                'session_duration': (datetime.now() - active_sessions[session_id]['start_time']).seconds
            }
        })

@app.route('/api/analytics')
def get_analytics():
    """Get system analytics"""
    if not active_sessions:
        return jsonify({
            'total_sessions': 0,
            'avg_engagement': 0,
            'content_modifications': 0,
            'performance_metrics': neural_director.get_performance_metrics()
        })
    
    analytics_data = {
        'total_sessions': len(active_sessions),
        'avg_engagement': np.mean([s['engagement_score'] for s in active_sessions.values()]),
        'content_modifications': sum(len(s['content_modifications']) for s in active_sessions.values()),
        'performance_metrics': neural_director.get_performance_metrics(),
        'active_sessions': len([s for s in active_sessions.values() if 
                              (datetime.now() - s['start_time']).seconds < 3600])
    }
    
    return jsonify(analytics_data)

@app.route('/api/session/<session_id>/stats')
def get_session_stats(session_id):
    """Get individual session statistics"""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session_data = active_sessions[session_id]
    duration = (datetime.now() - session_data['start_time']).seconds
    
    stats = {
        'session_id': session_id,
        'duration_seconds': duration,
        'engagement_score': session_data['engagement_score'],
        'total_interactions': len(session_data['viewing_pattern']),
        'optimizations_applied': len(session_data['content_modifications']),
        'viewing_pattern': session_data['viewing_pattern'][-10:]  # Last 10 interactions
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    print("🚀 Starting Neural Content Director...")
    print("🌐 Access the application at: http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)