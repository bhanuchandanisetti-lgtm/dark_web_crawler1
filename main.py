"""
Crawl orchestration:
- Crawl darknet pages
- Run domain-aware threat detection
- Score findings
- Store results for dashboard & reporting
"""

import logging

from crawler import crawl
from detection import analyze_page
from scoring import compute_threat_score
from storage import init_db, save_finding
from config import MAX_PAGES_PER_SEED, LOG_FILE


import time
from config import MAX_PAGES_PER_SEED, LOG_FILE, CRAWL_INTERVAL_SECONDS

def run_crawl(seeds, organization, log_queue=None, stop_event=None):
    init_db()

    def log(msg):
        print(msg)
        if log_queue:
            log_queue.put(msg)
        if LOG_FILE:
            logging.info(msg)

    log(f"[+] Continuous monitoring started for domain: {organization}")

    while True:
        if stop_event and stop_event.is_set():
            log("[+] Monitoring stopped by user")
            break

        log("[+] Starting monitoring cycle")

        for seed in seeds:
            log(f"[+] Crawling seed: {seed}")
            pages = crawl(seed, max_pages=MAX_PAGES_PER_SEED)

            for page in pages:
                if stop_event and stop_event.is_set():
                    log("[+] Monitoring stopped during crawl")
                    return

                url = page["url"]
                text = page["text"]

                findings = analyze_page(text, url, organization)
                repetition_count = {}

                for f in findings:
                    key = (f["type"], url)
                    repetition_count[key] = repetition_count.get(key, 0) + 1

                    threat_score, risk_level = compute_threat_score(
                        f["type"],
                        repetition_rank=repetition_count[key]
                    )

                    save_finding(
                        source_url=f["source"],
                        finding_type=f["type"],
                        value=f["value"],
                        severity=f["severity"],
                        threat_score=threat_score,
                        risk_level=risk_level,
                        detected_at=f["timestamp"]
                    )

                    log(
                        f"[!] {f['type']} | {f['value']} | "
                        f"Score={threat_score} | Risk={risk_level}"
                    )

        log(f"[+] Monitoring cycle complete. Sleeping for {CRAWL_INTERVAL_SECONDS} seconds")

        # Sleep in small steps so Stop button works instantly
        slept = 0
        while slept < CRAWL_INTERVAL_SECONDS:
            if stop_event and stop_event.is_set():
                log("[+] Monitoring stopped during wait period")
                return
            time.sleep(5)
            slept += 5



def _setup_logging():
    if LOG_FILE:
        logging.basicConfig(
            filename=LOG_FILE,
            format="%(asctime)s %(message)s",
            level=logging.INFO,
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Dark Web Monitoring & Threat Intelligence System"
    )
    parser.add_argument(
        "--report",
        nargs="?",
        const="threat_intel_report.txt",
        metavar="PATH",
        help="Export text report and exit",
    )
    parser.add_argument(
        "--report-csv",
        nargs="?",
        const="threat_intel_report.csv",
        metavar="PATH",
        help="Export CSV report and exit",
    )
    parser.add_argument(
        "--check-tor",
        action="store_true",
        help="Verify Tor connectivity and exit",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Run web dashboard (default)",
    )
    args = parser.parse_args()

    if args.report is not None:
        from reporting import export_report
        path = export_report(args.report)
        print(f"Report written to: {path}")
        raise SystemExit(0)

    if args.report_csv is not None:
        from reporting import export_report_csv
        path = export_report_csv(args.report_csv)
        print(f"CSV report written to: {path}")
        raise SystemExit(0)

    if args.check_tor:
        from tor import check_connection
        ok, msg = check_connection()
        print("✅", msg) if ok else print("❌", msg)
        raise SystemExit(0 if ok else 1)

    _setup_logging()
    from gui import app
    print("\n  * Running on http://127.0.0.1:5000  (open in browser)\n")
    app.run(debug=True, host="127.0.0.1", port=5000)

