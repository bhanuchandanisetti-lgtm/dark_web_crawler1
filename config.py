"""
Configuration for Dark Web Monitoring & Threat Intelligence System.
Single source of truth for crawl limits, Tor routing, storage, and logging.
"""

# =======================
# Tor Configuration
# =======================
# 9050 → system tor service
# 9150 → Tor Browser
TOR_PROXY = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

REQUEST_TIMEOUT = 10


# Monitoring interval (seconds)
CRAWL_INTERVAL_SECONDS =  60   # 24 hours


# =======================
# Paths & Storage
# =======================
DB_NAME = "intel.db"
SEEDS_FILE = "seeds.txt"
LOG_FILE = "crawl.log"   # Set to None to disable file logging


# =======================
# Crawl Limits
# =======================
# Pages crawled per seed URL (controlled traversal)
MAX_PAGES_PER_SEED = 5


# =======================
# System Identity
# =======================
# Used in crawler User-Agent
PROJECT_NAME = "DarkWebMonitoringSDP"
PROJECT_VERSION = "1.0"


# =======================
# Dashboard / Reporting
# =======================
DEFAULT_ORDER_BY = "detected_at DESC"

