class Config:
    pass

class DevelopmentConfig():
    TOKEN = 'jopUIHp1239Oads'

class ProductionConfig():
    TOKEN = '0LAFvVAbcufUX1SVNSaRBCp2PgIqVVz4'
    
config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
    'default': DevelopmentConfig
}