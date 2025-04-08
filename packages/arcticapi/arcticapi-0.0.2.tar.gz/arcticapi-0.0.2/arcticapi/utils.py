"""Arctic utils."""

from .const import VERSION


def generate_headers():
    """Generate headers containing user agent."""
    return {
        "User-Agent": f"arcticapipy/{VERSION}",
    }
