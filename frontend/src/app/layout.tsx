import type { Metadata } from "next";
import { Germania_One, Roboto } from "next/font/google";
import "./globals.css";

const germaniaOne = Germania_One({
  variable: "--font-germania-one",
  subsets: ["latin"],
  weight: ["400"],
});

const roboto = Roboto({
  variable: "--font-roboto",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Suraksha Setu",
  description: "Suraksha Setu",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${roboto.variable} ${germaniaOne.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
