import imaplib
from dataclasses import dataclass

from bs4 import BeautifulSoup
from imap_tools import MailBox, AND
import imaplib
from imap_tools import MailBox, AND
import os
from datetime import datetime, timedelta

from config.provider_model import Provider

UNSUBSCRIBE_KEYWORDS = [
    "unsubscribe", "opt out", "cancel subscription",  # English
    "désabonner", "se désinscrire", "résilier",       # French
    "darse de baja", "cancelar suscripción", "anular", # Spanish
    "abmelden", "abbestellen", "kündigen",           # German
    "disiscriviti", "annulla iscrizione"             # Italian
]
NETFLIX_KEYWORDS = ["ja, das war ich", "code anfordern"]

@dataclass
class Result:
    msg: str
    html: str
    url: str

class ProviderHandler:
    def __init__(self, provider = Provider):
        self.provider = provider
    def login(self, initial_folder="INBOX"):
        return MailBox(self.provider.imap_server).login(self.provider.username, self.provider.password, initial_folder=initial_folder)
    def fetch_newsletter_uids(self):
        uid_list = []
        with self.login() as mailbox:
            criteria = 'ALL'
            found_nums = mailbox.numbers(criteria)
            page_len = 3
            pages = int(len(found_nums) // page_len) + 1 if len(found_nums) % page_len else int(
                len(found_nums) // page_len)
            for page in range(pages):
                page_limit = slice(page * page_len, page * page_len + page_len)
                for msg in mailbox.fetch(criteria, bulk=True, limit=page_limit):
                    result = msg.text if msg.text else msg.html
                    if any(a in result.lower() for a in ["abbestellen", "abmelden", "newsletter", "unsubscribe"]):
                        print(f"Newsletter for EMAIL: {msg} found.")
                        uid_list.append(msg.uid)
        return uid_list

    def move(self, uid_list, destination_folder="Newsletter"):
        with self.login() as mailbox:
            mailbox.move(uid_list, destination_folder=destination_folder)


    @staticmethod
    def find_links(email_html, keywords=None):
        if keywords is None:
            keywords = UNSUBSCRIBE_KEYWORDS
        soup = BeautifulSoup(email_html, 'html.parser')
        links = []

        # Search for <a> tags containing unsubscribe keywords
        for a_tag in soup.find_all('a', href=True):
            link_text = a_tag.get_text(strip=True).lower()
            href = a_tag['href'].lower()

            # Check if keywords match the text or href attribute
            if any(keyword in link_text for keyword in keywords) or \
                    any(keyword in href for keyword in keywords):
                links.append(a_tag)

        # Search for <button> tags containing unsubscribe keywords
        for button_tag in soup.find_all('button'):
            button_text = button_tag.get_text(strip=True).lower()
            if any(keyword in button_text for keyword in keywords):
                links.append(button_tag)

        return links

    def click_on_newsletter(self, initial_folder="Newsletter"):
        with self.login(initial_folder) as mailbox:
            criteria = 'ALL'
            found_nums = mailbox.numbers(criteria)
            page_len = 3
            pages = int(len(found_nums) // page_len) + 1 if len(found_nums) % page_len else int(
                len(found_nums) // page_len)
            for page in range(pages):
                page_limit = slice(page * page_len, page * page_len + page_len)
                for msg in mailbox.fetch(criteria, bulk=True, limit=page_limit):
                    result = self.find_links(msg.html)
                    if result:
                        print(result)

    def fetch_new_mails(self, initial_folder="Newsletter"):
        ret = []
        with self.login(initial_folder) as mailbox:
            unseen_emails = mailbox.fetch(AND(seen=False))
            for msg in unseen_emails:
                results = self.find_links(msg.html, keywords=NETFLIX_KEYWORDS)
                for result in results:
                    print("Found a new mail!")
                    try:
                        ret.append(Result(msg="URL", html=str(result), url=result['href']))
                    except Exception as e:
                        print(e)
        return ret
