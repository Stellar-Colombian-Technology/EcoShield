import os
from datetime import datetime, timedelta
from pathlib import Path
from fastapi import BackgroundTasks
from infrastructure.model import User, EmailVerificationToken
from infrastructure.config.Db import get_db
from infrastructure.config.mailConfig import MailService  

class EmailService:
    @staticmethod
    async def send_verification_email(
        user: User,
        base_url: str = None,
        background_tasks: BackgroundTasks = None
    ):
        db = next(get_db())  
        
        try:
            token = EmailVerificationToken.create_for_user(user.id)
            db.add(token)
            db.commit()
            
            base_url = base_url or os.getenv("BASE_URL", "http://localhost:3000")
            verification_url = f"{base_url}/api/v1/auth/verify-email?token={token.token}"
            
            template_path = Path("shared/layouts/email.html")
            with open(template_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            html_content = html_content \
                .replace('{{name}}', user.first_name) \
                .replace('{{verificationUrl}}', verification_url)
            
            email_data = {
                "to": user.email,
                "subject": "Verifica tu cuenta en Ecoshield360",
                "html_content": html_content
            }
            
            if background_tasks:
                background_tasks.add_task(
                    MailService.send_email,
                    **email_data
                )
            else:
                await MailService.send_email(**email_data)
                
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()