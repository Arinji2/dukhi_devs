import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { getNews } from "./news";
import { NewsItem } from "./news-item";
import { NewsSearch } from "./news-search";

export default async function NewsPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; isCase?: string }>;
}) {
  const { q, isCase } = await searchParams;
  const query = q ?? "indian legal news";
  const isCaseQuery = isCase ?? "false";
  const data = await getNews(query);

  return (
    <div className="flex min-h-screen w-full flex-col gap-6">
      <div className="relative h-62.5 w-full">
        <div className="-z-10 absolute inset-0">
          <div className="absolute inset-0 z-10 bg-black/80" />
          <Image src="/news.png" alt="news" fill className="object-cover" />
        </div>

        <div className="flex h-full flex-col items-center justify-center gap-4">
          <h1 className="font-title text-6xl text-pastel-teal">
            {isCase === "true" ? "CASE UPDATES" : "LEGAL NEWS"}
          </h1>

          <p className="w-[25%] text-center text-foreground">
            {isCase === "true"
              ? "Track realtime updates on real cases"
              : "Search for all news related to indian legal cases and updates"}
          </p>

          <NewsSearch initialQuery={query} />
        </div>
      </div>
      <div className="flex w-full flex-col items-center justify-center">
        <Button className="w-fit" asChild>
          <Link href="/">Back to Home</Link>
        </Button>
      </div>

      {/* RESULTS */}
      <div className="flex flex-wrap items-center justify-center gap-4 gap-x-12 px-6">
        {data.map((article) => (
          <NewsItem key={article.url} article={article} />
        ))}
      </div>
    </div>
  );
}
