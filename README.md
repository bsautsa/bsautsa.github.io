# BSA@UTSA Website

SEO-first static website for the BSA@UTSA.

## Stack

- Astro static site
- JSON-based content in `data/`
- GitHub Pages deployment

## Domains

- Canonical domain: `https://bsautsa.github.io`
- Mirror domains: none (GitHub Pages is the primary domain)

## Local Setup

```bash
npm install
npm run validate:content
npm run dev
```

## Content Update Workflow

1. Use helper tool:

```bash
npm run content:add
```

2. Or manually update JSON files under `data/`.
3. Add images under `public/images/`.
4. Ensure profile privacy uses `isPublic: true` only for consented profiles.
5. Run:

```bash
npm run validate:content
npm run build
```

6. Open PR and merge into `main`.

For step-by-step image and JSON examples, see `CONTENT_UPDATE_GUIDE.md`.

## Canonical SEO Rules

- All pages set canonical URLs to `https://bsautsa.github.io`.
- `sitemap.xml` only emits canonical URLs.
- `robots.txt` includes canonical sitemap URL.

## Personal Visibility

Abu Noman Md Sakib appears in:

- Global footer developer credit
- About page profile section
- Dedicated page at `/abu-noman-md-sakib` with `Person` JSON-LD
