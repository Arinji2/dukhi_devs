export const dynamic = "force-dynamic";
export const CHAT_ID = "ddvdncakqfa8apm";

import { getAdminPb } from "@/lib/pb";
import { ChatUI } from "./chat";
import { ChatList } from "./chat-list";

export default async function ChatPage() {
  const pb = await getAdminPb();
  const chats = await pb.collection("messages").getFullList({
    filter: `chat='${CHAT_ID}'`,
  });
  return (
    <div className="relative flex h-screen flex-row items-center justify-center bg-background">
      <ChatList />
      <ChatUI messages={chats} />
    </div>
  );
}
