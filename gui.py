from queue import Empty
import threading

from flask import Flask, render_template, request, redirect, url_for, Response

from config import SEEDS_FILE
from main import run_crawl
from storage import init_db, get_findings, get_summary_by_type, get_risk_overview
from logger import log_queue, stop_event

init_db()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    findings = get_findings()
    summary_by_type = get_summary_by_type()
    risk_overview = get_risk_overview()

    return render_template(
        "index.html",
        findings=findings,
        summary_by_type=summary_by_type,
        risk_overview=risk_overview
    )


@app.route("/stream")
def stream():
    def event_stream():
        while True:
            try:
                msg = log_queue.get(timeout=1)
                yield f"data: {msg}\n\n"
            except Empty:
                yield ": keepalive\n\n"

    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/run", methods=["POST"])
def run():
    organization = request.form.get("org")
    stop_event.clear()

    with open(SEEDS_FILE) as f:
        seeds = [line.strip() for line in f if line.strip()]

    t = threading.Thread(
        target=run_crawl,
        args=(seeds, organization, log_queue),
        kwargs={"stop_event": stop_event},
        daemon=True
    )
    t.start()

    return render_template("crawl_live.html", organization=organization)


@app.route("/stop", methods=["POST"])
def stop():
    stop_event.set()
    return redirect(url_for("index"))


@app.route("/logs")
def logs():
    logs = []
    while not log_queue.empty():
        logs.append(log_queue.get())
    return {"logs": logs}


if __name__ == "__main__":
    from main import _setup_logging
    _setup_logging()
    app.run(debug=True, host="127.0.0.1", port=5000)

