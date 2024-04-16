from dataclasses import dataclass, field
from email.message import Message


@dataclass
class EmailAttachment:
    name: str
    blob: bytes = field(repr=False)


@dataclass
class Email:
    uid: str
    raw_message: Message
    recipient: str
    sender: str
    subject: str
    date: str
    body: str
    attachments: list[EmailAttachment]

    @property
    def attachments_count(self) -> int:
        return len(self.attachments)


