from dataclasses import dataclass


@dataclass
class EmailSearchCriteria:
    """X-GM-RAW is specific to Gmail (https://developers.google.com/gmail/imap/imap-extensions#extension_of_the_search_command_x-gm-raw)"""

    unseen: bool | None = None
    to: str | None = None
    sender: str | None = None
    subject: str | None = None
    body: str | None = None
    sent_on: str | None = None
    sent_since: str | None = None
    sent_before: str | None = None
    x_gm_raw: str | None = None
    folder: str = "INBOX"

    def as_imap_format(self) -> tuple[str]:
        imap_format = []

        if self.unseen is None:
            pass

        elif self.unseen:
            imap_format.append("UNSEEN")

        elif self.unseen == False:  # noqa: E712
            imap_format.append("SEEN")

        if self.sender:
            imap_format.extend(["FROM", f'"{self.sender}"'])

        if self.to:
            imap_format.extend(["TO", f'"{self.to}"'])

        if self.subject:
            imap_format.extend(["SUBJECT", f'"{self.subject}"'])

        if self.body:
            imap_format.extend(["BODY", f'"{self.body}"'])

        if self.sent_on:
            imap_format.extend(["SENTON", self.sent_on])

        if self.sent_since:
            imap_format.extend(["SENTSINCE", self.sent_since])

        if self.sent_before:
            imap_format.extend(["SENTBEFORE", self.sent_before])

        if self.x_gm_raw:
            imap_format.extend(["X-GM-RAW", f'"{self.x_gm_raw}"'])

        return tuple(imap_format)
