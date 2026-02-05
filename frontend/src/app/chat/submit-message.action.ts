"use server";

import { revalidatePath } from "next/cache";
import { getClarityPB } from "@/lib/pb-clarity";

export async function SubmitMessageAction(message: string) {
  const pb = await getClarityPB();

  pb.collection("chatbot_test").create({
    query: message,
    status: "pending",
  });

  revalidatePath("/chat", "page");

  return {
    message: "Message sent successfully",
  };
}
