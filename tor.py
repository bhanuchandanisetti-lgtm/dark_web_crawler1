"""
Tor connectivity check for Dark Web Monitoring System.
Verifies Tor access using configured SOCKS proxy.
"""

import requests
from config import TOR_PROXY

CHECK_URL = "https://check.torproject.org"
SUCCESS_MARKER = "Congratulations. This browser is configured to use Tor"


def get_proxy():
    """Return Tor SOCKS proxy from config."""
    return TOR_PROXY


def check_connection(proxy=None, timeout=20):
    """
    Verify Tor connectivity.
    Returns (success: bool, message: str).
    """
    proxy = proxy or get_proxy()
    try:
        r = requests.get(CHECK_URL, proxies=proxy, timeout=timeout)
        if SUCCESS_MARKER in r.text:
            return True, "Tor is working properly."
        return False, "Connected, but Tor confirmation message not found."
    except Exception as e:
        return False, f"Tor connection failed: {e}"


if __name__ == "__main__":
    ok, msg = check_connection()
    print("✅", msg) if ok else print("❌", msg)

