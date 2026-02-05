export const dynamic = "force-dynamic";
export const CHAT_ID = "ddvdncakqfa8apm";

import type { MessagesRecord } from "@/lib/pocketbase-types";
import { ChatUI } from "./chat";
import { ChatList } from "./chat-list";

export default async function ChatPage() {
  return (
    <div className="relative flex h-screen flex-row items-center justify-center bg-background">
      <ChatList />
      <ChatUI />
    </div>
  );
}
