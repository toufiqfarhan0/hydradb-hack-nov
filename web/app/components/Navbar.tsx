"use client";

import React from "react";
import Link from "next/link";
import { ArrowUpRight, Sliders, BookOpen } from "lucide-react";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md swiss-border-b">
      <div className="max-w-[1400px] mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4 whitespace-nowrap">
        {/* Brand Logo */}
        <div className="flex items-center flex-shrink-0">
          <Link href="/" className="flex items-center gap-2.5 group cursor-pointer flex-shrink-0 whitespace-nowrap">
            <span className="w-3.5 h-3.5 bg-[#D82C2C] inline-block transition-transform duration-200 group-hover:scale-110 flex-shrink-0" />
            <span className="font-bold tracking-tighter text-xl font-swiss-display text-[#1A1A1A] whitespace-nowrap">
              LUCEN
            </span>
            <span className="hidden sm:inline-block text-[11px] font-swiss-mono font-bold text-[#A9B2B1] pl-2 border-l border-[#E2E6E6]">
              HYDRADB CONTEXT LAYER
            </span>
          </Link>
        </div>

        {/* Navigation Links: Docs, Console, and Blog */}
        <div className="flex items-center gap-5 flex-shrink-0 whitespace-nowrap">
          <nav className="flex items-center gap-5 text-xs font-swiss-mono font-medium flex-shrink-0">
            <Link
              href="/docs"
              className="text-[#1A1A1A] hover:text-[#D82C2C] transition-colors font-bold flex items-center gap-1.5"
            >
              <BookOpen className="w-3.5 h-3.5 text-[#0033A0]" />
              <span>Docs</span>
            </Link>
            <Link
              href="/console"
              className="text-[#1A1A1A] hover:text-[#D82C2C] transition-colors font-bold flex items-center gap-1.5"
            >
              <Sliders className="w-3.5 h-3.5 text-[#D82C2C]" />
              <span>Console</span>
            </Link>
            <Link
              href="/blog"
              className="text-[#D82C2C] font-bold hover:underline inline-flex items-center gap-0.5"
            >
              <span>Blog</span>
              <ArrowUpRight className="w-3 h-3" />
            </Link>
            <a
              href="https://lucen-app.onrender.com"
              target="_blank"
              rel="noreferrer"
              className="hidden sm:inline-flex items-center gap-1.5 px-2 py-0.5 bg-emerald-50 text-emerald-800 border border-emerald-300 text-[10px] font-swiss-mono font-bold hover:bg-emerald-100 transition-colors"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse" />
              <span>LIVE DEMO</span>
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
}
