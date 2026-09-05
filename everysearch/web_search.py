"""
web_search.py

Checks whether a given username exists on popular social platforms
by requesting their public profile URL and inspecting the response.

Reliability notes:
- Status codes alone are NOT trustworthy — platforms often return 200
  even for "not found" pages (soft 404s) or CAPTCHA/block pages.
- This version checks page content for known "not found" markers.
- Instagram / Facebook remain the least reliable since their real
  profile data loads via JS behind a login wall.
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

# Phrases that indicate the profile does NOT exist, even on a 200 response.
NOT_FOUND_MARKERS = {
    "instagram": [
        "Sorry, this page isn't available",
        "page not found",
    ],
    "tiktok": [
        "Couldn't find this account",
        "user-not-found",
        "page-not-found",
    ],
    "facebook": [
        "This content isn't available",
        "page not found",
        "isn't available right now",
    ],
}

# Platforms where we have any real confidence at all.
# Instagram/Facebook stay unreliable regardless of this check,
# because logged-out pages are mostly JS-rendered shells.
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
    exists: Optional[bool]   # True/False if confident, None if unknown
    reliable: bool


def _looks_missing(platform: str, page_text: str) -> bool:
    markers = NOT_FOUND_MARKERS.get(platform, [])
    lowered = page_text.lower()
    return any(marker.lower() in lowered for marker in markers)


def check_username(
    username: str,
    platforms: Optional[List[str]] = None,
    timeout: int = 6,
) -> List[SocialResult]:
    platforms = platforms or list(PLATFORM_URLS.keys())
    results = []

    for platform in platforms:
        if platform not in PLATFORM_URLS:
            continue

        url = PLATFORM_URLS[platform].format(username=username)
        reliable = RELIABLE_STATUS_CHECK.get(platform, False)
        exists: Optional[bool] = None

        try:
            resp = requests.get(
                url, headers=HEADERS, timeout=timeout, allow_redirects=True
            )

            if resp.status_code == 404:
                exists = False
            elif resp.status_code == 200:
                # Don't trust the 200 blindly — check content
                if _looks_missing(platform, resp.text):
                    exists = False
                else:
                    # Page loaded and didn't show a "not found" marker.
                    # For unreliable platforms, this is still a guess.
                    exists = True
            else:
                exists = None  # rate-limited, blocked, redirected weirdly, etc.

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
