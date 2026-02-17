import fs from "node:fs/promises";
import path from "node:path";
import { z } from "zod";

const dataDir = path.resolve("data");

const linkSchema = z.object({
  label: z.string().min(1),
  url: z.string().url()
});

const siteSchema = z.object({
  siteName: z.string().min(1),
  siteShortName: z.string().min(1),
  tagline: z.string().min(1),
  canonicalBaseUrl: z.string().url(),
  mirrorUrls: z.array(z.string().url()),
  email: z.string().email(),
  phone: z.string().min(1),
  address: z.string().min(1),
  mapsEmbedUrl: z.string().url(),
  socialLinks: z.array(linkSchema),
  developerCredit: z.object({
    name: z.string().min(1),
    role: z.string().min(1),
    bioShort: z.string().min(1),
    photo: z.string().startsWith("/"),
    links: z.array(linkSchema)
  })
});

const newsItemSchema = z.object({
  id: z.string().min(1),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  title: z.string().min(1),
  summary: z.string().min(1),
  content: z.string().min(1),
  coverImage: z.string().startsWith("/"),
  gallery: z.array(z.string().startsWith("/")),
  publishedAt: z.string().date(),
  author: z.string().min(1),
  tags: z.array(z.string().min(1)),
  seo: z.object({
    title: z.string().min(1),
    description: z.string().min(1),
    ogImage: z.string().startsWith("/")
  })
});

const eventItemSchema = z.object({
  id: z.string().min(1),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  title: z.string().min(1),
  description: z.string().min(1),
  startDate: z.string().date(),
  endDate: z.string().date(),
  location: z.string().min(1),
  registrationUrl: z.string().url(),
  coverImage: z.string().startsWith("/"),
  gallery: z.array(z.string().startsWith("/")),
  videoUrl: z.string(),
  isFeatured: z.boolean(),
  status: z.enum(["upcoming", "past"])
});

const directoryItemSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  role: z.string().optional(),
  program: z.string().min(1),
  academicLevel: z.string().optional(),
  subject: z.string().optional(),
  enrollmentTerm: z.string().optional(),
  term: z.string().optional(),
  graduationYear: z.number().int().optional(),
  currentPosition: z.string().optional(),
  photo: z.string().startsWith("/"),
  linkedinUrl: z.string().url(),
  bio: z.string().min(1),
  isPublic: z.boolean()
});

const alumniItemSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  role: z.string().optional(),
  program: z.string().min(1),
  graduationYear: z.number().int().optional(),
  currentPosition: z.string().optional(),
  institution: z.string().optional(),
  photo: z.string().startsWith("/"),
  linkedinUrl: z.string().url().optional(),
  links: z.array(linkSchema).optional(),
  bio: z.string().min(1),
  isPublic: z.boolean()
});

const joinSchema = z.object({
  newMemberFormUrl: z.string().url(),
  achievementFormUrl: z.string().url(),
  newStudentGuideSections: z.array(
    z.object({
      title: z.string().min(1),
      content: z.string().min(1)
    })
  )
});

const personSchema = z.object({
  slug: z.string().regex(/^[a-z0-9-]+$/),
  name: z.string().min(1),
  headline: z.string().min(1),
  bio: z.string().min(1),
  photo: z.string().startsWith("/"),
  affiliation: z.string().min(1),
  sameAs: z.array(z.string().url()),
  highlights: z.array(z.string().min(1)),
  seo: z.object({
    title: z.string().min(1),
    description: z.string().min(1),
    ogImage: z.string().startsWith("/")
  })
});

const files = [
  ["site.json", siteSchema],
  ["news.json", z.array(newsItemSchema)],
  ["events.json", z.array(eventItemSchema)],
  ["members.json", z.array(directoryItemSchema)],
  ["officers.json", z.array(directoryItemSchema)],
  ["alumni.json", z.array(alumniItemSchema)],
  ["join.json", joinSchema],
  ["people/abu_noman_md_sakib.json", personSchema]
];

let hasError = false;

for (const [file, schema] of files) {
  const fullPath = path.join(dataDir, file);
  const raw = await fs.readFile(fullPath, "utf-8");
  const parsed = JSON.parse(raw);
  const result = schema.safeParse(parsed);

  if (!result.success) {
    hasError = true;
    console.error(`Validation failed for data/${file}`);
    console.error(result.error.issues.map((x) => `- ${x.path.join(".")}: ${x.message}`).join("\n"));
  }
}

if (hasError) {
  process.exit(1);
}

console.log("All content files are valid.");
