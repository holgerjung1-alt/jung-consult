#!/usr/bin/env python3
"""Build the public vehicle feed from Pages CMS vehicle files."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / "daten" / "fahrzeuge"
target = root / "fahrzeuge.json"
vehicles = []
files = sorted(p for p in source.iterdir() if p.is_file() and p.suffix.lower() in {".json", ".md"}) if source.exists() else []
if not files:
    raise SystemExit("No Pages CMS vehicle files found; refusing to overwrite existing feed")
for path in files:
    raw = path.read_text(encoding="utf-8-sig").strip()
    try:
        vehicle = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid vehicle JSON in {path}: {exc}")
    if not isinstance(vehicle, dict):
        raise SystemExit(f"Vehicle entry must be an object: {path}")
    if vehicle.get("veroeffentlicht") is not True:
        continue
    vehicle["id"] = path.stem
    vehicles.append(vehicle)
target.write_text(json.dumps(vehicles, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Built {target.name} with {len(vehicles)} published vehicles from {len(files)} CMS files")
