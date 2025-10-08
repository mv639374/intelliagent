import type { Config } from "tailwindcss";
import animatePlugin from "tailwindcss-animate"; // <-- CHANGED

const config = {
  darkMode: "class",
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      // ... (rest of the theme config is unchanged)
    },
  },
  plugins: [animatePlugin], // <-- CHANGED
} satisfies Config;

export default config;
