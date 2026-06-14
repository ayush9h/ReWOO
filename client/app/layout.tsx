import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geist = Geist({
  variable: "--font-geist",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Experiment integrating ReWOO and HITL",
  description: "ReWOO integration with Human in the loop",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`$ ${geist.variable}  h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-stone-800">{children}</body>
    </html>
  );
}
