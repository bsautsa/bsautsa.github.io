import { canonicalUrl, newsData, eventsData } from "@/utils/content";

function entry(path: string, lastmod?: string) {
  return `<url><loc>${canonicalUrl(path)}</loc>${lastmod ? `<lastmod>${lastmod}</lastmod>` : ""}</url>`;
}

export function GET() {
  const staticPaths = [
    "/",
    "/news",
    "/events",
    "/members",
    "/officers",
    "/alumni",
    "/join",
    "/about",
    "/search",
    "/abu-noman-md-sakib"
  ];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${staticPaths.map((p) => entry(p)).join("\n")}
${newsData.map((n) => entry(`/news/${n.slug}`, n.publishedAt)).join("\n")}
${eventsData.map((e) => entry(`/events/${e.slug}`, e.startDate)).join("\n")}
</urlset>`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8"
    }
  });
}
