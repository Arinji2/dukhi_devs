"use server";

import { getAdminPb } from "@/lib/pb";
import { CHAT_ID } from "./page";

export async function SubmitAIMessageAction(message: string) {
  const user = await getAdminPb();
  await user.collection("messages").create({
    chat: CHAT_ID,
    content: message,
    is_user_message: false,
    created: new Date().toISOString(),
  });
}
