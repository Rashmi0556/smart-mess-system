import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ.get('MYSQL_USER')}"
        f":{os.environ.get('MYSQL_PASSWORD')}"
        f"@{os.environ.get('MYSQL_HOST')}"
        f"/{os.environ.get('MYSQL_DB')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False