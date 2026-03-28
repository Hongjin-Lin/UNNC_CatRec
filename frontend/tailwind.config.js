/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        cream: {
          50:  '#FFF8F0',
          100: '#FEF3E2',
          200: '#FDE8C8',
        },
        brand: {
          light:  '#FDBA74',
          DEFAULT:'#F97316',
          dark:   '#EA580C',
        },
        paw: {
          dark: '#1C1917',
          mid:  '#44403C',
          soft: '#78716C',
        },
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
