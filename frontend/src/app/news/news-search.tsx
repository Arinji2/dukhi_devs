"use client";

import { Loader2 } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { useState, useTransition } from "react";
import { NewsPaperIcon } from "@/components/icons/newspaper";
import { SearchIcon } from "@/components/icons/search";

export function NewsSearch({ initialQuery }: { initialQuery: string }) {
  const router = useRouter();
  const params = useSearchParams();

  const [value, setValue] = useState(initialQuery);
  const [isPending, startTransition] = useTransition();

  function submit() {
    startTransition(() => {
      const sp = new URLSearchParams(params.toString());
      sp.set("q", value);
      router.push(`/news?${sp.toString()}`);
    });
  }

  return (
    <div className="flex h-12 w-[60%] items-center gap-3 rounded-md border bg-card px-4">
      <NewsPaperIcon className="size-6 text-pastel-green" />
      <div className="h-full w-px bg-border" />

      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Search legal news..."
        className="w-full bg-transparent text-white outline-none"
      />

      <button
        type="button"
        disabled={isPending}
        onClick={submit}
        className="flex size-8 items-center justify-center rounded bg-pastel-green disabled:opacity-60"
      >
        {isPending ? (
          <Loader2 className="size-4 animate-spin text-background" />
        ) : (
          <SearchIcon className="size-4 text-background" />
        )}
      </button>
    </div>
  );
}
