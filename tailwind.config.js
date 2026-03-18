/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./_includes/*.html",
    "./build.py",        // scans dynamically generated class names (reviews, etc.)
  ],
  theme: {
    extend: {
      colors: {
        brand: { 600: "#1e40af", 700: "#1d3a8a", 800: "#1e3066" },
        accent: { 500: "#f59e0b", 600: "#d97706" },
      },
    },
  },
  plugins: [],
}
