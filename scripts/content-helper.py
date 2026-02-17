#!/usr/bin/env python3
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_list(filename):
    path = DATA / filename
    with path.open("r", encoding="utf-8") as f:
        return json.load(f), path


def save_list(path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def ask(prompt, default=None, required=True):
    suffix = f" [{default}]" if default is not None else ""
    while True:
        value = input(f"{prompt}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        if not required:
            return ""
        print("This field is required.")


def ask_bool(prompt, default=True):
    d = "y" if default else "n"
    val = ask(f"{prompt} (y/n)", d, required=True).lower()
    return val in ("y", "yes", "true", "1")


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text or "item"


def next_id(prefix, items):
    n = len(items) + 1
    return f"{prefix}-{n:03d}"


def split_gallery(raw):
    vals = [v.strip() for v in raw.split(",") if v.strip()]
    return vals


def add_news():
    items, path = load_list("news.json")
    title = ask("News title")
    slug = ask("Slug", slugify(title))
    cover = ask("Cover image path", "/images/news/new-item.jpg")
    gallery = split_gallery(ask("Gallery image paths (comma-separated)", cover))
    tags = split_gallery(ask("Tags (comma-separated)", "BSA,UTSA"))

    item = {
        "id": next_id("news", items),
        "slug": slug,
        "title": title,
        "summary": ask("Short summary"),
        "content": ask("Full content"),
        "coverImage": cover,
        "gallery": gallery,
        "publishedAt": ask("Publish date (YYYY-MM-DD)", str(date.today())),
        "author": ask("Author", "BSA Media Team"),
        "tags": tags,
        "seo": {
            "title": ask("SEO title", f"{title} | BSA@UTSA"),
            "description": ask("SEO description"),
            "ogImage": cover,
        },
    }
    items.append(item)
    save_list(path, items)
    print(f"Added news item to {path}")


def add_event():
    items, path = load_list("events.json")
    title = ask("Event title")
    slug = ask("Slug", slugify(title))
    cover = ask("Cover image path", "/images/events/new-event.jpg")
    start = ask("Start date (YYYY-MM-DD)", str(date.today()))
    status = ask("Status", "upcoming")

    item = {
        "id": next_id("event", items),
        "slug": slug,
        "title": title,
        "description": ask("Description"),
        "startDate": start,
        "endDate": ask("End date (YYYY-MM-DD)", start),
        "location": ask("Location", "UTSA"),
        "registrationUrl": ask("Registration URL", "https://forms.gle/example"),
        "coverImage": cover,
        "gallery": split_gallery(ask("Gallery image paths (comma-separated)", cover)),
        "videoUrl": ask("Video URL (optional)", "", required=False),
        "isFeatured": ask_bool("Feature this event?", default=False),
        "status": status if status in ("upcoming", "past") else "upcoming",
    }
    items.append(item)
    save_list(path, items)
    print(f"Added event to {path}")


def add_profile(kind, filename):
    items, path = load_list(filename)
    name = ask(f"{kind} name")
    item = {
        "id": next_id(kind.lower(), items),
        "name": name,
        "role": ask("Role", kind) if kind != "Member" else None,
        "program": ask("Program", "BSA@UTSA"),
        "term": ask("Term/year", str(date.today().year), required=False),
        "graduationYear": None,
        "currentPosition": ask("Current position (optional)", "", required=False),
        "photo": ask("Photo path", f"/images/{kind.lower()}s/{slugify(name)}.jpg"),
        "linkedinUrl": ask("Profile URL", "https://linkedin.com"),
        "bio": ask("Short bio", f"{name} is part of BSA@UTSA."),
        "isPublic": ask_bool("Public profile?", default=True),
    }

    if kind == "Member":
        item.pop("role", None)
        item.pop("term", None)
        item["academicLevel"] = ask("Academic level (PhD/MS/Undergrad)", "MS")
        item["subject"] = ask("Subject", "Computer Science")
        item["program"] = f"{item['academicLevel']} in {item['subject']}"
        item["enrollmentTerm"] = ask("Enrollment term (e.g., Fall 2025)", "Fall 2025")
        item["graduationYear"] = int(ask("Graduation year", str(date.today().year)))
        item.pop("currentPosition", None)
    elif kind == "Officer":
        item.pop("graduationYear", None)
        item.pop("currentPosition", None)
    elif kind == "Alumni":
        item["role"] = "Alumnus"
        item.pop("term", None)
        item["graduationYear"] = int(ask("Graduation year", str(date.today().year - 1)))
        item["currentPosition"] = ask("Current position", "Professional role")

    items.append(item)
    save_list(path, items)
    print(f"Added {kind.lower()} to {path}")


def main():
    print("Content Helper")
    print("1) Add news")
    print("2) Add event")
    print("3) Add member")
    print("4) Add officer")
    print("5) Add alumni")
    choice = ask("Choose an option", required=True)

    if choice == "1":
        add_news()
    elif choice == "2":
        add_event()
    elif choice == "3":
        add_profile("Member", "members.json")
    elif choice == "4":
        add_profile("Officer", "officers.json")
    elif choice == "5":
        add_profile("Alumni", "alumni.json")
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
