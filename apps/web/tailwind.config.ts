import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0c1116",
        panel: "#111a22",
        accent: "#35c2ff",
        positive: "#2dd4bf",
        negative: "#fb7185"
      }
    }
  },
  plugins: []
};

export default config;
