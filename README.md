# Fetching email content and attached files with Python made easy.

This is wrapper arround python builtin IMAP4 SSL client that simplifies searching, finding and fetching emails.

Emails are then fetched, parsed and store in simple Python Email object. 

Email bodies, headers and attached files can then be accessed very easily.

## Installation
```
pip install -e git+https://github.com/AmineBTG/pymailbox
``` 

## Supported and tested Email Services
The follwoing emails services are supported and have been tested :
-   Gmail
-   Outlook

Other services could work fine using 'OutlookEmailService' however this is not garanteed.

## Quistart
```python
import os

from src.search import EmailSearchCriteria
from src.services import GmailEmailService, OutlookEmailService

# get credentials from environment variables
outlook_account_username = os.environ.get("OUTLOOK_USERNAME")
outlook_account_password = os.environ.get("OUTLOOK_PASSWORD")

gmail_account_username = os.environ.get("GMAIL_USERNAME")
gmail_account_password = os.environ.get("GMAIL_PASSWORD")

# Instantiate IMAP clients and connect to the email services.
outlook = OutlookEmailService(
    username=outlook_account_username,
    password=outlook_account_password,
    imap_server="outlook.office365.com",
    imap_port=993,
)

gmail = GmailEmailService(
    username=gmail_account_username,
    password=gmail_account_password,
    imap_server="imap.gmail.com",
    imap_port=993,
)

# define search criteria
outlook_criteria = EmailSearchCriteria(unseen=None, sender="gmail")
gmail_criteria = EmailSearchCriteria(unseen=False, sender="H7229", sent_on="15-APR-2024")

# search for email using the above search criteria
outlook_email = outlook.search_email(outlook_criteria)
gmail_email = gmail.search_email(gmail_criteria)

# printing some returned email attributes
print(outlook_email.date)
#> Mon, 15 Apr 2024 17:43:08 +0200

print(outlook_email.sender)
#> "Boutaghou, Amine (Gmail)" <boutaghouamine@gmail.com>

print(outlook_email.attachments_count)
#> 0

print(gmail_email.date)
#> Mon, 15 Apr 2024 14:27:08 +0000 (UTC)

print(gmail_email.sender)
#> Pullman Paris Tour Eiffel <H7229@accor.com>

print(gmail_email.attachments_count)
#> 1

print(gmail_email.attachments[0].name)
#> H7229_20240415_manager_report_23990247.txt

print(gmail_email.attachments[0].blob[:10])
#> b'MASTER_VAL'


# reading the attached csv file with Pandas
from io import BytesIO
import pandas as pd

df = pd.read_csv(BytesIO(gmail_email.attachments[0].blob))
print(df.shape)
# (17, 103304)
```