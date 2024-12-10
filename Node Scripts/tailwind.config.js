/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  variant: {
    extend: {
      animation: ['group-hover'],
    },
  },
  plugins: [],
}