/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: { DEFAULT: "#0a0a0a", subtle: "#111113", card: "#151518" },
        border: { DEFAULT: "#27272a", strong: "#3f3f46" },
        fg: { DEFAULT: "#e4e4e7", muted: "#a1a1aa", subtle: "#71717a" },
        accent: { DEFAULT: "#22c55e" },
        warn: { DEFAULT: "#f59e0b" },
        error: { DEFAULT: "#f43f5e" },
        info: { DEFAULT: "#0ea5e9" },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      boxShadow: {
        card: "0 1px 0 0 rgba(255,255,255,0.04), 0 0 0 1px rgba(255,255,255,0.06)",
      },
    },
  },
  plugins: [],
};
