import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueDevTools(),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    },
    preview: {
        host: '0.0.0.0', // Permite conexões de qualquer IP no preview
        port: 4173, // Porta padrão do preview (pode mudar se quiser)
        strictPort: false,
        allowedHosts: [
            '.ngrok-free.app',
            '.ngrok.io',
            'localhost',
        ],
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            }
        }
    },
})
