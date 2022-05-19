import os


class Config:
    # SECRET_KEY = os.environ.get("SECRET_KEY")
    SECRET_KEY = 'youshouldusethis'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    SQLALCHEMY_DATABASE_URI = "sqlite:///vacationdb"
    # SECRET_KEY = os.environ.get("SECRET_KEY")
    SECRET_KEY = 'youshouldusethis'
    #SECRET_KEY = os.environ.get("SECRET_KEY")
    SECRET_KEY ='youshouldusethis'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
    # uri = os.environ.get("DATABASE_URL")  # or other relevant config var
    # if uri.startswith("postgres://"):
    #     uri = uri.replace("postgres://", "postgresql://", 1)
    # # rest of connection code using the connection string `uri`
    # SQLALCHEMY_DATABASE_URI = uri


config_option = {
    'development': DevConfig,
    'production': ProdConfig,
    'default': DevConfig
}
