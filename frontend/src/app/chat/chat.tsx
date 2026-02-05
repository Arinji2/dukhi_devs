import { SendIcon } from "@/components/icons/send";
import { SmartToyIcon } from "@/components/icons/smart-toy";
import { cn } from "@/lib/utils";
export function ChatUI() {
  return (
    <div className="relative flex h-full w-full flex-col items-center">
      <div className="fixed bottom-6 z-20 flex h-16 w-[60%] flex-row items-center justify-between rounded-md border border-border bg-card px-4 py-4 shadow-lg">
        <textarea
          className="h-full w-full resize-none border-transparent font-content text-white outline-none"
          placeholder="Type your message here..."
        />
        <button
          type="button"
          className="flex size-9 flex-col items-center justify-center rounded-md bg-background"
        >
          <SendIcon className="size-4 text-pastel-green" />
        </button>
      </div>
      <div className="before:-z-10 relative isolate flex h-full w-full flex-col items-center justify-start gap-8 px-4 py-6 before:pointer-events-none before:absolute before:inset-0 before:bg-[url('/chat.png')] before:bg-size-[70%] before:bg-repeat before:opacity-3 before:content-['']">
        <ChatMessage
          message="Hello, I am your Suraksha Setu Legal Assistant. Briefly describe your  situation, and I will guide you through relevant laws and rights."
          isUser={false}
          date={new Date()}
        />

        <ChatMessage
          message="
                  I am experiencing verbal harassment from my manager at the
                  office. He constantly makes demeaning comments about my
                  appearance in front of the team.
"
          isUser={true}
          date={new Date()}
        />
      </div>
    </div>
  );
}
function ChatMessage({
  message,
  isUser,
  date,
}: {
  message: string;
  isUser: boolean;
  date: Date;
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
        "flex h-fit w-full flex-row items-end justify-start gap-3",
        {
          "flex-row-reverse": isUser,
        },
      )}
    >
      {isUser ? (
        <div className="flex size-8 flex-col items-center justify-center rounded-full bg-pastel-mauve"></div>
      ) : (
        <div className="flex size-8 flex-col items-center justify-center rounded-full bg-primary/40">
          <SmartToyIcon className="size-5 text-blue-500" />
        </div>
      )}
      <div className="flex h-full w-full flex-col items-center justify-start gap-2">
        <div
          className={cn(
            "flex h-fit w-full flex-row items-center justify-start gap-2",
            {
              "justify-end": isUser,
            },
          )}
        >
          <p className="font-content font-medium text-muted-foreground text-xs">
            {isUser ? "You" : "Suraksha Sakhi"}
          </p>
          <div className="size-1 rounded-full bg-muted-foreground"></div>

          <p className="font-content font-medium text-muted-foreground text-xs">
            {formatted}
          </p>
        </div>
        <div
          className={cn(
            "flex h-full w-full flex-col items-start justify-center rounded-lg rounded-tl-none bg-card p-3 shadow-lg",
            {
              "rounded-tl-lg rounded-br-none bg-primary": isUser,
            },
          )}
        >
          <p className="font-content text-foreground text-sm">{message}</p>
        </div>
      </div>
    </div>
  );
}
