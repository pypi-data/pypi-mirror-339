import django
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives


def to_dict(email_message):
    email_message_data = {
        "cc": email_message.cc,
        "subject": email_message.subject,
        "body": email_message.body,
        "from_email": email_message.from_email,
        "to": email_message.to,
        "bcc": email_message.bcc,
        "attachments": email_message.attachments,
        "headers": email_message.extra_headers,
        "reply_to": email_message.reply_to,
    }
    if isinstance(email_message, EmailMultiAlternatives):
        email_message_data["alternatives"] = email_message.alternatives
        if django.VERSION >= (5, 2):
            email_message_data["alternatives"] = [
                (content, mimetype) for content, mimetype in email_message.alternatives
            ]
    return email_message_data


def from_dict(email_message_data):
    kwargs = dict(email_message_data)
    if alternatives := kwargs.pop("alternatives", None):
        if django.VERSION >= (5, 2):
            alternatives = [(content, mimetype) for content, mimetype in alternatives]
        return EmailMultiAlternatives(alternatives=alternatives, **kwargs)
    return EmailMessage(**kwargs)
