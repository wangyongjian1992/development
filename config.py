import os


class Config:
    SECRET_KEY = 'hard to guess string'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'yongjianw_92@163.com'
    MAIL_PASSWORD = 'sdlc0123'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'yongjianw_92@163.com'
    FLASKY_ADMIN = 'yongjianw_92@163.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_POSTS_PER_PAGE = 15
    FLASKY_FOLLOWERS_PER_PAGE = 15

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:wangyongjian3@localhost/web_dev'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:wangyongjian3@localhost/web_test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:wangyongjian3@localhost/web_pro'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
