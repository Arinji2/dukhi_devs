type Article = {
  query: string;
  title: string;
  description: string;
  url: string;
  published_date: string;
  publisher: {
    title: string;
  };
};

import { unstable_cache } from "next/cache";

export function getNews(query: string) {
  return unstable_cache(async () => {
    const queryEncoded = encodeURIComponent(query);
    console.log(query);
    const res = await fetch(
      `https://innxio-news.arinji.com/news?search=${queryEncoded}`,
    );
    const data = await res.json();
    return data.articles as Article[];
  }, ["news-search", query])();
}
