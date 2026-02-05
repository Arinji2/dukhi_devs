import PocketBase from "pocketbase";
import type { TypedPocketBase } from "./pocketbase-types";

export const pb = new PocketBase(
  "https://innxio-pb.arinji.com",
) as TypedPocketBase;

export const getAdminPb = async () => {
  await pb
    .collection("_superusers")
    .authWithPassword("arinjaydhar205@gmail.com", "U11tItkeUTBgix7");
  return pb;
};

export const getUserPb = async () => {
  await pb.collection("users").authWithPassword("test@gmail.com", "123456789");
  return pb;
};
