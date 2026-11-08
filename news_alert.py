#!/usr/bin/env python3
"""Scheduled USD economic-news alert for IT GOLD AI BOT V3.

Runs as a short-lived GitHub Actions job. It does not need a laptop or MT5.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

API_URL = "https://showmytrades.com/api/public/calendar/v1"
TELEGRAM_API = "https://api.telegram.org"
CAMBODIA_TZ = ZoneInfo("Asia/Phnom_Penh")
ALERT_WINDOW_SECONDS = 15 * 60


def fetch_calendar() -> tuple[list[dict], int]:
    params = urllib.parse.urlencode({
        "currency": "USD",
        "impact": "high,medium",
        "days": "7",
        "format": "json",
    })
    request = urllib.request.Request(
        f"{API_URL}?{params}",
        headers={"User-Agent": "IT-GOLD-AI-BOT-V3/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        payload = json.loads(response.read().decode("utf-8"))

    events = payload.get("events", [])
    if not isinstance(events, list):
        raise ValueError("Economic calendar response has no valid 'events' list")

    server_time = payload.get("server_time")
    if not isinstance(server_time, (int, float)):
        # Fallback to UTC system clock if provider omits server_time.
        server_time = datetime.now(timezone.utc).timestamp()
    return events, int(server_time)


def format_event(event: dict) -> str:
    ts = int(event.get("ts", 0))
    if ts:
        local_time = datetime.fromtimestamp(ts, timezone.utc).astimezone(CAMBODIA_TZ)
        time_text = local_time.strftime("%d-%m-%Y %H:%M")
    else:
        time_text = str(event.get("time", "Unknown time"))

    impact = str(event.get("impact", "unknown")).upper()
    icon = "🔴" if impact == "HIGH" else "🟠" if impact == "MEDIUM" else "⚪"
    title = str(event.get("title", "USD economic event"))
    forecast = str(event.get("forecast") or "—")
    previous = str(event.get("previous") or "—")
    actual = str(event.get("actual") or "—")
    status = str(event.get("status") or "scheduled")
    confidence = str(event.get("confidence") or "")

    lines = [
        f"{icon} {impact} IMPACT — USD",
        f"📰 {title}",
        f"⏰ ម៉ោងកម្ពុជា: {time_text}",
        f"Forecast: {forecast} | Previous: {previous} | Actual: {actual}",
    ]
    if status != "scheduled" or confidence == "tentative":
        lines.append(f"⚠️ Status: {status}" + (" / tentative" if confidence == "tentative" else ""))
    return "\n".join(lines)


def telegram_send(token: str, chat_id: str, message: str) -> None:
    url = f"{TELEGRAM_API}/bot{token}/sendMessage"
    body = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(request, timeout=25) as response:
        result = json.loads(response.read().decode("utf-8"))
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error: {result}")


def main() -> int:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_ids = [x.strip() for x in os.getenv("TELEGRAM_CHAT_IDS", "").split(",") if x.strip()]
    mode = os.getenv("NEWS_MODE", "alert").strip().lower()

    if not token or not chat_ids:
        print("ERROR: Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_IDS in GitHub Actions Secrets.", file=sys.stderr)
        return 2

    events, server_time = fetch_calendar()
    now_utc = datetime.fromtimestamp(server_time, timezone.utc)
    print(f"Calendar connected. Events returned: {len(events)}. Server UTC: {now_utc.isoformat()}")

    valid_events = []
    for event in events:
        if str(event.get("currency", "")).upper() != "USD":
            continue
        if str(event.get("impact", "")).lower() not in {"high", "medium"}:
            continue
        try:
            event_ts = int(event.get("ts", 0))
        except (TypeError, ValueError):
            continue
        if event_ts <= 0:
            continue
        delta = event_ts - server_time
        if mode == "digest":
            if 0 <= delta <= 24 * 60 * 60:
                valid_events.append(event)
        else:
            # One 15-minute forward window per scheduled run. This avoids
            # repeatedly alerting for the same event under normal scheduling.
            if 0 <= delta < ALERT_WINDOW_SECONDS:
                valid_events.append(event)

    valid_events.sort(key=lambda item: int(item.get("ts", 0)))

    if mode != "digest" and not valid_events:
        print("No high/medium-impact USD event in the next 15 minutes; no Telegram alert sent.")
        return 0

    if not valid_events:
        message = (
            "🟡 IT GOLD AI BOT V3 — USD NEWS\n\n"
            "🟢 Economic Calendar: Connected\n"
            "មិនមានព័ត៌មាន USD កម្រិត Medium/High ក្នុង 24 ម៉ោងខាងមុខទេ។\n\n"
            "Source: ShowMyTrades Economic Calendar"
        )
    else:
        heading = "🟡 IT GOLD AI BOT V3 — USD NEWS DIGEST" if mode == "digest" else "🚨 IT GOLD AI BOT V3 — USD NEWS ALERT"
        lead = "ព័ត៌មាន USD ក្នុង 24 ម៉ោងខាងមុខ៖" if mode == "digest" else "មានព័ត៌មាន USD នឹងចេញក្នុង 15 នាទីខាងមុខ៖"
        message = heading + "\n\n🟢 Economic Calendar: Connected\n" + lead + "\n\n"
        message += "\n\n──────────────\n\n".join(format_event(event) for event in valid_events[:15])
        message += "\n\nSource: https://showmytrades.com/tools/economic-calendar"

    for chat_id in chat_ids:
        telegram_send(token, chat_id, message)
        print(f"Telegram message sent to configured chat ending ...{chat_id[-4:]}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
