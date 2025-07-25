import os
from dotenv import load_dotenv
from emails import Message

load_dotenv()

class MailConfig:
    MAIL_HOST = os.getenv("MAIL_HOST", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "angelmini508@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "wjordmxsuduomdzx")
    MAIL_FROM = os.getenv("MAIL_USERNAME")  
    MAIL_FROM_NAME = "Ecoshield360"  
    MAIL_TLS = True  
    MAIL_SSL = False  
    MAIL_DEBUG = False

    @staticmethod
    def get_message() -> Message:
        """Crea un objeto Message con la identidad de Ecoshield360"""
        return Message(
            mail_from=(MailConfig.MAIL_FROM_NAME, MailConfig.MAIL_FROM),
            smtp={
                "host": MailConfig.MAIL_HOST,
                "port": MailConfig.MAIL_PORT,
                "user": MailConfig.MAIL_USERNAME,
                "password": MailConfig.MAIL_PASSWORD,
                "tls": MailConfig.MAIL_TLS,
                "ssl": MailConfig.MAIL_SSL,
                "timeout": 30
            },
            headers={
                "X-Mailer": "Ecoshield360 Mail Service",
                "X-Priority": "1",
                "Importance": "high"
            }
        )