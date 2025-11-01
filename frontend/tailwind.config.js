/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        wakfu: {
          primary: '#00a8e8',
          secondary: '#f77f00',
          dark: '#003049',
          light: '#edf2f4',
        },
      },
    },
  },
  plugins: [],
}

