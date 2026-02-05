import PocketBase from "pocketbase";

export const pb = new PocketBase("https://db-clarity.arinji.com");

export const getClarityPB = async () => {
  await pb
    .collection("_superusers")
    .authWithPassword("architshinde006@gmail.com", "CB-iC4yQI3OCiCP");
  pb.autoCancellation(false);
  return pb;
};

export const getUserPb = async () => {
  await pb.collection("users").authWithPassword("test@gmail.com", "123456789");
  return pb;
};
