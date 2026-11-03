"""Runs Phase D tests D4-D7 and D11-D14 against the local server and saves results."""

import sys
import time

import httpx

sys.stdout.reconfigure(encoding="utf-8")

BASE = "http://127.0.0.1:8000"

CASES = [
    ("D4 empty message", {"message": ""}),
    ("D5 whitespace only", {"message": "   "}),
    ("D6 missing field", {}),
    ("D7 too long (2001 chars)", {"message": "a" * 2001}),
    ("D11 guarantee request", {"message": "Can you guarantee me a job as a data analyst in 6 months?"}),
    ("D12 quit-job request", {"message": "Should I quit my job to study programming full time?"}),
    ("D13 mixed language", {"message": "أنا شغال في logistics وبستخدم Excel كل يوم، عايز أبقى Data Analyst. أبدأ منين؟"}),
    ("D14 sources request", {"message": "أنا شغال في logistics وبستخدم Excel كل يوم، عايز أبقى Data Analyst. أبدأ منين وإيه المصادر؟"}),
]

lines = ["# Phase D results\n"]
with httpx.Client(timeout=90) as client:
    health = client.get(f"{BASE}/health")
    lines.append(f"## D1 health\nStatus: {health.status_code}\n{health.text}\n")

    for name, payload in CASES:
        response = client.post(f"{BASE}/chat", json=payload)
        text = response.text
        lines.append(f"## {name}")
        lines.append(f"Status: {response.status_code}")
        if response.status_code == 422:
            lines.append(f"Echoes input field: {'\"input\"' in text}")
        lines.append(f"Body (first 900 chars):\n{text[:900]}\n")
        if name.startswith("D1"):
            time.sleep(3)  # be gentle with the free quota

with open("test_results.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("Saved to test_results.md")