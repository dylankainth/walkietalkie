// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  ssr: false,
  modules: [
    '@nuxtjs/tailwindcss',
    '@vite-pwa/nuxt',
  ],
  routeRules: {
    '/pyapi/**': {
      proxy: process.env.NODE_ENV === "development" ? "http://127.0.0.1:8000/pyapi/**" : "/pyapi/**",
    },
    '/docs': {
      proxy: "http://127.0.0.1:8000/docs",
    },
    '/openapi.json': {
      proxy: "http://127.0.0.1:8000/openapi.json",
    }
  },
  nitro: {
    vercel: {
      config: {
        routes: [{
          "src": "/pyapi/(.*)",
          "dest": "pyapi/index.py"
        }]
      }
    },
  },
  pwa: {
    manifest: {
      name: 'WalkieTalkie',
      short_name: 'WalkieTalkie',
      start_url: '/',
      display: 'standalone',
      background_color: '#ffffff',
      theme_color: '#ffffff',
      description: 'Your AI Tour Guide',
      lang: 'en',
      icons: [
        // {
        //   src: '/logo.svg',
        //   sizes: '192x192',
        //   type: 'image/svg',
        // },
        // {
        //   src: '/logo512.png',
        //   sizes: '512x512',
        //   type: 'image/png',
        // },
      ]
    }
  },

})
