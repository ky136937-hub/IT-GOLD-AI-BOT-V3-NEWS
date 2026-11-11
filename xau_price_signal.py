#!/usr/bin/env python3
"""Telegram-only XAU/USD spot snapshot from XAUS. No trading or simulated prices."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

XAUS_URL = "https://xaus.com/api/v1/spot?compact=1"
TELEGRAM_API = "https://api.telegram.org"
CAMBODIA_TZ = ZoneInfo("Asia/Phnom_Penh")
MAX_FRESH_AGE_SECONDS = 180


def fetch_xau() -> dict:
    req = urllib.request.Request(
        XAUS_URL,
        headers={"User-Agent": "IT-TRADE-PRO/1.0", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
            http_status = response.status
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            payload = {}
        if exc.code == 503:
            return {"_http_status": 503, **payload}
        raise RuntimeError(f"XAUS HTTP {exc.code}: {body[:300]}") from exc

    if not isinstance(payload, dict):
        raise ValueError("XAUS returned an invalid JSON object")
    payload["_http_status"] = http_status
    return payload


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def make_message(payload: dict) -> str:
    now = datetime.now(timezone.utc)
    local_now = now.astimezone(CAMBODIA_TZ)
    state = payload.get("data_state") or {}
    status = str(state.get("status") or "").lower()
    updated = parse_iso(payload.get("updated_at"))
    as_of = parse_iso(state.get("as_of") or payload.get("price_as_of"))

    # Independently validate response age so an old cached response cannot be
    # labelled live just because its original data_state said "fresh".
    age = None
    if as_of:
        age = max(0, int((now - as_of).total_seconds()))
    if status == "fresh" and age is not None and age > MAX_FRESH_AGE_SECONDS:
        status = "stale"
    if status not in {"fresh", "stale", "unavailable"}:
        status = "unavailable"

    lines = [
        "🟡 IT TRADE PRO — XAU/USD",
        "📡 Data source: XAUS (Free / No API Key)",
        f"🕒 ម៉ោងកម្ពុជា: {local_now.strftime('%d-%m-%Y %H:%M:%S')} (UTC+7)",
    ]

    price = payload.get("spot_usd_oz")
    if status == "unavailable" or not isinstance(price, (int, float)) or price <= 0:
        lines.extend([
            "🔴 ស្ថានភាពទិន្នន័យ: UNAVAILABLE",
            "មិនមានតម្លៃ XAU/USD ពិតដែលអាចផ្ទៀងផ្ទាត់បានទេ។",
            "មិនបង្ហាញតម្លៃជំនួស និងមិនបង្កើតតម្លៃក្លែងក្លាយទេ។",
        ])
    else:
        label = "🟢 FRESH" if status == "fresh" else "🟠 STALE — តម្លៃចាស់"
        lines.extend([
            f"💰 XAU/USD: ${float(price):,.2f} / troy oz",
            f"📊 ស្ថានភាពទិន្នន័យ: {label}",
        ])
        if as_of:
            as_of_local = as_of.astimezone(CAMBODIA_TZ)
            lines.append(f"🗓️ តម្លៃនេះគិតត្រឹម: {as_of_local.strftime('%d-%m-%Y %H:%M:%S')} (ម៉ោងកម្ពុជា)")
        if age is not None:
            lines.append(f"⌛ អាយុទិន្នន័យ: {age} វិនាទី")
        if status == "stale":
            lines.append("⚠️ តម្លៃនេះជាទិន្នន័យចាស់ពី cache មិនមែនតម្លៃ Live ទេ។")

    lines.extend([
        "",
        "🔔 Telegram Signal Only — មិនបើក/បិទ Order ដោយស្វ័យប្រវត្តិ",
        "ℹ️ តម្លៃ XAUS ជា indicative spot reference មិនមែន tradable broker quote។",
        "Source: https://xaus.com/api/",
    ])
    return "\n".join(lines)


def send_telegram(token: str, chat_ids: list[str], message: str) -> None:
    for chat_id in chat_ids:
        body = json.dumps({"chat_id": chat_id, "text": message}).encode("utf-8")
        req = urllib.request.Request(
            f"{TELEGRAM_API}/bot{token}/sendMessage",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
        if not result.get("ok"):
            raise RuntimeError(f"Telegram API rejected message for chat ...{chat_id[-4:]}")


def main() -> int:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_ids = [v.strip() for v in os.getenv("TELEGRAM_CHAT_IDS", "").split(",") if v.strip()]
    if not token or not chat_ids:
        print("ERROR: Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_IDS in GitHub Actions Secrets.", file=sys.stderr)
        return 2

    payload = fetch_xau()
    message = make_message(payload)
    print(message)
    send_telegram(token, chat_ids, message)
    print(f"Telegram XAU/USD signal snapshot sent to {len(chat_ids)} configured chat(s).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
