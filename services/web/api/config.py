import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv("SECRET", 'Th1s1ss3cr3t')