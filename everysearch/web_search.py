"""
web_search.py

Checks whether a given username exists on popular social platforms
by requesting their public profile URL pattern.

Reliability varies by platform:
- TikTok: fairly reliable (returns 404 for missing users)
- Instagram / Facebook: often return 200 for both real and fake
  usernames because the real profile data loads via JS behind a
  login wall. Treat these as "likely" rather than certain.
"""

import requests
from dataclasses import dataclass
from typing import List, Optional

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

PLATFORM_URLS = {
    "instagram": "https://www.instagram.com/{username}/",
    "tiktok": "https://www.tiktok.com/@{username}",
    "facebook": "https://www.facebook.com/{username}",
}

# Platforms where a 200 status is a strong signal vs. a weak one
RELIABLE_STATUS_CHECK = {
    "instagram": False,
    "facebook": False,
    "tiktok": True,
}


@dataclass
class SocialResult:
    platform: str
    username: str
    url: str
    exists: Optional[bool]   # True/False if confident, None if unknown/error
    reliable: bool


def check_username(
    username: str,
    platforms: Optional[List[str]] = None,
    timeout: int = 6,
) -> List[SocialResult]:
    """
    Checks `username` against each platform's public profile URL.
    Returns a list of SocialResult, one per platform checked.
    Never raises — network errors are captured as exists=None.
    """
    platforms = platforms or list(PLATFORM_URLS.keys())
    results = []

    for platform in platforms:
        if platform not in PLATFORM_URLS:
            continue

        url = PLATFORM_URLS[platform].format(username=username)
        reliable = RELIABLE_STATUS_CHECK.get(platform, False)

        try:
            resp = requests.get(
                url, headers=HEADERS, timeout=timeout, allow_redirects=True
            )
            if resp.status_code == 404:
                exists = False
            elif resp.status_code == 200:
                exists = True
            else:
                exists = None  # ambiguous (rate-limited, blocked, etc.)
        except requests.RequestException:
            exists = None

        results.append(
            SocialResult(
                platform=platform,
                username=username,
                url=url,
                exists=exists,
                reliable=reliable,
            )
        )

    return results
