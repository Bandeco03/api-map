# Sistema de Coleta Automática de Dados

## O que foi implementado

### 1. Coleta Automática em Background
- **Task assíncrona** que roda automaticamente ao iniciar a aplicação
- Coleta dados da API externa **a cada 5 minutos**
- Salva os dados incrementalmente no banco de dados SQLite
- Logs no console para acompanhar o processo

### 2. Banco de Dados SQLite
- Arquivo: `power_data.db` (criado automaticamente)
- Armazena **todos os registros** de forma incremental
- Cada registro contém:
  - ID único
  - Timestamp da coleta
  - Dados completos da API (JSON)
  - Código de resultado
  - Mensagem de resultado

### 3. Novos Endpoints

#### `GET /api/power-data`
- **Retorna apenas os últimos dados coletados**
- Não faz chamada à API externa
- Lê do banco de dados

#### `GET /api/power-data/history?limit=100`
- Retorna histórico de dados coletados
- Parâmetro `limit` define quantos registros retornar (padrão: 100)
- Ordenado do mais recente para o mais antigo

#### `GET /api/power-data/fetch-now`
- Força uma coleta imediata (fora do ciclo de 5 minutos)
- Útil para testes ou updates manuais
- Salva os dados no banco

#### `GET /health`
- Health check
- Informa se a task de background está rodando

## Como funciona

1. **Ao iniciar o backend**, a task de background inicia automaticamente
2. **A cada 5 minutos**, os dados são coletados da API externa e salvos no banco
3. **O frontend** agora consulta `/api/power-data` que retorna dados do banco (rápido)
4. **Histórico completo** fica armazenado para análises futuras

## Arquivos modificados/criados

- ✅ `requirements.txt` - Adicionado SQLAlchemy e aiosqlite
- ✅ `database.py` - Novo arquivo para gerenciar o banco de dados
- ✅ `main.py` - Modificado para incluir coleta automática e novos endpoints

## Como testar

1. Inicie o backend:
```bash
cd backend
python main.py
```

2. Você verá no console:
```
🚀 Background data collection started - fetching every 5 minutes
📊 [2025-11-04 10:30:00] Fetching power data from API...
✅ Data saved to database with ID: 1
```

3. Acesse os endpoints:
- http://localhost:8000/api/power-data - Últimos dados
- http://localhost:8000/api/power-data/history - Histórico
- http://localhost:8000/api/power-data/fetch-now - Forçar coleta agora
- http://localhost:8000/health - Status da task

## Vantagens

✅ Não depende do frontend para coletar dados
✅ Dados históricos preservados
✅ Consultas rápidas (banco local)
✅ Reduz chamadas à API externa
✅ Sistema autônomo e resiliente

