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
    server: {
        host: '0.0.0.0', // Permite conexões de qualquer IP
        port: 5173, // Porta padrão do Vite
        strictPort: false, // Tenta outra porta se 5173 estiver ocupada
        allowedHosts: [
            '.ngrok-free.app',
            '.ngrok.io',
            'localhost',
        ],
    },
})
