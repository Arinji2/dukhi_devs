import { CalenderIcon } from "@/components/icons/calender";
import { OrganizationIcon } from "@/components/icons/organization";
import { Button } from "@/components/ui/button";

export function NewsItem({ article }: { article: any }) {
  return (
    <div className="flex h-[250px] w-[300px] flex-col gap-4 rounded-md bg-card py-3">
      <div className="flex items-center justify-between border-b px-3 pb-2">
        <div className="flex items-center gap-1">
          <OrganizationIcon className="size-4 text-pastel-pink" />
          <p className="text-xs">{article.publisher.title}</p>
        </div>

        <div className="flex items-center gap-1">
          <CalenderIcon className="size-4 text-pastel-orange" />
          <p className="text-xs">
            {new Date(article.published_date).toDateString()}
          </p>
        </div>
      </div>

      <h2 className="line-clamp-2 px-3 font-bold text-xl">{article.title}</h2>

      <p className="line-clamp-4 px-3 text-muted-foreground text-xs">
        {article.description}
      </p>

      <div className="px-3">
        <Button size="sm" asChild>
          <a href={article.url} target="_blank">
            Read Article
          </a>
        </Button>
      </div>
    </div>
  );
}
