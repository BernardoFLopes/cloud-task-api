# Cloud Tasks API — Projeto Final de Computação em Nuvem

Aplicação Flask/SQLite com esteira de **CI/CD no GitHub Actions, Docker, GHCR e AWS EC2**.

## Integrantes
- **Bernardo Ferreira Lopes (RA: 22309764)** — Configuração do GitHub/Actions, desenvolvimento dos endpoints (`DELETE` e filtro) e deploy na EC2.

## Arquitetura
`Branch/PR -> CI (pytest + Docker build) -> merge main -> CI (publicação GHCR por SHA) -> CD (SSH EC2 + docker pull/run) -> /health`

## Rodar localmente
```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate  |  Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m pytest -q
python -m flask --app app.main run --port 5000
```
Ou com Docker:
```bash
docker compose up --build
```
E acesse `http://localhost:8080/health`.

## Endpoints da API
| Método | Rota | Função |
|---|---|---|
| GET | `/` | Informações da API |
| GET | `/health` | Saúde da aplicação e conexão com o SQLite |
| GET | `/tasks` | Lista tarefas (suporta filtro opcional `?done=true` ou `?done=false`) |
| POST | `/tasks` | Cria tarefa (`{"title":"..."}`) |
| PATCH | `/tasks/<id>` | Atualiza conclusão (`{"done":true}`) |
| DELETE | `/tasks/<id>` | Remove uma tarefa existente (`204 No Content` ou `404 Not Found`) |

### Exemplos de uso:
```bash
# Checar saúde
curl http://localhost:8080/health

# Criar tarefa
curl -X POST http://localhost:8080/tasks -H "Content-Type: application/json" -d '{"title":"Minha tarefa"}'

# Listar todas ou filtrar por concluídas
curl http://localhost:8080/tasks
curl "http://localhost:8080/tasks?done=true"

# Marcar como concluída
curl -X PATCH http://localhost:8080/tasks/1 -H "Content-Type: application/json" -d '{"done":true}'

# Excluir tarefa
curl -X DELETE http://localhost:8080/tasks/1 -i
```

## Documentação e Relatório
- Guia de configuração: [docs/CONFIGURACAO.md](docs/CONFIGURACAO.md)
- Relatório técnico da entrega: [RELATORIO.md](RELATORIO.md)
