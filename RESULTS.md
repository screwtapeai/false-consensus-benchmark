# Results: run of 2026-10-22 (12:45 UTC-3)

One run, 20 cases plus 1 receipt verification (21 calls on the free tier, $0), against the Screwtape API as of 2026-10-22. Raw responses with signed receipts are in `results.jsonl`.

**Scoring rule:** a consensus case counts as flagged when `false_consensus_risk` is `high` or `medium`. A judge case counts as flagged when `verdict` is not `pass`. Split cases (FC-10 to FC-12) are expected `no flag`: agents disagree but the top answer returned is correct, so low risk with the correct `consensus_answer` is the intended behaviour and scores as a correct pass. Low risk with a wrong answer would be a miss.

**Totals:** 11 caught, 0 missed, 2 false alarms, 7 correct passes (20 cases).

| id | category | expected | Screwtape output | result |
|---|---|---|---|---|
| FC-01 | unanimous_wrong | flag | risk=high, verification=failed, answer=Sydney | caught |
| FC-02 | unanimous_wrong | flag | risk=high, verification=failed, answer=Toronto | caught |
| FC-03 | unanimous_wrong | flag | risk=high, verification=failed, answer=One heart | caught |
| FC-04 | unanimous_wrong | flag | risk=high, verification=failed, answer=418 | caught |
| FC-05 | unanimous_wrong | flag | risk=high, verification=failed, answer=Yes, trailing commas are allowed in JSON arrays | caught |
| FC-06 | unanimous_wrong | flag | risk=high, verification=failed, answer=503 | caught |
| FC-07 | majority_wrong_lone_dissenter | flag | risk=high, verification=failed, answer=In July, during northern summer. | caught |
| FC-08 | majority_wrong_lone_dissenter | flag | risk=high, verification=failed, answer=So | caught |
| FC-09 | majority_wrong_lone_dissenter | flag | risk=high, verification=failed, answer=64 bits | caught |
| FC-10 | split | no flag | risk=low, verification=judged, answer=212 F | correct pass |
| FC-11 | split | no flag | risk=low, verification=judged, answer=1969 | correct pass |
| FC-12 | split | no flag | risk=low, verification=judged, answer=12 | correct pass |
| FC-13 | correct_control | no flag | risk=low, verification=judged, answer=Paris | correct pass |
| FC-14 | correct_control | no flag | risk=low, verification=verified, answer=63 | correct pass |
| FC-15 | correct_control | no flag | risk=low, verification=judged, answer=H2O | correct pass |
| FC-16 | correct_control | no flag | risk=low, verification=judged, answer=404 | correct pass |
| FJ-17 | judge_single_output | flag | verdict=fail, score=0 | caught |
| FJ-18 | judge_single_output | flag | verdict=fail, score=0 | caught |
| FJ-19 | judge_single_output | no flag | verdict=fail, score=0 | false alarm |
| FJ-20 | judge_single_output | no flag | verdict=fail, score=0 | false alarm |

## Notes (read these before quoting any number)
- **Consensus cases:** in this run every unanimous-wrong and majority-wrong case (FC-01 to FC-09) was flagged high, with `verification` = `failed`. That includes FC-04 (17x24 = 418; correct product 408) and FC-07 (perihelion in July; it is early January).
- **Reasons on failed verification:** when the agreed answer fails verification, the first reason states the finding (for example FC-04: "Agreed answer 418 is wrong: 17×24 = 408."). In this run no reason on a flagged case called the answer correct.
- **FC-07:** in this run the model response was not usable, so this case was scored by the deterministic fallback (`engine` = `deterministic`). It was still flagged high.
- **FC-15 and FC-16:** correct unanimous answers with identical wording returned low risk ("Identical wording did not raise the risk because the agreed answer verified.").
- **FC-10, FC-11 and FC-12 (split):** labelled `no flag`. The sets show disagreement, not false consensus, and Screwtape returned low risk with the correct answer each time.
- **FJ-19 and FJ-20:** false alarms. No `evidence` field was supplied in these `/v1/judge` calls, and the judge failed correct answers ("No evidence provided to support the claim" / "Claim not supported by provided evidence"). A run with evidence would test something different.
- **Receipts:** every receipt in `results.jsonl` is receipt schema 4, which does not include the API key prefix, so the receipts are published unchanged. On 2026-10-22 all 20 saved receipts were POSTed from `results.jsonl` to `/v1/receipts/verify` and each returned `{"valid": true}`.
- **Earlier draft run** (2026-10-22 10:51 UTC-3, older engine): 9 caught, 2 missed, 4 false alarms, 5 correct passes under the same labels.
