import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    # Determine database URI: use external DATABASE_URL if provided,
    # use tmp SQLite on Vercel (readonly root), otherwise use local file.
    _db_url = os.getenv('DATABASE_URL')
    if _db_url:
        SQLALCHEMY_DATABASE_URI = _db_url
    elif os.getenv('VERCEL'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/movieweb.db'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'movieweb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    # weitere Settings …

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False