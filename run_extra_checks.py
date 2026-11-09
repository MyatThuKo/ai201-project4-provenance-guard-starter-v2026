#!/usr/bin/env python3
"""
The checks run_eval.py can't express.  <- UNIT 8, MILESTONE 3

    python app.py                                  # in one terminal
    python run_extra_checks.py --label before      # in another

run_eval.py only sends valid JSON to /submit, so two of my criteria need more:

    Criterion 4  submit, appeal the content_id that came back, then read
                 /log to confirm the appeal was recorded and the item is
                 under_review. Plus one appeal against an id that doesn't exist.

    Criterion 5  all seven bad inputs, including case 7 (unparseable JSON),
                 with GET /health checked after each one.

Three trials, like run_eval.py. Writes results/extra_checks_<stamp>_<label>.md.
"""

import argparse
import datetime as dt
import json
import sys
import uuid

import config

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

APPEAL_TEXT = (
    "I wrote this paragraph for a class assignment. I drafted it twice and "
    "changed the ending after my friend read it. It is short, but it is mine."
)

# Criterion 5, cases 1–7 from criteria.md: (name, expected status, how to send).
# "json" is sent as a JSON body; "raw" is sent as-is with a JSON content type.
BAD_INPUTS = [
    ("missing text", 400, "json", {"creator_id": "extra_bad_missing_text"}),
    ("empty text", 400, "json", {"text": "", "creator_id": "extra_bad_empty"}),
    ("missing creator_id", 400, "json", {"text": "A perfectly ordinary sentence."}),
    ("numeric text", 400, "json", {"text": 12345, "creator_id": "extra_bad_number"}),
    ("text over 10,000 chars", 413, "json", {"text": "word " * 2001, "creator_id": "extra_bad_huge"}),
    ("whitespace-only text", 400, "json", {"text": "   \n\t  ", "creator_id": "extra_bad_space"}),
    ("unparseable JSON", 400, "raw", '{"text": "unfinished'),
]


def check_appeals(requests, url, trial):
    """Criterion 4: five real appeals and one against a made-up id."""
    results = []

    for i in range(1, 6):
        creator = f"extra_appeal_t{trial}_{i}"
        submitted = requests.post(f"{url}/submit",
                                  json={"text": APPEAL_TEXT, "creator_id": creator},
                                  timeout=90)
        content_id = submitted.json().get("content_id")

        appealed = requests.post(f"{url}/appeal",
                                 json={"content_id": content_id,
                                       "reasoning": "I wrote this myself."},
                                 timeout=30)
        body = appealed.json()

        entries = [e for e in requests.get(f"{url}/log", timeout=30).json()["entries"]
                   if e.get("content_id") == content_id]
        appeal_logged = any(e.get("event") == "appeal" for e in entries)
        latest_status = entries[-1].get("status") if entries else None

        passed = (appealed.status_code == 200
                  and body.get("status") == "under_review"
                  and appeal_logged
                  and latest_status == "under_review")
        results.append({
            "check": f"appeal {i}",
            "content_id": content_id,
            "appeal_status_code": appealed.status_code,
            "response_status": body.get("status"),
            "appeal_in_log": appeal_logged,
            "latest_status_in_log": latest_status,
            "passed": passed,
        })

    fake_id = str(uuid.uuid4())
    appealed = requests.post(f"{url}/appeal",
                             json={"content_id": fake_id, "reasoning": "Test."},
                             timeout=30)
    logged = any(e.get("content_id") == fake_id
                 for e in requests.get(f"{url}/log", timeout=30).json()["entries"])
    results.append({
        "check": "nonexistent content_id",
        "content_id": fake_id,
        "appeal_status_code": appealed.status_code,
        "appeal_in_log": logged,
        "passed": appealed.status_code == 404 and not logged,
    })
    return results


def check_bad_inputs(requests, url):
    """Criterion 5: expected status, a JSON error body, and /health still 200."""
    results = []
    for name, expected, how, body in BAD_INPUTS:
        if how == "json":
            response = requests.post(f"{url}/submit", json=body, timeout=30)
        else:
            response = requests.post(f"{url}/submit", data=body, timeout=30,
                                     headers={"Content-Type": "application/json"})
        try:
            error = response.json().get("error")
        except ValueError:
            error = None
        health = requests.get(f"{url}/health", timeout=10).status_code

        results.append({
            "check": name,
            "expected": expected,
            "status": response.status_code,
            "json_error": error,
            "health_after": health,
            "passed": response.status_code == expected and bool(error) and health == 200,
        })
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    trials = []
    for trial in range(1, args.trials + 1):
        appeals = check_appeals(requests, args.url, trial)
        bad = check_bad_inputs(requests, args.url)
        trials.append({"appeals": appeals, "bad_input": bad})
        print(f"trial {trial}: criterion 4 {sum(r['passed'] for r in appeals)}/{len(appeals)}"
              f" · criterion 5 {sum(r['passed'] for r in bad)}/{len(bad)}")

    write_report(trials, args)


def write_report(trials, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"extra_checks_{stamp}{label}.md"

    def score(key, t):
        return f"{sum(r['passed'] for r in t[key])}/{len(t[key])}"

    n = len(trials)
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    lines = [
        f"# Extra checks{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_extra_checks.py::main`",
        "- Service: `app.py::submit`, `app.py::appeal`, `app.py::get_log`, `app.py::health`",
        f"- {n} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"| Criterion | Target | {headers} |",
        f"|---|---|{'|'.join(['---'] * n)}|",
        f"| 4. Appeal reliability | 6 of 6 | {' | '.join(score('appeals', t) for t in trials)} |",
        f"| 5. Bad input handling | 7 of 7 | {' | '.join(score('bad_input', t) for t in trials)} |",
        "",
        "---",
        "",
        "## What actually came back",
        "",
    ]
    for number, t in enumerate(trials, 1):
        lines += [f"**Trial {number}**", "", "```json", json.dumps(t, indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
