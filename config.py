class Config:
    pass

class DevelopmentConfig():
    TOKEN = 'jopUIHp1239Oads'
    REDIS_URL = "redis://:""@localhost:6379/1"

class ProductionConfig():
    TOKEN = '0LAFvVAbcufUX1SVNSaRBCp2PgIqVVz4'
    
config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
    'default': DevelopmentConfig
}