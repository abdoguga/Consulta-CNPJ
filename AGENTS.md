# AGENTS.md

Notas de setup deste repositório (o que não é óbvio pelos manifests).

## Como rodar

```bash
docker compose -f docker-compose.base44.yml up -d --build
```

Serviços: `db` (Postgres 16), `migrate` (one-shot que cria as tabelas), `api`
(FastAPI + uvicorn `--reload`) e `web` (Vite dev server). O entry point público é
a porta **3000**.

Detalhes que importam:

- **`web` roda `npm install` na inicialização** dentro do volume nomeado
  `web_node_modules` (o `node_modules` do host não é usado). O `package.json` é
  montado junto, então mudar dependências exige apenas reiniciar o serviço.
- **Dependências Python ficam na imagem** (`api/Dockerfile` instala
  `requirements.txt`). Ao alterar `api/requirements.txt`, suba com `--build`.
- **Uma única origem**: o dev server do Vite faz proxy de `/api` para
  `http://api:8000` (ver `API_URL` em `web/vite.config.js`), então não há CORS
  nem cookie cross-site. A porta 8000 também é exposta, mas só para
  depuração/webhooks.
- **Não existe autenticação**: qualquer visitante pode consultar e mexer no
  histórico.
- **Nenhum segredo é necessário**: os dados vêm da
  [BrasilAPI](https://brasilapi.com.br/docs#tag/CNPJ), pública e sem chave. O
  container `api` precisa de saída para a internet.

## Modo preview (sandbox)

`BASE44_PREVIEW_MODE` é repassado pelo compose aos serviços `api` e `web`:

- `= "1"` → liga polling do watcher nos dois lados (`WATCHFILES_FORCE_POLLING`
  no uvicorn e `server.watch.usePolling` no Vite), necessário porque bind mount
  pode não gerar eventos de inotify.
- ausente/outro valor → comportamento normal (inotify), sem nenhum override.

Nunca fixe a flag em `1` no compose/Dockerfile; no `command` do compose use
`$$BASE44_PREVIEW_MODE` para a variável ser lida em tempo de execução, e não
substituída na hora de parsear o YAML.

## Verificando que está de pé

```bash
docker compose -f docker-compose.base44.yml ps          # tudo healthy
curl -s localhost:3000/ | grep -q '@vite/client'        # dev server servindo fonte
curl -s localhost:8000/api/cnpj/33000167000101          # consulta real (Petrobras)
curl -s localhost:3000/api/historico                    # proxy /api do Vite
```

Healthchecks usam apenas endpoints já existentes: `/openapi.json` na `api` e `/`
no `web`. Não crie endpoint só para healthcheck.

`GET /api/cnpj/{cnpj}` **grava** no histórico — ao testar, remova o registro
criado por você com `DELETE /api/historico/{id}`.
