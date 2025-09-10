import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'neural-content-director-2024-key'
    DEBUG = True
    
    # Redis configuration (for production)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # ML Model settings
    MODEL_UPDATE_INTERVAL = 300  # 5 minutes
    ENGAGEMENT_THRESHOLD = 0.6
    
    # Content optimization settings
    MAX_OPTIMIZATIONS_PER_SESSION = 5
    REAL_TIME_UPDATES = True
    
    # Analytics settings
    ANALYTICS_RETENTION_DAYS = 30
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}