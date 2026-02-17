import { siteData } from "@/utils/content";

export function GET() {
  const body = `User-agent: *\nAllow: /\n\nSitemap: ${siteData.canonicalBaseUrl}/sitemap.xml\n`;
  return new Response(body, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8"
    }
  });
}
