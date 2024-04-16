import email.message
import logging

from .models import EmailAttachment


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s | %(name)s | %(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    logger_stream_handler = logging.StreamHandler()
    logger_stream_handler.setFormatter(formatter)

    logger.addHandler(logger_stream_handler)

    return logger


def get_email_body(message: email.message.Message) -> str:
    """Return the email body of an email object

    Args:
        message (email.message.EmailMessage): EmailMessage to be parsed

    Returns:
        str: Email body
    """
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            return part.get_payload()

    return None


def get_email_attachments(message: email.message.Message) -> list[EmailAttachment]:
    """Return a list EmailAttachment

    Args:
        message (email.message.EmailMessage): EmailMessage to be parsed

    Returns:
        list[EmailAttachment]: list of EmailAttachments
    """
    attachments: list[EmailAttachment] = []

    for part in message.walk():

        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue

        fileName = part.get_filename()
        blob = part.get_payload(decode=True)

        attachments.append(
            EmailAttachment(
                name=fileName,
                blob=blob,
            )
        )

    return attachments
