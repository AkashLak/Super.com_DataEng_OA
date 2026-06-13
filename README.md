✅ Submission approved by Super.com

# Data Engineer Intern Challenge - Super.com

Goal: Validate, de-duplicate, and summarize user events from a JSON file.

## Usage

```bash
python3 main.py
```

Expects `events.json` in the working directory. Logs pipeline steps to terminal 
and writes final session summaries to `session_summaries.json`.

## What It Does

| Step | Description |
|------|-------------|
| 1. Validate | Parses each `event_time` as ISO-8601. Skips and logs malformed rows with line number and reason |
| 2. De-duplicate | Drops exact duplicate events where all three fields (`user_id`, `event_time`, `event_type`) match |
| 3. Summarize | Computes per-user `session_start`, `session_end`, and `event_count` from clean events |

## Output Format (session_summaries.json)

```json
[
  {
    "user_id": 10,
    "session_start": "2024-07-10T12:00:05+00:00",
    "session_end":   "2024-07-11T09:30:00+00:00",
    "event_count":   7
  }
]
```

## Data Quality Proposals - Akash Lakshmanan

1) **Schema Drift validation**: Making sure required keys (`user_id: int`, 
`event_type:str`, `event_time: str`) exist with correct types on every row 
before processing. Also rejecting malformed records immediately.

2) **Timestamp Range Check**: Flagging events whose `event_time` falls outside
a plausible window (Ex: more than 1 year in the past or any future timestamp)
as suspicious. Can log this separately from fully invalid rows.

3) **Event-type allowlist**: Validate `event_type` against a known enum `{view, click, 
purchase}`. Unrecognized values indicate upstream schema drift and should
trigger an alert (faster detection, and more accurate).

4) **Duplicate-rate monitoring**: Track the duplicate drop ratio per pipeline
run, as a sudden spike signals upstream double-publishing, pipeline replay bugs, 
or misconfigured producers.

5) **User anomaly detection**: Flag users whose `event_count` exceeds 3-3.5 standard deviations above the population mean, as this can potentially indicate bot traffic/data injection

6) **Ordering Sanity Check**: After deduplication, make sure each user's events
are monotonically increasing when sorted by `event_time`, as out-of-order events
suggest clock/time errors or multi-source merging issues.
