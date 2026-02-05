import { ChatUI } from "./chat";
import { ChatList } from "./chat-list";

export default function ChatPage() {
  return (
    <div className="relative flex h-screen flex-row items-center justify-center bg-background">
      <ChatList />
      <ChatUI />
    </div>
  );
}
