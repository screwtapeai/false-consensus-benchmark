# False-Consensus Benchmark


When several agents agree, it is tempting to treat the agreement as proof. **False consensus** is the case where agents agree, or a majority agrees, and are still wrong. It is a general multi-agent problem. It can happen in any orchestration setup, whatever the framework or model provider. This repo is a small, reproducible test set for that problem, plus a harness that runs it against the public Screwtape API.


An independent judge for your agents. Screwtape is independent of your agent's own model and vendor, with no stake in your agent passing. Every verdict comes with a signed receipt you can verify yourself, which gives you a record you can trust when it matters.

## Contents
- `cases.jsonl`: 20 cases (16 consensus and 4 single-output judge cases). Each case has the exact task, per-agent outputs, expected truth, a verifiable source (a URL or the arithmetic), and its provenance. **All cases are constructed/synthetic.** The outputs are hand-written and none of them is a documented real-world incident.
- `harness.py`: Python, standard library only. Calls only `POST /v1/consensus`, `POST /v1/judge` and, optionally, `POST /v1/receipts/verify`.
- `results.jsonl`: raw responses with receipts, plus `RESULTS.md`, an honest per-case table that includes misses and false alarms.


## Run it
```bash
export SCREWTAPE_API_KEY=...   # free, 100 calls/day: https://screwtape.ai/signup/
python3 harness.py --verify
```
One run uses 21 calls.


## Use via MCP
Add the remote MCP server `https://screwtape.ai/mcp` to any MCP client. Its tools are `judge`, `consensus`, `get_api_key` and `buy_pack`.


## Verify a receipt
POST the raw `receipt` object to `https://screwtape.ai/v1/receipts/verify`. The public keys are at `https://screwtape.ai/.well-known/screwtape-receipt-keys.json` (Ed25519). The receipts saved in `results.jsonl` are unmodified (receipt schema 4 does not include any part of the API key), so you can verify any of them as-is, or verify a fresh receipt from your own run.


## License
Code: MIT (`LICENSE`). Data: CC-BY-4.0 (`LICENSE-DATA`).

