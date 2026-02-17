import site from "../../data/site.json";
import news from "../../data/news.json";
import events from "../../data/events.json";
import members from "../../data/members.json";
import officers from "../../data/officers.json";
import alumni from "../../data/alumni.json";
import join from "../../data/join.json";
import sakib from "../../data/people/abu_noman_md_sakib.json";

export const siteData = site;
export const newsData = [...news].sort((a, b) => (a.publishedAt < b.publishedAt ? 1 : -1));
export const eventsData = [...events].sort((a, b) => (a.startDate > b.startDate ? 1 : -1));
export const membersData = members.filter((item) => item.isPublic);
export const officersData = officers.filter((item) => item.isPublic);
export const alumniData = alumni.filter((item) => item.isPublic);
export const joinData = join;
export const sakibData = sakib;

export function canonicalUrl(pathname: string): string {
  const base = siteData.canonicalBaseUrl.replace(/\/$/, "");
  const path = pathname.startsWith("/") ? pathname : `/${pathname}`;
  return `${base}${path === "/" ? "" : path}`;
}

export function formatDate(dateIso: string): string {
  return new Date(dateIso).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric"
  });
}
