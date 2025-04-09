import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail


class EmailSender:
    """
    A class to send emails using SendGrid.
    Attributes:
        SENDGRID_API_KEY (str): The API key for SendGrid.
    Methods:
        send(
            receivers: list[str],
            subject: str,
            content: str,
            from_email: str,
            from_name: str,
        ):
            Sends an email to the specified receivers with
            the given subject and content.
    """

    SENDGRID_API_KEY: str

    def __init__(
        self,
        sendgrid_api_key: str,
    ):
        self.SENDGRID_API_KEY = sendgrid_api_key

    def send(
        self,
        receivers: list[str],
        subject: str,
        content: str,
        from_email: str,
        from_name: str,
    ):
        """
        Sends an email to the specified receivers with the given subject
        and content.
        Args:
            receivers (list[str]): List of email addresses to send
            the email to.
            subject (str): Subject of the email.
            content (str): HTML content of the email.
            from_email (str): Sender's email address.
            from_name (str): Sender's name.
        Returns:
            {
                "status_code": int,
                "message": str,
                "body": dict,
                "headers": dict,
            }
        """
        sg = sendgrid.SendGridAPIClient(api_key=self.SENDGRID_API_KEY)

        email_from = Email(email=from_email, name=from_name)
        content = Content("text/html", content)
        mail = Mail(email_from, receivers, subject, content)

        mail_json = mail.get()
        return sg.client.mail.send.post(request_body=mail_json)
