import Image from "next/image";
import { CalenderIcon } from "@/components/icons/calender";
import { NewsPaperIcon } from "@/components/icons/newspaper";
import { OrganizationIcon } from "@/components/icons/organization";
import { SearchIcon } from "@/components/icons/search";
import { Button } from "@/components/ui/button";

export default function NewsPage() {
  return (
    <div className="flex min-h-screen w-full flex-col items-center justify-start gap-5">
      <div className="relative flex h-62.5 w-full flex-col items-center justify-start gap-2">
        <div className="-z-10 absolute h-full w-full">
          <div className="absolute z-10 h-full w-full bg-black/80"></div>
          <Image src="/news.png" alt="news" fill className="object-cover" />
        </div>
        <div className="flex h-full w-full flex-col items-center justify-center gap-2 py-4">
          <h1 className="font-title text-6xl text-pastel-teal">
            LEGAL NEWS FEED
          </h1>
          <div className="flex w-[25%] flex-col items-center justify-center">
            <p className="text-center text-foreground tracking-tighter">
              Search for all news related to indian legal cases and updates
            </p>
          </div>

          <div className="mt-auto flex h-12 w-[60%] flex-row items-center justify-start gap-3 rounded-md border border-border bg-card px-4 shadow-lg">
            <NewsPaperIcon className="size-6 text-pastel-green" />
            <div className="h-full w-px bg-border"></div>
            <input
              className="h-full w-full resize-none border-transparent font-content text-white outline-none"
              placeholder="Type your message here..."
            />
            <button
              type="button"
              className="flex size-7 w-8 flex-col items-center justify-center rounded-[2.6px] bg-pastel-green"
            >
              <SearchIcon className="size-4 text-background" />
            </button>
          </div>
        </div>
      </div>
      <div className="flex h-fit w-full flex-row items-center justify-start gap-4 px-6">
        <NewsItem />
      </div>
    </div>
  );
}

function NewsItem() {
  return (
    <div className="flex h-[250px] w-[300px] flex-col items-start justify-start gap-4 rounded-md bg-card py-3">
      <div className="flex h-fit w-full flex-row items-center justify-between border-border border-b px-3 pb-2">
        <div className="flex h-fit w-fit items-center justify-center gap-1">
          <OrganizationIcon className="size-4 text-pastel-pink" />
          <p className="font-content text-foreground text-xs">Times of India</p>
        </div>
        <div className="flex h-fit w-fit items-center justify-center gap-1">
          <CalenderIcon className="size-4 text-pastel-orange" />
          <p className="font-content text-foreground text-xs">Times of India</p>
        </div>
      </div>
      <h2 className="line-clamp-2 px-3 font-bold font-content text-2xl text-foreground">
        New Cyber Safety Laws Enacted
      </h2>
      <h2 className="line-clamp-3 px-3 font-content font-light text-muted-foreground text-xs">
        Stay informed about the latest cyber laws aimed at protecting digital
        identities and banking transactions from fraud.
      </h2>
      <div className="h-fit w-fit px-3">
        <Button
          size="sm"
          className="justify-start px-6 py-1 font-medium text-[10px]"
        >
          Read Article
        </Button>
      </div>
    </div>
  );
}
