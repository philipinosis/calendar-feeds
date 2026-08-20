# calendar-feeds

Public iCal (`.ics`) subscription feeds for personal calendars.

Currently one feed: `cannery.ics` — Might Could Cannery LLC formation, grant, and
QSBS deadlines, for subscription in Apple Calendar.

## Status / how it's served

Published from GitHub repo `philipinosis/calendar-feeds` (branch `main`). No build
step, no Pages — clients fetch the file directly over GitHub's raw content URL.
Apple Calendar re-polls hourly (`REFRESH-INTERVAL:PT1H` in the feed).

## Structure

- `build_ics.py` — generator. Hard-coded `EVENTS` list → writes `cannery.ics`. Self-contained, no deps.
- `cannery.ics` — generated feed. Subscribe to this; do not hand-edit.
- `README.md` — this file.

## Subscribe (Apple Calendar)

Feed URL:
```
https://raw.githubusercontent.com/philipinosis/calendar-feeds/main/cannery.ics
```

- **Mac:** Calendar → File → New Calendar Subscription → paste URL → Subscribe → refresh "Every hour".
- **iPhone:** Settings → Calendar → Accounts → Add Account → Other → Add Subscribed Calendar → paste URL.

## Update a feed

1. Edit the `EVENTS` list in `build_ics.py` (tuple: uid_slug, summary, ISO date, description, url, categories, priority, alarms).
2. `python3 build_ics.py` — regenerates `cannery.ics`. Events older than yesterday are dropped automatically.
3. Commit and push `cannery.ics` to `main`. Subscribers pick it up on the next hourly poll.
