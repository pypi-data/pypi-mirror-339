"""Arctic constants."""

from dataclasses import dataclass
from enum import Enum


@dataclass
class Tenant:
    """Description of a tenant."""

    id: str
    name: str
    location: str

    def __str__(self):
        return f"{self.name} ({self.location})"


class Tenants(Enum):
    """List of tenant names."""

    BLUESTAR = Tenant("bluestar", "Bluestar", "Southampton")
    NCTX = Tenant("nctx", "Nottingham City Transport", "Nottingham")
    BRIGHTONHOVE = Tenant(
        "brightonhove", "Brighton and Hove Buses", "Brighton and Hove"
    )
    MOREBUS = Tenant("morebus", "Morebus", "Bournemouth")
    KONECTBUS = Tenant("konectbus", "Konectbus", "Norfolk")
    OXFORDBUS = Tenant("oxfordbus", "Oxford Bus Company", "Oxford")


VERSION = "0.0.2"
