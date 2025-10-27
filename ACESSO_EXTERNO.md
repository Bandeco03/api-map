# Como Acessar a Aplicação Externamente

## Configuração Concluída ✅

O arquivo `vite.config.js` já foi configurado para aceitar conexões externas.

## Como Usar

### 1. Iniciar o Servidor de Desenvolvimento
```bash
npm run dev
```

### 2. Descobrir seu IP Local
Abra o terminal e execute:

**Windows (CMD):**
```cmd
ipconfig
```

**Windows (PowerShell):**
```powershell
ipconfig
```

Procure por "Endereço IPv4" na interface de rede ativa (geralmente algo como `192.168.x.x` ou `10.0.x.x`)

### 3. Acessar de Outro Computador na Rede Local

De qualquer dispositivo na mesma rede WiFi/LAN, acesse:
```
http://SEU_IP:5173
```

Exemplo: `http://192.168.1.100:5173`

---

## Para Acesso pela Internet (Fora da Rede Local)

Para permitir acesso de computadores fora da sua rede local, você tem estas opções:

### Opção 1: Port Forwarding no Roteador (Mais Seguro)
1. Acesse as configurações do seu roteador (geralmente `192.168.1.1` ou `192.168.0.1`)
2. Encontre a seção "Port Forwarding" ou "Encaminhamento de Portas"
3. Crie uma regra:
   - Porta Externa: 5173
   - Porta Interna: 5173
   - IP Destino: Seu IP local (ex: 192.168.1.100)
   - Protocolo: TCP
4. Descubra seu IP público em: https://whatismyipaddress.com/
5. Compartilhe: `http://SEU_IP_PUBLICO:5173`

**⚠️ Atenção de Segurança:**
- Isso expõe sua aplicação à internet
- Use apenas para testes temporários
- Considere adicionar autenticação
- Feche o port forwarding quando não precisar mais

### Opção 2: Túnel com Ngrok (Mais Rápido)
1. Instale o Ngrok: https://ngrok.com/download
2. Execute:
   ```bash
   ngrok http 5173
   ```
3. O Ngrok fornecerá uma URL pública (ex: `https://abc123.ngrok.io`)
4. Compartilhe essa URL

**Vantagens:**
- Não precisa configurar roteador
- HTTPS automático
- Mais seguro que port forwarding direto

### Opção 3: Deploy em Produção (Recomendado)
Para uso permanente, faça deploy em:

**Vercel (Grátis):**
```bash
npm install -g vercel
npm run build
vercel
```

**Netlify (Grátis):**
```bash
npm install -g netlify-cli
npm run build
netlify deploy --prod --dir=dist
```

**GitHub Pages:**
1. Adicione em `vite.config.js`:
   ```javascript
   base: '/api-map/'
   ```
2. Instale gh-pages:
   ```bash
   npm install -D gh-pages
   ```
3. Adicione no `package.json`:
   ```json
   "scripts": {
     "deploy": "npm run build && gh-pages -d dist"
   }
   ```
4. Execute:
   ```bash
   npm run deploy
   ```

---

## Firewall do Windows

Se não conseguir acessar mesmo na rede local, pode ser o firewall:

1. Pesquise "Firewall do Windows" no menu Iniciar
2. Clique em "Permitir um aplicativo pelo Firewall do Windows"
3. Clique em "Alterar configurações"
4. Procure por "Node.js" e marque as caixas "Privada" e "Pública"
5. Ou crie uma nova regra para a porta 5173

---

## Testando

Quando o servidor estiver rodando, você verá algo como:
```
  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.1.100:5173/
```

Use o endereço "Network" para compartilhar com outros dispositivos!

