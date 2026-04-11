import type { Metadata } from "next";
import { DM_Sans } from "next/font/google";
import "./globals.css";

const dmSans = DM_Sans({
  variable: "--font-dm-sans",
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
    <html lang="en" className={`$ ${dmSans.variable}  h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-olive-900">{children}</body>
    </html>
  );
}
