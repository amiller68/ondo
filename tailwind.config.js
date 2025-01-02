/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./src/**/*.py",
  ],
  theme: {
    extend: {
      keyframes: {
        typewriter: {
          to: { left: "100%" }
        },
        blink: {
          "0%": {
            opacity: "0"
          },
          "50%": {
            opacity: "1"
          }
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        'spin': {
          'from': {
            transform: 'rotate(0deg)'
          },
          'to': {
            transform: 'rotate(360deg)'
          }
        }
      },
      animation: {
        typewriter: "typewriter 2s steps(16) forwards",
        caret: "typewriter 2s steps(16) forwards, blink 1s steps(2) infinite 2s",
        'fade-in': 'fade-in 0.5s ease-out',
        'spin': 'spin 1s linear infinite'
      },
      colors: {
        black: '#000000',
        white: '#fff',
        accent: "#f56565",
      },
      spacing: {
        4: "1rem",
        8: "2rem",
        12: "3rem",
        16: "4rem",
      },
      fontFamily: {
        'roboto': ['"Roboto"', 'monospace'],
      },
      boxShadow: {
        'header': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
      },
      borderWidth: {
        '2': '2px',
      },
      transitionProperty: {
        'all': 'all',
        'transform': 'transform',
      },
      transitionDuration: {
        '300': '300ms',
      },
      rotate: {
        '45': '45deg',
        '-45': '-45deg',
      }
    },
  },
  plugins: []
}