# Consulta-CNPJ

Consulta de dados públicos de empresas brasileiras (Receita Federal) a partir do
CNPJ, com histórico das consultas.

- **web** — React + Vite (porta 3000)
- **api** — FastAPI (porta 8000), consome a [BrasilAPI](https://brasilapi.com.br/docs#tag/CNPJ)
  (gratuita, **não exige chave/token**)
- **db** — PostgreSQL, guarda o histórico de consultas

## Rodando

```bash
docker compose -f docker-compose.base44.yml up -d --build
```

Depois abra http://localhost:3000. O frontend fala com a API pela própria origem
(`/api`), com proxy do dev server para `http://api:8000`.

## API

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/cnpj/{cnpj}` | Consulta um CNPJ (com ou sem máscara) e registra no histórico |
| `GET` | `/api/historico?limit=10` | Últimas consultas realizadas |
| `DELETE` | `/api/historico/{id}` | Remove uma consulta do histórico |

Exemplo:

```bash
curl http://localhost:8000/api/cnpj/19131243000197
```

Documentação interativa: http://localhost:8000/docs
