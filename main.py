#Akash Lakshmanan
#Date: May 22, 2026
#Data Engineer Intern Challenge - Super.com


import json
from datetime import datetime
from collections import defaultdict

#Task 1 (Validate Timestamps)
def read_timestamp(time_str):
  """
  Parse timestamp string, and returns datetime if valid, else nothing
  """
  try:
    #Attempting to convert to datetime object
    return datetime.fromisoformat(time_str.replace("Z", "+00:00"))
  except (ValueError, AttributeError):
    return None
  
def load_and_validate(path="events.json"):
  """
  Loads events.json, skips malformed timestamps, and logs each skip
  """
  #reading input file
  with open(path) as infile:
    raw = json.load(infile)

  valid = []
  for i, event in enumerate (raw, start = 1):
    time_s = read_timestamp(event.get("event_time", ""))
    if time_s is None:
      print(f"[SKIP] Line {i}: invalid timestamp '{event.get('event_time')}'")
    else:
      valid.append({
        "user_id": event["user_id"],
        "event_time": time_s,
        "event_type": event["event_type"],
      })
  return valid
      
#Task 2 (De-duplicate)

def check_duplicate(events):
  """
  Drop events where all three fields are identical
  """
  #Getting this composite identifier, which identifies a unique event
  #Keeping only first occurance
  seen = set()
  result = []
  for ev in events:
    identifier = (ev["user_id"], ev["event_time"], ev["event_type"])
    if identifier not in seen:
      seen.add(identifier)
      result.append(ev)
  return result

#Task 3 (Transform to User Sessions)
def build_session(events):
  """
  Returns list of {user_id, session_start, session_end, event_count}
  """
  buckets = defaultdict(list)
  for ev in events:
    buckets[ev["user_id"]].append(ev["event_time"])

  sessions = []
  for uid in sorted(buckets):
    times = buckets[uid]
    sessions.append({
      "user_id": uid,
      "session_start": min(times).isoformat(),
      "session_end": max(times).isoformat(),
      "event_count": len(times)
    })
  return sessions

def main():
  #Task 1
  valid = load_and_validate("events.json")
  print(f"\nValid events after timestamp check : {len(valid)}")

  #Task 2
  deduped = check_duplicate(valid)
  print(f"Events after de-duplication  : {len(deduped)}  "
        f"({len(valid) - len(deduped)} duplicate(s) dropped)\n")
  
  #Task 3
  sessions = build_session(deduped)
  print(f"{'user_id':<10} {'session_start':<32} {'session_end':<32} {'event_count'}")
  print("-" * 85)
  for s in sessions:
    print(f"{s['user_id']:<10} {s['session_start']:<32} {s['session_end']:<32} {s['event_count']}")
  #Session_summary.json is just an addition (not shown in coderbyte due to restrictions)
  #However, the json is shown in private Github repo
  with open("session_summaries.json", "w") as f:
    json.dump(sessions, f, indent = 2)
  print("\nOutput written to session_summaries.json")

if __name__ == "__main__":
  main()