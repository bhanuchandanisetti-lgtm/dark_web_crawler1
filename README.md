# Dark Web Monitoring and Threat Intelligence System

Final-year B.Tech cybersecurity project: crawl .onion sites over Tor, detect data leaks and credential exposure, store findings locally, and generate reports for academic evaluation and viva.

---

## How to run the project

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Tor**  
   - Either run the **Tor service** (listening on port **9050**), or  
   - Run **Tor Browser** (uses port **9150** — then set `TOR_PROXY` in `config.py` to port 9150).

3. **Run the application**
   ```bash
   python main.py
   ```
   This starts the **web dashboard** at **http://127.0.0.1:5000**.  
   - Open that URL in a browser.  
   - Enter an organisation name/domain (e.g. `example.com`) and click **Run Crawl**.  
   - Seed URLs are read from `seeds.txt` (one .onion URL per line).

4. **Other ways to run**
   - **Check Tor**: `python main.py --check-tor`
   - **Export text report**: `python main.py --report` (creates `threat_intel_report.txt`)
   - **Export CSV report**: `python main.py --report-csv` (creates `threat_intel_report.csv`)
   - **Run GUI only** (same as step 3): `python main.py --gui` or `python gui.py`

---

## All features of the project

| Feature | Description |
|--------|-------------|
| **Tor-based crawling** | Fetches .onion pages over SOCKS5 proxy (configurable port 9050/9150). |
| **BFS crawl** | Starts from seed URLs in `seeds.txt`, follows .onion links only, up to a configurable page limit. |
| **Email leak detection** | Finds emails matching your organisation domain (e.g. *@example.com) and scores them by leak/credential/selling keywords (risk: LOW/MEDIUM/HIGH/CRITICAL). |
| **Organisation mention** | Records pages that mention the organisation name (context only). |
| **Threat keyword detection** | Flags pages containing configured keywords (leak, dump, password, breach, etc.). |
| **Local storage** | All findings saved in SQLite (`intel.db`): URL, type, value, confidence, risk, snippet, timestamp. |
| **Web dashboard** | Flask UI: view all findings, run a new crawl with an org name, see live crawl logs. |
| **Stop crawl** | “Stop Crawl” button on the live crawl page stops the crawl gracefully. |
| **Live log stream** | During a crawl, logs are streamed to the browser (Server-Sent Events). |
| **File logging** | Crawl activity is appended to `crawl.log` (configurable in `config.py`). |
| **Text report** | `python main.py --report` generates a human-readable report for project report and viva. |
| **CSV export** | `python main.py --report-csv` exports findings as CSV for analysis or screenshots. |
| **Tor check** | `python main.py --check-tor` verifies Tor connectivity before running a crawl. |
| **Config-driven** | All settings (proxy, paths, keywords, limits, log file) in `config.py`. |

## Prerequisites

- **Python 3.7+**
- **Tor**: Either Tor service (default port 9050) or Tor Browser (port 9150; update `config.py` if needed).
- **Dependencies**: `pip install -r requirements.txt`

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Tor** (system Tor service on 9050, or run Tor Browser for 9150).

3. **Run the application** (recommended entry point)
   ```bash
   python main.py
   ```
   Opens the web dashboard at http://127.0.0.1:5000

4. **Optional**
   - Check Tor: `python main.py --check-tor`
   - Export text report: `python main.py --report` or `python main.py --report my_report.txt`
   - Export CSV: `python main.py --report-csv` or `python main.py --report-csv findings.csv`

## Project structure

| Module       | Purpose |
|-------------|---------|
| `config.py` | Tor proxy, paths, keywords, limits |
| `crawler.py`| Fetch pages over Tor; extract text and links |
| `tor.py`    | Tor connectivity check; proxy from config |
| `detection.py` | Email leak detection and risk scoring |
| `storage.py`  | SQLite: save/list findings |
| `reporting.py`| Text and CSV report generation |
| `main.py`   | Crawl orchestration; **entry point** (GUI, --report, --check-tor) |
| `gui.py`    | Flask dashboard and live crawl UI |
| `logger.py` | Shared log queue and stop flag |

## Outputs for demo and viva

- **Dashboard**: Run a crawl from the web UI; use “Run Crawl” with an organisation name (e.g. domain or keyword). Findings appear on the home page.
- **Screenshots**: Dashboard table and live crawl page are suitable for report screenshots.
- **Report**: After a crawl, run `python main.py --report` to generate `threat_intel_report.txt` for the project report.
- **Log**: Crawl activity is appended to `crawl.log` when `config.LOG_FILE` is set (default: `crawl.log`).

## Configuration

Edit `config.py` to change:

- `TOR_PROXY`: Port 9050 (Tor service) or 9150 (Tor Browser).
- `SEEDS_FILE`: Path to seed URLs (one .onion URL per line).
- `MAX_PAGES_PER_SEED`: Global page cap per crawl (default 50).
- `LOG_FILE`: Log file path, or `None` to disable file logging.

## Licence

Academic project use.
