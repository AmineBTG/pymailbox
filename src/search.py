from dataclasses import dataclass

@dataclass
class EmailSearchCriteria:
    unseen: bool | None = None
    sender: str | None = None
    subject: str | None = None
    body: str | None = None
    sent_on: str | None = None
    sent_since: str | None = None
    sent_before: str | None = None

    def as_imap_format(self) -> tuple[str]:

        imap_format = []

        if self.unseen is None:
            pass

        elif self.unseen:
            imap_format.append("UNSEEN")

        elif self.unseen == False:
            imap_format.append("SEEN")

        if self.sender:
            imap_format.extend(["FROM", self.sender])

        if self.subject:
            imap_format.extend(["SUBJECT", self.subject])

        if self.body:
            imap_format.extend(["BODY", self.body])

        if self.sent_on:
            imap_format.extend(["SENTON", self.sent_on])

        if self.sent_since:
            imap_format.extend(["SENTSINCE", self.sent_on])

        if self.sent_before:
            imap_format.extend(["SENTBEFORE", self.sent_on])

        return tuple(imap_format)
