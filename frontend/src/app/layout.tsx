import type { Metadata } from "next";
import localFont from "next/font/local";
import { Layout } from "@/components/layout/layout";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});

const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "WealthBot - AI-Powered Trading Platform",
  description: "Advanced trading bot with Solana integration, powered by LangChain and AI",
  keywords: [
    "trading bot",
    "cryptocurrency",
    "Solana",
    "AI trading",
    "automated trading",
    "WealthBot",
    "blockchain",
  ],
  authors: [{ name: "WealthBot Team" }],
  viewport: {
    width: "device-width",
    initialScale: 1,
  },
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "white" },
    { media: "(prefers-color-scheme: dark)", color: "black" },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} min-h-screen bg-background font-sans antialiased`}
      >
        <Layout>{children}</Layout>
      </body>
    </html>
  );
}