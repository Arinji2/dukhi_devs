import { AddIcon } from "@/components/icons/add";
import { HomeIcon } from "@/components/icons/home";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function ChatList() {
  return (
    <div className="flex h-full w-[40%] flex-col items-center justify-start gap-7 overflow-y-auto border-border border-r bg-card px-4 py-6">
      <div className="flex h-fit w-full flex-col items-center justify-start gap-3">
        <Button className="flex w-full flex-row items-center justify-center gap-1 bg-pastel-blue">
          <HomeIcon className="size-5 text-foreground" />
          <p className="font-content font-medium text-foreground">Home</p>
        </Button>
        <Button className="flex w-full flex-row items-center justify-center gap-1 bg-pastel-lavender">
          <AddIcon className="size-5 text-foreground" />
          <p className="font-content font-medium text-foreground">New Chat</p>
        </Button>
      </div>
      <div className="flex h-fit w-full flex-col items-start justify-start gap-3">
        <p className="font-content font-semibold text-gray-500 text-xs tracking-tighter">
          RECENTS
        </p>
        <ChatCard
          name="Workplace Harrasment Query"
          date={new Date()}
          active={true}
        />

        <ChatCard
          name="Workplace Harrasment Query"
          date={new Date()}
          active={false}
        />

        <ChatCard
          name="Workplace Harrasment Query"
          date={new Date()}
          active={false}
        />

        <ChatCard
          name="Workplace Harrasment Query"
          date={new Date()}
          active={false}
        />

        <ChatCard
          name="Workplace Harrasment Query"
          date={new Date()}
          active={false}
        />

        <ChatCard
          name="Workplace Harrasment Query"
          date={new Date()}
          active={false}
        />

        <ChatCard
          name="Workplace Harrasment Query"
          date={new Date()}
          active={false}
        />

        <ChatCard
          name="Workplace Harrasment Query"
          date={new Date()}
          active={false}
        />

        <ChatCard
          name="Workplace Harrasment Query"
          date={new Date()}
          active={false}
        />
      </div>
    </div>
  );
}

function ChatCard({
  name,
  date,
  active,
}: {
  name: string;
  date: Date;
  active: boolean;
}) {
  const formatted = new Intl.DateTimeFormat("en-IN", {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(date);
  return (
    <div
      className={cn(
        "flex h-15 w-full flex-col items-start justify-center gap-1 rounded-md bg-primary p-3",
        {
          "border border-primary bg-card": !active,
        },
      )}
    >
      <p className="font-content font-semibold text-foreground text-xs">
        {name}
      </p>
      <p className="font-content text-[10px] text-foreground/80">{formatted}</p>
    </div>
  );
}
