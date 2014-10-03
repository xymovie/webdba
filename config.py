from __future__ import print_function
import os
from getpass import getpass

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #MAIL_SERVER = 'smtp.googlemail.com'
    #MAIL_PORT = 587
    #MAIL_USE_TLS = True
    #MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[WebDBA]'
    FLASKY_MAIL_SENDER = 'WebDBA Admin <admin@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    DBNAME = 'sample'
    DBUSER = 'asif'
    DBPW = os.environ.get('DBPW') or getpass()
    DBHOST = 'localhost'
    DBPORT = '60100'
    SQLALCHEMY_DATABASE_URI = 'ibm_db_sa://{user}:{password}@{host}:{port}/{dbname}'.format(
            user = DBUSER
            , password = DBPW
            , host = DBHOST
            , port = DBPORT
            , dbname = DBNAME)

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
            Config.SQLALCHEMY_DATABASE_URI

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            Config.SQLALCHEMY_DATABASE_URI

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            Config.SQLALCHEMY_DATABASE_URI

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

if __name__ == '__main__':
    d = DevelopmentConfig()
    print(d.SQLALCHEMY_DATABASE_URI)

