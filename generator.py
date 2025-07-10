"""
generator.py
Core helpers for the Password‑Smith project
"""

import secrets, string, hashlib, requests
from zxcvbn import zxcvbn

# private constant for symbols
_SYMBOLS = "!@#$%^&*()_+-=[]{};:,.?"

def generate_password(length: int = 16,
                      *,
                      digits: bool = True,
                      symbols: bool = True,
                      uppercase: bool = True,
                      lowercase: bool = True) -> str:
    """Return a cryptographically‑secure random password."""
    pools: list[str] = []
    if digits:    pools.append(string.digits)
    if symbols:   pools.append(_SYMBOLS)
    if uppercase: pools.append(string.ascii_uppercase)
    if lowercase: pools.append(string.ascii_lowercase)
    if not pools:
        raise ValueError("No character sets selected")

    all_chars = "".join(pools)

    # guarantee ≥1 char from each chosen set
    pw_chars = [secrets.choice(pool) for pool in pools]
    pw_chars += [secrets.choice(all_chars) for _ in range(length - len(pools))]
    secrets.SystemRandom().shuffle(pw_chars)
    return "".join(pw_chars)


def score_password(pwd: str) -> dict:
    """Return the full zxcvbn analysis dictionary (score 0‑4)."""
    return zxcvbn(pwd)


def hibp_pwned(pwd: str) -> int:
    """
    Return the number of times *pwd* appears in Have‑I‑Been‑Pwned.
    0 means not found.
    """
    sha1 = hashlib.sha1(pwd.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    for line in resp.text.splitlines():
        suf, count = line.split(":")
        if suf == suffix:
            return int(count)
    return 0
