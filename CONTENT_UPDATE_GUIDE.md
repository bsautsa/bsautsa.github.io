# Content and Image Update Guide

## Fastest way (no manual JSON editing)

Run:

```bash
npm run content:add
```

Then choose:

- `1` news
- `2` event
- `3` member
- `4` officer
- `5` alumni

It will ask simple questions and automatically append a valid entry in the correct JSON file.

## Import from Google Form Sheet (bulk)

1. In your linked Google Sheet, go to `File -> Download -> Comma-separated values (.csv)`.
2. Run:

```bash
npm run content:import -- --csv /path/to/your-sheet.csv
```

3. Optional replace mode (overwrite current `members/officers/alumni` from sheet):

```bash
npm run content:import -- --csv /path/to/your-sheet.csv --mode replace
```

Rules:
- Imports only `Category = Member` or `Category = Alumni`.
- `Member + committee = Yes` creates an officer record too.
- For members, use an `Enrollment Term` column (example: `Fall 2025`, `Spring 2026`) for grouped display.
- Requires consent + accuracy confirmation.
- If `Approved` column exists, only rows with `Approved = Yes` are imported.

## 1) Where to put images

Use these folders:

- News images: `public/images/news/`
- Event images: `public/images/events/`
- Member photos: `public/images/members/`
- Officer photos: `public/images/officers/`
- Alumni photos: `public/images/alumni/`
- Personal profile photos: `public/images/people/`

Use file names like: `spring-cultural-night-2026.jpg` (lowercase, hyphenated).

## 2) How to reference images in JSON

Always use a path starting with `/images/...`.

Example in `data/news.json`:

```json
{
  "coverImage": "/images/news/spring-cultural-night-2026.jpg",
  "gallery": [
    "/images/news/spring-cultural-night-2026-1.jpg",
    "/images/news/spring-cultural-night-2026-2.jpg"
  ]
}
```

Example in `data/events.json`:

```json
{
  "coverImage": "/images/events/spring-cultural-night-2026.jpg",
  "gallery": [
    "/images/events/spring-cultural-night-2026-1.jpg"
  ]
}
```

## 3) Recommended image size

- Card/cover images: `1600x900` (16:9)
- Profile images: `800x1000` (4:5)
- Format: `.jpg` for photos, `.png` only when needed
- Keep most files below ~400 KB when possible

## 4) Update workflow

1. Add image files to `public/images/...`
2. Run `npm run content:add` and answer prompts (or edit JSON manually)
3. Run checks:

```bash
npm run validate:content
npm run build
```

4. Commit and push.

## 5) Common errors

- `Image not showing`: path typo in JSON
- `Build fails`: invalid JSON syntax (missing comma/quote)
- `Wrong image loaded`: old filename cached, rename file and update JSON
