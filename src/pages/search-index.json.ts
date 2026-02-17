import { newsData, eventsData, membersData, officersData, alumniData } from "@/utils/content";

export function GET() {
  const rows = [
    ...newsData.map((item) => ({
      type: "News",
      title: item.title,
      excerpt: item.summary,
      url: `/news/${item.slug}`,
      text: `${item.title} ${item.summary} ${item.content} ${item.tags.join(" ")}`.toLowerCase()
    })),
    ...eventsData.map((item) => ({
      type: "Event",
      title: item.title,
      excerpt: item.description,
      url: `/events/${item.slug}`,
      text: `${item.title} ${item.description} ${item.location}`.toLowerCase()
    })),
    ...membersData.map((item) => ({
      type: "Member",
      title: item.name,
      excerpt: item.bio,
      url: "/members",
      text: `${item.name} ${item.program} ${item.bio}`.toLowerCase()
    })),
    ...officersData.map((item) => ({
      type: "Officer",
      title: item.name,
      excerpt: `${item.role ?? "Officer"} | ${item.program}`,
      url: "/officers",
      text: `${item.name} ${item.role ?? ""} ${item.program} ${item.bio}`.toLowerCase()
    })),
    ...alumniData.map((item) => ({
      type: "Alumni",
      title: item.name,
      excerpt: item.currentPosition ?? item.bio,
      url: "/alumni",
      text: `${item.name} ${item.currentPosition ?? ""} ${item.bio}`.toLowerCase()
    }))
  ];

  return new Response(JSON.stringify(rows), {
    headers: {
      "Content-Type": "application/json"
    }
  });
}
