import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        swiss: {
          red: "#D82C2C",
          black: "#1A1A1A",
          white: "#FFFFFF",
          grey: "#A9B2B1",
          blue: "#0033A0",
          light: "#F2F2F2",
          border: "#E2E6E6",
        },
      },
      fontFamily: {
        sans: ["Helvetica Neue", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
        mono: ["JetBrains Mono", "SF Mono", "Consolas", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
