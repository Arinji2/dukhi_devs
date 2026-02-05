import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { getAdminPb } from "@/lib/pb";
import { PetitionsItem } from "./item";

export default async function PetitionsPage() {
  const pb = await getAdminPb();
  const petitionsData = await pb.collection("petitions").getFullList();
  return (
    <div className="flex min-h-screen w-full flex-col gap-6">
      <div className="relative h-62.5 w-full">
        <div className="-z-10 absolute inset-0">
          <div className="absolute inset-0 z-10 bg-black/80" />
          <Image src="/support.png" alt="news" fill className="object-cover" />
        </div>

        <div className="flex h-full flex-col items-center justify-center gap-4">
          <h1 className="font-title text-6xl text-pastel-teal">
            PETITIONS AND SUPPORT
          </h1>

          <p className="w-[30%] text-center text-foreground">
            Support other women with legal issues via digiallty signing
            petitions in their support
          </p>
        </div>
      </div>
      <div className="flex w-full flex-col items-center justify-center">
        <Button className="w-fit" asChild>
          <Link href="/">Back to Home</Link>
        </Button>
      </div>

      <div className="flex flex-wrap items-center justify-center gap-4 gap-x-12 px-6">
        {petitionsData.map((item) => {
          return <PetitionsItem key={item.id} item={item} />;
        })}
      </div>
    </div>
  );
}
