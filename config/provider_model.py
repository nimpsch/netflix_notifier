from dataclasses import dataclass


@dataclass
class Provider:
    name: str
    imap_server: str
    smtp_server: str
    imap_port: int
    smtp_port: int
    username: str
    password: str
