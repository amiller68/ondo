/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./src/**/*.py",
  ],
  darkMode: 'class',
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
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        success: {
          DEFAULT: "hsl(var(--success))",
          foreground: "hsl(var(--success-foreground))",
        },
        warning: {
          DEFAULT: "hsl(var(--warning))",
          foreground: "hsl(var(--warning-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
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
      },
      height: {
        'screen': '100vh',
        'screen-small': '-webkit-fill-available', // For iOS Safari
      },
      minHeight: {
        'screen': '100vh',
        'screen-small': '-webkit-fill-available', // For iOS Safari
      },
    },
  },
  plugins: []
}