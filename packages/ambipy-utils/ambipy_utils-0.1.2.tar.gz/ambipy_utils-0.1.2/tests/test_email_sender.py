from unittest.mock import MagicMock, patch

from ambipy_utils.email_sender import EmailSender
from tests.commons.status_code import HttpStatusCode


class TestEmailSender:
    @staticmethod
    @patch("sendgrid.SendGridAPIClient")
    def test_send_email_success(mock):
        mock_response = MagicMock()
        mock_response.status_code = HttpStatusCode.ACCEPTED
        mock.return_value.client.mail.send.post.return_value = mock_response

        email_sender = EmailSender(sendgrid_api_key="fake_api_key")
        receivers = ["test@example.com"]
        subject = "Test Subject"
        content = "<p>Test Content</p>"
        from_email = "sender@example.com"
        from_name = "Sender Name"

        response = email_sender.send(
            receivers, subject, content, from_email, from_name
        )

        assert response.status_code == HttpStatusCode.ACCEPTED
        mock.return_value.client.mail.send.post.assert_called_once()
        called_args = mock.return_value.client.mail.send.post.call_args[1]
        assert "request_body" in called_args

    @staticmethod
    @patch("sendgrid.SendGridAPIClient")
    def test_send_email_failure(mock):
        mock_response = MagicMock()
        mock_response.status_code = HttpStatusCode.BAD_REQUEST
        mock.return_value.client.mail.send.post.return_value = mock_response

        email_sender = EmailSender(sendgrid_api_key="fake_api_key")
        receivers = ["test@example.com"]
        subject = "Test Subject"
        content = "<p>Test Content</p>"
        from_email = "sender@example.com"
        from_name = "Sender Name"

        response = email_sender.send(
            receivers, subject, content, from_email, from_name
        )

        assert response.status_code == HttpStatusCode.BAD_REQUEST
        mock.return_value.client.mail.send.post.assert_called_once()
