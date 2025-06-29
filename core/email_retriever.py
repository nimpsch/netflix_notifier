import email
from email import policy

class EmailRetriever:
    def __init__(self, connection):
        self.connection = connection

    def fetch_email(self, email_id):
        result, data = self.connection.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        message = email.message_from_bytes(raw_email, policy=policy.default)
        return {
            "subject": message["subject"],
            "from": message["from"],
            "to": message["to"],
            "body": self.get_body(message)
        }

    def get_body(self, message):
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return message.get_payload(decode=True).decode()
