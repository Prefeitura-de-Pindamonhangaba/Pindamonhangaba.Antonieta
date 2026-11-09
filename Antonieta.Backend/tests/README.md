# Testes do backend

Na pasta `Antonieta.Backend`, com Python 3.11 ou superior:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m unittest discover -s tests -v
```

Executar apenas um grupo:

```powershell
.venv\Scripts\python -m unittest discover -s tests -p test_endpoint_security.py -v
.venv\Scripts\python -m unittest discover -s tests -p test_api_integration.py -v
.venv\Scripts\python -m unittest discover -s tests -p test_reports_and_regressions.py -v
```

Não é necessário iniciar Docker, frontend, backend ou PostgreSQL. A suíte configura
um segredo JWT exclusivo para testes e usa SQLite em memória, com chaves estrangeiras
habilitadas e um banco novo para cada caso. Nenhum dado do `.env` é usado para acessar
o banco da aplicação. Execute em um processo separado, pelos comandos acima.

## Cobertura

- Segurança de todas as rotas: token ausente, inválido e expirado; login público;
  documentação desativada; gestão de usuários restrita a administradores.
- Integração HTTP com JWT, bcrypt e persistência reais: login, renovação, usuário
  removido, mudança de perfil, CRUD de usuários, auditoria e proteção de senhas.
- Beneficiários: criação, consulta, exclusão, validação e ocultação de registros antigos.
- Estoque: entrada com quantidade fracionada, edição, exclusão e distribuição.
- Dashboard e relatórios: totais, filtros, registros antigos e limite final de datas.

## Regressões de estoque

Os testes exigem erro 400 para estoque insuficiente sem alteração de saldo, rejeição
de entradas negativas, zero e valores não finitos na criação e edição, e devolução
ao estoque ao excluir uma distribuição. A exclusão repetida não pode duplicar o
estorno. Todos esses casos devem passar, sem falhas esperadas ou testes ignorados.

SQLite não substitui a validação de migrações, concorrência e particularidades do
PostgreSQL. Os testes Playwright existentes em `Antonieta.Tests` continuam separados.
