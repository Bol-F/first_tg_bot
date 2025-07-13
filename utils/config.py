from decouple import config
import sys


class Config:
    TOKEN = config("TOKEN", default=None)
    DEBUG = config("DEBUG", default=False, cast=bool)
    LOG_LEVEL = config("LOG_LEVEL", default="INFO")

    @classmethod
    def validate(cls):
        if not cls.TOKEN:
            print("❌ Error: TOKEN not found in environment variables")
            print("Please set TOKEN in your .env file or environment")
            sys.exit(1)
