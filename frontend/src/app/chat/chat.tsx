"use client";
type Messages = {
  message: string;
  is_user: boolean;
  date: Date;
};

import Image from "next/image";
import { useRouter } from "next/navigation";
import Pocketbase from "pocketbase";
import { useEffect, useState } from "react";
import { SendIcon } from "@/components/icons/send";
import { SmartToyIcon } from "@/components/icons/smart-toy";
import { cn } from "@/lib/utils";
import { SubmitMessageAction } from "./submit-message.action";

const pb = new Pocketbase("https://db-clarity.arinji.com");
export function ChatUI() {
  const [messages, setMessages] = useState<Messages[]>([
    {
      message:
        "Welcome to Suraksha Sakhi, an AI-powered legal assistant. How can I help you today?",
      is_user: false,
      date: new Date(),
    },
  ]);
  useEffect(() => {
    pb.collection("chatbot_test").subscribe("*", (doc) => {
      console.log(doc);
      if (doc.action === "update") {
        if (doc.record.status === "done") {
          setMessages((prev) => [
            ...prev,
            {
              message: doc.record.result,
              is_user: false,
              date: new Date(),
            },
          ]);
        }
      }
    });

    return () => {
      pb.collection("chatbot_test").unsubscribe("*");
    };
  }, []);
  const [typedMessage, setTypedMessage] = useState("");
  const router = useRouter();

  return (
    <div className="relative h-screen w-full overflow-hidden">
      <div className="pointer-events-none absolute inset-0 z-0">
        <div className="h-full w-full bg-[url('/chat.png')] bg-center bg-cover bg-no-repeat opacity-5" />
      </div>

      <div className="relative z-10 flex h-full w-full flex-col items-center">
        <div className="w-full flex-1 overflow-y-auto px-4 py-6">
          <div className="mx-auto flex w-full max-w-4xl flex-col gap-8">
            {messages.map((message) => (
              <ChatMessage
                key={Math.random()}
                message={message.message!}
                isUser={message.is_user!}
                date={new Date(message.date)}
              />
            ))}
          </div>
        </div>

        <div className="w-full border-border border-t bg-card px-4 py-3">
          <div className="mx-auto flex h-16 w-full max-w-4xl items-center gap-3 rounded-md">
            <textarea
              value={typedMessage}
              onChange={(e) => setTypedMessage(e.target.value)}
              className="h-full w-full resize-none bg-transparent text-white outline-none"
              placeholder="Type your message here..."
            />
            <button
              type="button"
              onClick={async () => {
                await SubmitMessageAction(typedMessage);
                setMessages((prev) => [
                  ...prev,
                  {
                    message: typedMessage,
                    is_user: true,
                    date: new Date(),
                  },
                ]);
                setTypedMessage("");
              }}
              className="flex size-9 items-center justify-center rounded-md bg-background"
            >
              <SendIcon className="size-4 text-pastel-green" />
            </button>
          </div>
        </div>
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

  message = message.replaceAll("\n", "");
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
        <div className="flex size-8 flex-col items-center justify-center overflow-hidden rounded-full">
          <Image
            src="/avatar.png"
            alt="avatar"
            width={40}
            height={40}
            className="rounded-full"
          />
        </div>
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
