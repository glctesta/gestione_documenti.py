# -*- coding: utf-8 -*-
"""Test diretto future-flights endpoint."""
import urllib.request
import urllib.parse
import json

API_KEY = input("Inserisci FlightLabs API key: ").strip()

# Test /advanced-future-flights
url = f"https://www.goflightlabs.com/advanced-future-flights?access_key={API_KEY}&iataCode=TSR&type=arrival&date=2026-03-09"
print(f"\nURL: {url[:60]}...")
print(f"Key length: {len(API_KEY)} chars")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode('utf-8')
        print(f"✅ OK! Length: {len(raw)} chars")
        print(f"Content: {raw[:500]}")
except urllib.error.HTTPError as e:
    print(f"❌ HTTP {e.code}: {e.reason}")
    try:
        body = e.read().decode()
        print(f"Body: {body[:300]}")
    except: pass
except Exception as e:
    print(f"❌ Error: {e}")
