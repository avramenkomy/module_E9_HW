import os


class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'LongAndRandomSecretKey'

    MAX_CONTENT_LENGTH = 1024 * 1024 * 3
    MAX_FILE_SIZE = 1024 * 1024 * 3 + 1

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    UPLOAD_FOLDER_IMAGES = 'app\static\images'
    FOLDER_IMAGES = 'static\images'
