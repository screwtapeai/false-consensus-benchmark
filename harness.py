#!/usr/bin/env python3
"""False-Consensus benchmark harness. Stdlib only. Calls only the public Screwtape API.
Usage: SCREWTAPE_API_KEY=... python3 harness.py [--verify]"""
import json, os, sys, time, urllib.request, urllib.error
BASE = "https://screwtape.ai"
KEY = os.environ.get("SCREWTAPE_API_KEY")
if not KEY: sys.exit("set SCREWTAPE_API_KEY (free key: https://screwtape.ai/signup/)")

def post(path, body, auth=True):
    h = {"Content-Type": "application/json", "User-Agent": "screwtape-fc-bench/0.1"}
    if auth: h["Authorization"] = "Bearer " + KEY
    req = urllib.request.Request(BASE + path, json.dumps(body).encode(), h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as r: return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read())
        except Exception: return e.code, {"error": "non-json"}

def redact(o):
    """Receipt schema 4 and later never contain key_prefix, so they are saved unchanged and still verify.
    Older receipts (schema 3 or earlier) get payment.key_prefix replaced; those no longer verify."""
    if isinstance(o, dict):
        if o.get("schema_version", 4) >= 4 and "signature" in o: return o
        return {k: ("[redacted]" if k == "key_prefix" else redact(v)) for k, v in o.items()}
    if isinstance(o, list): return [redact(x) for x in o]
    return o

def main():
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "results"), exist_ok=True)
    out = []
    for line in open(os.path.join(here, "cases.jsonl")):
        c = json.loads(line)
        if c["type"] == "consensus":
            st, r = post("/v1/consensus", {"task": c["task"], "answers": c["answers"]})
        else:
            st, r = post("/v1/judge", {"task": c["task"], "agent_output": c["agent_output"]})
        out.append({"id": c["id"], "type": c["type"], "category": c["category"], "expected_flag": c["expected_flag"], "http_status": st, "response": r})
        print(c["id"], st, file=sys.stderr); time.sleep(1)
    if "--verify" in sys.argv:
        rc = next((o["response"].get("receipt") for o in out if isinstance(o["response"], dict) and o["response"].get("receipt")), None)
        if rc:
            st, v = post("/v1/receipts/verify", rc)  # raw receipt object as the body
            out.append({"id": "receipt-verify", "http_status": st, "response": v})
    with open(os.path.join(here, "results", "results.jsonl"), "w") as f:
        for o in out: f.write(json.dumps(redact(o)) + "\n")

if __name__ == "__main__": main()
