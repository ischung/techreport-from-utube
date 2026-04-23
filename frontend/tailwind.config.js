/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: { DEFAULT: "#0a0a0a", subtle: "#111113", card: "#151518" },
        border: { DEFAULT: "#27272a", strong: "#3f3f46" },
        // WCAG AA contrast against bg (#0a0a0a):
        //   fg         #e4e4e7  → 17.9:1  (AAA)
        //   fg-muted   #b0b0b8  →  9.0:1  (AAA)  — tuned up from zinc-400
        //   fg-subtle  #8b8b93  →  5.8:1  (AA+) — tuned up from zinc-500
        fg: { DEFAULT: "#e4e4e7", muted: "#b0b0b8", subtle: "#8b8b93" },
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
