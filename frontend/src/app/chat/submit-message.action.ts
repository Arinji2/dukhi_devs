"use server";

import { getUserPb } from "@/lib/pb";
import { CHAT_ID } from "./page";
import { revalidatePath } from "next/cache";

export async function SubmitMessageAction(message: string) {
  const user = await getUserPb();
  const res = await user.collection("messages").create({
    chat: CHAT_ID,
    content: message,
    is_user_message: true,
    created: new Date().toISOString(),
  });
  revalidatePath("/chat", "page");

  //Do mock request
  return {
    message: "Message sent successfully",
  };
}
