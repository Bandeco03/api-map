# 🌐 Deploy com ngrok - Acesso Universal

## 🎯 Cenário: Backend + Frontend no MESMO PC, acesso via ngrok

Você quer que qualquer pessoa acesse seu site apenas abrindo um link, sem configurar nada.

---

## 📋 Passo a Passo

### 1️⃣ Instale o ngrok

```powershell
# Opção 1: Download direto
# Acesse: https://ngrok.com/download

# Opção 2: Via Chocolatey
choco install ngrok

# Configure seu token (crie conta grátis em ngrok.com)
ngrok authtoken SEU_TOKEN_AQUI
```

---

### 2️⃣ Inicie Backend e Frontend

**Terminal 1 - Backend:**
```powershell
cd backend
python main.py
```
✅ Backend rodando em `http://localhost:8000`

**Terminal 2 - Frontend (build):**
```powershell
cd frontend
npm run build
npm run preview
```
✅ Frontend rodando em `http://localhost:4173`

---

### 3️⃣ Inicie o ngrok APENAS para o Frontend

**Terminal 3 - ngrok:**
```powershell
ngrok http 4173
```

Você verá algo assim:
```
Session Status    online
Forwarding        https://abc123def456.ngrok.io -> http://localhost:4173
```

---

## 🎉 Pronto!

✅ **Compartilhe o link:** `https://abc123def456.ngrok.io`

Qualquer pessoa que abrir esse link verá seu site funcionando completamente!

---

## 🔄 Como Funciona (Proxy Reverso)

```
[Usuário Externo]
        ↓
[https://abc123.ngrok.io] ← Link público
        ↓
[ngrok túnel] → [Frontend localhost:4173]
                        ↓
                [Vite Proxy] → [Backend localhost:8000]
```

### 🎯 Explicação Técnica:

1. **Usuário acessa:** `https://abc123.ngrok.io`
2. **Frontend carrega** e faz requisição: `GET /api/power-data`
3. **Vite proxy intercepta** requisições `/api/*` 
4. **Proxy redireciona** para `http://localhost:8000/api/power-data`
5. **Backend responde** e o proxy retorna os dados ao frontend
6. **Frontend renderiza** os dados normalmente

✅ **Tudo no mesmo PC, apenas 1 túnel ngrok necessário!**

---

## ⚙️ Configurações Aplicadas

### `frontend/vite.config.js`
```javascript
preview: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

### `frontend/.env.production`
```env
VITE_API_URL=
```
*(String vazia = requisições relativas através do proxy)*

---

## 💡 Comandos Resumidos

### Iniciar tudo:
```powershell
# Terminal 1
cd backend
python main.py

# Terminal 2  
cd frontend
npm run build
npm run preview

# Terminal 3
ngrok http 4173
```

### Parar tudo:
- Pressione `Ctrl+C` em cada terminal

---

## 🎯 Vantagens desta Configuração

✅ **Simples:** Apenas 1 túnel ngrok necessário  
✅ **Sem rebuild:** URL do ngrok muda, mas não precisa fazer build novamente  
✅ **Acesso global:** Qualquer pessoa, de qualquer lugar, pode acessar  
✅ **HTTPS grátis:** ngrok fornece certificado SSL automaticamente  
✅ **Sem firewall:** Não precisa configurar portas ou roteador  

---

## ❌ Troubleshooting

### "Este site não pode ser acessado"
- Verifique se o ngrok está rodando
- Verifique se o frontend está rodando (localhost:4173)

### Frontend carrega mas não mostra dados
- Verifique se o backend está rodando (localhost:8000)
- Teste: abra `http://localhost:8000/docs` no navegador do servidor

### "Too Many Connections" (ngrok)
- Versão grátis tem limite de 40 req/min
- Aguarde 1 minuto ou atualize para versão paga

---

## 🚀 Para Produção Real

Se quiser hospedar permanentemente, considere:
- **Vercel** (frontend) + **Render/Railway** (backend) - Grátis
- **Heroku** - Backend e frontend juntos
- **AWS/Azure/GCP** - Mais controle, mas mais complexo
- **ngrok pago** - Mais simples, URL fixa, sem limites

