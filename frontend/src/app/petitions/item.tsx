"use client";

import { useState } from "react";
import { CalenderIcon } from "@/components/icons/calender";
import { Button } from "@/components/ui/button";
import type { PetitionsRecord } from "@/lib/pocketbase-types";

export function PetitionsItem({ item }: { item: PetitionsRecord }) {
  const [hasSupported, setHasSupported] = useState(false);
  const GOAL = 180;
  const progress = Math.min(Math.round((item.signatures! / GOAL) * 100), 100);
  return (
    <div className="flex h-fit w-75 flex-col gap-4 rounded-md bg-card py-3">
      <div className="flex items-center justify-between border-b px-3 pb-2">
        <div className="flex items-center gap-1">
          <CalenderIcon className="size-4 text-pastel-orange" />
          <p className="text-xs">{new Date(item.created).toDateString()}</p>
        </div>
      </div>

      <h2 className="line-clamp-2 px-3 font-bold text-xl">{item.title}</h2>

      <p className="line-clamp-4 px-3 text-muted-foreground text-xs">
        {item.description}
      </p>

      <div className="flex h-fit w-full flex-col items-start justify-start px-3">
        <p className="font-medium text-foreground text-xs tracking-tighter">
          SIGNATURES
        </p>
        <p className="text-muted-foreground text-sm">
          <span className="font-medium text-secondary">{item.signatures}</span>{" "}
          of 180 goal
        </p>
        <div className="relative mt-2 h-2 w-full overflow-hidden rounded-full bg-muted">
          <div
            className="h-full rounded-full bg-secondary transition-[width] duration-300 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="px-3">
        <Button
          disabled={hasSupported}
          className="w-full"
          onClick={() => {
            setHasSupported(true);
            item.signatures = item.signatures! + 1;
          }}
          size="sm"
        >
          Show Support
        </Button>
      </div>
    </div>
  );
}
