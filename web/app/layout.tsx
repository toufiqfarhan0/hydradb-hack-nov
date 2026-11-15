import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LUCEN — Agent Context Layer for HydraDB",
  description:
    "Lucen is an active agent context store built on HydraDB. Traverses tool schemas, skills, and resolved runtime entities in 1.8ms via OpenCypher instead of naive prompt preloading.",
  keywords: [
    "HydraDB",
    "OpenCypher",
    "GraphBLAS",
    "Agent Context Layer",
    "MCP Tools",
    "Model Context Protocol",
    "AI Coding Agents",
    "Context Compression"
  ],
  authors: [{ name: "Lucen Research ft. HydraDB" }],
  openGraph: {
    title: "LUCEN — Agent Context Layer for HydraDB",
    description: "Prune 94% of prompt context tokens in 1.8ms via HydraDB OpenCypher matrix traversals.",
    siteName: "Lucen",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "LUCEN — Agent Context Layer for HydraDB",
    description: "Prune 94% of prompt context tokens in 1.8ms via HydraDB OpenCypher matrix traversals.",
  },
};

export const viewport: Viewport = {
  themeColor: "#D82C2C",
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen bg-white text-[#1A1A1A] font-sans antialiased selection:bg-[#D82C2C] selection:text-white">
        {children}
      </body>
    </html>
  );
}
