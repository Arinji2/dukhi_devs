import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="relative flex h-fit flex-col items-center justify-start bg-sidebar">
      <div className="fixed top-0 left-0 h-lvh w-full">
        <div className="from absolute z-10 h-full w-full bg-linear-to-b from-black/80"></div>

        <Image
          src="/landing.png"
          alt="Landing"
          fill
          className="object-cover object-bottom"
        />
      </div>
      <div className="z-20 flex h-fit w-full flex-col items-center justify-start gap-6 px-4 py-6">
        <div className="flex h-fit flex-col items-center justify-center gap-3 xl:w-[40%]">
          <h1 className="text-center font-title text-7xl text-pastel-teal">
            Suraksha Sakhi
          </h1>
          <p className="text-center font-content text-foreground/70 text-xl">
            Empowering women and children through legal awareness, safety tools,
            and community support.
          </p>
        </div>
        <div className="flex h-fit w-full flex-col items-center justify-evenly gap-4 md:flex-row">
          <div className="flex h-55 w-full flex-col items-start justify-start gap-2 rounded-md bg-pastel-blue p-4 shadow-lg md:w-68.25">
            <h2 className="font-title text-4xl text-foreground">
              Legal Assistant
            </h2>
            <p className="font-content text-foreground text-lg">
              AI powered chat for instant legal guidance
            </p>
            <Button
              asChild
              className="mt-auto bg-foreground text-pastel-teal hover:bg-foreground/80"
            >
              <Link href="/chat">Start Chatting</Link>
            </Button>
          </div>
          <div className="flex h-55 w-full flex-col items-start justify-start gap-2 rounded-md bg-pastel-green p-4 shadow-lg md:w-68.25">
            <h2 className="font-title text-4xl text-foreground">Safety News</h2>
            <p className="font-content text-foreground text-lg">
              Stay updated with the latest legal news updates
            </p>

            <Button
              asChild
              className="mt-auto bg-foreground text-pastel-green hover:bg-foreground/80"
            >
              <Link href="/news">Read More</Link>
            </Button>
          </div>
          <div className="flex h-55 w-full flex-col items-start justify-start gap-2 rounded-md bg-pastel-mauve p-4 shadow-lg md:w-68.25">
            <h2 className="font-title text-4xl text-foreground">
              Case Updates
            </h2>
            <p className="font-content text-foreground text-lg">
              AI powered chat for instant legal guidance
            </p>
            <Button className="mt-auto bg-foreground text-pastel-mauve hover:bg-foreground/80">
              <Link href="/news?q=rg+kor+case">Read More</Link>
            </Button>
          </div>
          <div className="flex h-55 w-full flex-col items-start justify-start gap-2 rounded-md bg-pastel-lavender p-4 shadow-lg md:w-68.25">
            <h2 className="font-title text-4xl text-foreground">
              Sign Petitions
            </h2>
            <p className="font-content text-foreground text-lg">
              Join movements and digitally sign to show your support
            </p>
            <Button className="mt-auto bg-foreground text-pastel-lavender hover:bg-foreground/80">
              Show Support
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
