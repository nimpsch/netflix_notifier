from enum import Enum


class ProviderName(str, Enum):
    GMX = "gmx"
    GMAIL = "gmail"
    YAHOO = "yahoo"
    OUTLOOK = "outlook"
