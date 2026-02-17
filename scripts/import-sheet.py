#!/usr/bin/env python3
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def normalize_key(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").strip().lower())


def slugify(text: str) -> str:
    t = (text or "").lower().strip()
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    t = re.sub(r"[\s_-]+", "-", t)
    return t.strip("-") or "profile"


def boolish(value: str) -> bool:
    v = (value or "").strip().lower()
    return v in {"yes", "y", "true", "1", "checked"} or (v and v not in {"no", "n", "false", "0"})


def parse_year(value: str):
    if not value:
        return None
    m = re.search(r"(19|20)\d{2}", value)
    return int(m.group(0)) if m else None


def load_json_list(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json_list(path: Path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def next_id(prefix: str, items):
    nums = []
    for it in items:
        m = re.search(rf"^{re.escape(prefix)}-(\d+)$", str(it.get("id", "")))
        if m:
            nums.append(int(m.group(1)))
    n = (max(nums) + 1) if nums else 1
    return f"{prefix}-{n:03d}"


def index_rows(csv_path: Path):
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        keymap = {normalize_key(h): h for h in headers}
        rows = list(reader)
    return keymap, rows


def get(row, keymap, *keys):
    for k in keys:
        h = keymap.get(normalize_key(k))
        if h and row.get(h) is not None:
            return row.get(h, "").strip()
    return ""


def build_base_profile(row, keymap, category):
    full_name = get(row, keymap, "Full Name", "Name")
    display = get(row, keymap, "Preferred Display Name (optional)", "Preferred Display Name")
    name = display or full_name

    profile_url = get(row, keymap, "LinkedIn or Personal Website", "LinkedIn or Profile URL", "Profile URL")
    if not profile_url:
        profile_url = "https://linkedin.com"

    program = get(row, keymap, "Program / Department", "Program", "Department") or "BSA@UTSA"
    academic_level = get(row, keymap, "Academic Level", "Level")
    subject = get(row, keymap, "Subject")
    if not (academic_level and subject):
        m = re.match(r"^(PhD|MS|Undergrad|Undergraduate)\s+in\s+(.+)$", program, flags=re.IGNORECASE)
        if m:
            academic_level = academic_level or ("Undergrad" if m.group(1).lower().startswith("under") else m.group(1).upper())
            subject = subject or m.group(2).strip()

    bio = get(row, keymap, "Short Bio (2-4 lines)", "Short Bio") or f"{name} is part of BSA@UTSA."
    grad = parse_year(get(row, keymap, "Graduation Year"))
    enrollment_term = get(row, keymap, "Enrollment Term", "Enrollment", "Intake Term")

    photo_path = get(row, keymap, "PhotoPath")
    if not (photo_path and photo_path.startswith("/images/")):
        sub = "members" if category == "member" else ("alumni" if category == "alumni" else "officers")
        photo_path = f"/images/{sub}/{slugify(name)}.jpg"

    return {
        "name": name,
        "program": program,
        "academicLevel": academic_level,
        "subject": subject,
        "bio": bio,
        "linkedinUrl": profile_url,
        "photo": photo_path,
        "graduationYear": grad,
        "enrollmentTerm": enrollment_term,
    }


def already_exists(items, key_fields):
    for item in items:
        ok = True
        for k, v in key_fields.items():
            if str(item.get(k, "")).strip().lower() != str(v).strip().lower():
                ok = False
                break
        if ok:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Import BSA profiles from Google Sheet CSV")
    parser.add_argument("--csv", required=True, help="Path to CSV exported from Google Sheets")
    parser.add_argument("--mode", choices=["append", "replace"], default="append")
    args = parser.parse_args()

    csv_path = Path(args.csv).resolve()
    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path}")

    keymap, rows = index_rows(csv_path)

    members_path = DATA_DIR / "members.json"
    officers_path = DATA_DIR / "officers.json"
    alumni_path = DATA_DIR / "alumni.json"

    members = [] if args.mode == "replace" else load_json_list(members_path)
    officers = [] if args.mode == "replace" else load_json_list(officers_path)
    alumni = [] if args.mode == "replace" else load_json_list(alumni_path)

    added_members = 0
    added_officers = 0
    added_alumni = 0

    for row in rows:
        category = get(row, keymap, "Category").lower()
        if category not in {"member", "alumni"}:
            continue

        consent = get(row, keymap, "Consent to publish", "Consent to Publish")
        accuracy = get(row, keymap, "I confirm the submitted information is accurate", "I confirm")
        approved_raw = get(row, keymap, "Approved")
        approved = boolish(approved_raw) if approved_raw else True

        if not (boolish(consent) and boolish(accuracy) and approved):
            continue

        base = build_base_profile(row, keymap, category)

        if category == "member":
            member = {
                "id": next_id("member", members),
                "name": base["name"],
                "program": base["program"],
                "academicLevel": base["academicLevel"] or "",
                "subject": base["subject"] or "",
                "enrollmentTerm": base["enrollmentTerm"] or "Unknown Term",
                "graduationYear": base["graduationYear"] or 0,
                "photo": base["photo"],
                "linkedinUrl": base["linkedinUrl"],
                "bio": base["bio"],
                "isPublic": True,
            }
            if not already_exists(members, {"name": member["name"], "program": member["program"]}):
                members.append(member)
                added_members += 1

            committee_yes = get(row, keymap, "Are you on the current BSA committee?")
            if boolish(committee_yes):
                role = get(row, keymap, "Committee Role (if Yes)") or "Committee Member"
                term = get(row, keymap, "Committee Term (if Yes)") or "Current"
                officer = {
                    "id": next_id("officer", officers),
                    "name": base["name"],
                    "role": role,
                    "program": base["program"],
                    "term": term,
                    "photo": base["photo"],
                    "linkedinUrl": base["linkedinUrl"],
                    "bio": base["bio"],
                    "isPublic": True,
                }
                if not already_exists(officers, {"name": officer["name"], "role": officer["role"], "term": officer["term"]}):
                    officers.append(officer)
                    added_officers += 1

        elif category == "alumni":
            current_position = get(row, keymap, "Current Position (Alumni)") or "Alumnus"
            al = {
                "id": next_id("alumni", alumni),
                "name": base["name"],
                "role": "Alumnus",
                "program": base["program"],
                "graduationYear": base["graduationYear"] or 0,
                "currentPosition": current_position,
                "photo": base["photo"],
                "linkedinUrl": base["linkedinUrl"],
                "bio": base["bio"],
                "isPublic": True,
            }
            if not already_exists(alumni, {"name": al["name"], "program": al["program"], "graduationYear": al["graduationYear"]}):
                alumni.append(al)
                added_alumni += 1

    save_json_list(members_path, members)
    save_json_list(officers_path, officers)
    save_json_list(alumni_path, alumni)

    print("Import completed.")
    print(f"Added members: {added_members}")
    print(f"Added officers: {added_officers}")
    print(f"Added alumni: {added_alumni}")


if __name__ == "__main__":
    main()
