from emails.template import JinjaTemplate
from infrastructure.config.mailConfig import MailConfig

class MailService:
    @staticmethod
    async def send_email(to: str, subject: str, html_content: str):
        message = MailConfig.get_message()

        # Asignamos los datos del correo
        message.subject = subject
        message.to = to
        message.html = JinjaTemplate(html_content)

        # Enviamos el correo
        response = message.send()

        if response.status_code not in [200, 250]:
            raise Exception(f"Fallo al enviar correo: {response.status_code} - {response.message}")