import ssl, os, smtplib
from email.mime.text import MIMEText
from src.utils.transfer import Transfer
from email.mime.multipart import MIMEMultipart


class EmailService:
    @staticmethod
    def send_mail(email: str, text: str) -> Transfer:
        res = Transfer()
        try:
            context = ssl.create_default_context()
            port = os.getenv("EMAIL_PORT")

            body = MIMEMultipart("alternative")
            body["Subject"] = "Recuperação de senha Lucy"
            body["From"] = os.getenv("EMAIL_FROM")
            body["To"] = email
            body.attach(MIMEText(text, "plain"))

            with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
                server.starttls(context=context)
                server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASS"))
                server.sendmail(os.getenv("EMAIL_FROM"), email, body.as_string())

        except BaseException as e:
            res.set_status_code(500)
            res.set_message(str(e))
        finally:
            return res
