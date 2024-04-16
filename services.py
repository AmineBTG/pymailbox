import email
from abc import ABC, abstractmethod
from imaplib import IMAP4_SSL

from exceptions import EmailNotFound, NoSearchResultsFound
from search import Email, EmailSearchCriteria
from utils import get_email_attachments, get_email_body, get_logger

logger = get_logger(__name__)


class EmailService(ABC):
    """
    Email service Abstract Base Class. Services such sa Gmail, Outlook, etc. must inherit from this class.
    Wrapper arround Python builtin IMAP4_SSL class.
    """

    def __init__(self, username: str, password: str, imap_server: str, imap_port: int = 993) -> None:
        """Wrapper arround Python IMAP4_SSL class.

        Args:
            username (str): Email account email address
            password (str): Account password
            imap_server (str): Imap Server URL (ex: imap.gmail.com or outlook.office365.com)
            imap_port (int, optional): Imap Server Port. Defaults to 993.
        """
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port

        self.connection = IMAP4_SSL(host=imap_server, port=imap_port)
        self._status, self._auth = self.connection.login(username, password)

        if self._status == "OK":
            logger.info(f"Successfully authenticated to '{self.username}'")

    def __repr__(self):
        return f'{self.__class__.__name__}(username="{self.username}", password="***********")'

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        self.connection.close()

    def get_email_by_uid(self, uid: str) -> Email:
        """
        Fetching from Inbox, email by its UID following (RFC822) standar.

        Ex: self.connection.uid("FETCH", uid, "(RFC822)").

        Raises:
            EmailNotFound: if email is not found within the Inbox.

        Returns and Email object.
        """

        self.connection.select("INBOX")
        _, data = self.connection.uid("FETCH", uid, "(RFC822)")

        if not data:
            raise EmailNotFound(f"No email with UID '{uid}' found !")

        message = email.message_from_bytes(data[0][1])
        body = get_email_body(message)
        attachments = get_email_attachments(message)

        email_message = Email(
            uid=uid,
            raw_message=message,
            recipient=message["To"],
            sender=message["From"],
            subject=message["Subject"],
            date=message["Date"],
            body=body,
            attachments=attachments,
        )

        return email_message

    def mark_email_as_unseen(self, uid: str) -> None:
        """
        Mark the email as unseen / unread
        """
        logger.info(self.connection.uid("STORE", uid, "-FLAGS", "\\Seen"))

    def delete_email(self, uid: str) -> None:
        """
        BE CAREFULL - Cannot go back once done.
        Deleted email will have a different UID if it is put back into INBOX
        """
        logger.info(self.connection.uid("STORE", uid, "+FLAGS", "\\Deleted"))

    @abstractmethod
    def search_email(self, critera: EmailSearchCriteria) -> Email: ...


class GmailEmailService(EmailService):

    def search_email(self, critera: EmailSearchCriteria) -> Email:
        """Search for email with the Inbox following the passed Criteria.

        Args:
            critera (EmailSearchCriteria): Email Search Criteria. ex; EmailSearchCriteria(unseen=True, sender="Amine", senton="07-DEC-2023")

        Raises:
            NoSearchResultsFound: if no email found with passed criteria

        Returns:
            Email: Email object. If multiple emails found with passed criteria, the oldest email will be returned.
        """

        self.connection.select("INBOX")
        _, search_results = self.connection.uid("SEARCH", "CHARSET", "UTF-8", *critera.as_imap_format())

        if not search_results or search_results == [b""]:
            raise NoSearchResultsFound(f"No email found with following critera: {critera.as_imap_format()}.")

        search_results = search_results[0].split()

        if len(search_results) > 1:
            logger.warning(f"IMPORTANT: Multiple emails ({len(search_results)}) found with following critera: {critera.as_imap_format()} !")
            logger.warning(f"Emails found: {search_results}. Returned email UID (FIFO): {search_results[0]}.")

        email = self.get_email_by_uid(search_results[0])

        return email


class OutlookEmailService(EmailService):

    def search_email(self, critera: EmailSearchCriteria) -> Email:
        """Search for email with the Inbox following the passed Criteria.

        Args:
            critera (EmailSearchCriteria): Email Search Criteria. ex; EmailSearchCriteria(unseen=True, sender="Amine", senton="07-DEC-2023")

        Raises:
            NoSearchResultsFound: if no email found with passed criteria

        Returns:
            Email: Email object. If multiple emails found with passed criteria, the oldest email will be returned.
        """

        self.connection.select("INBOX")
        _, search_results = self.connection.uid("SEARCH", *critera.as_imap_format())

        if not search_results or search_results == [b""]:
            raise NoSearchResultsFound(f"No email found with following critera: {critera.as_imap_format()}.")

        search_results = search_results[0].split()

        if len(search_results) > 1:
            logger.warning(f"IMPORTANT: Multiple emails ({len(search_results)}) found with following criteria: {critera.as_imap_format()} !")
            logger.warning(f"Emails found: {search_results}. Returned email UID (FIFO): {search_results[0]}.")

        email = self.get_email_by_uid(search_results[0])

        return email
