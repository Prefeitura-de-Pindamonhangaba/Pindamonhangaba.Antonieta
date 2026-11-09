# Testes do frontend

Na pasta `Antonieta.Frontend`:

```powershell
npm ci
npm test
npm run build
```

Os testes Vitest não precisam de backend ou navegador. Cobrem tokens expirados e
malformados, confirmação de identidade/perfil no servidor, tratamento centralizado
de 401, preservação da sessão em 403/500, permissões de navegação e os contratos dos
serviços de usuários, tipos de ração e dashboard.

A checagem local de expiração não valida a assinatura JWT: as rotas confirmam a
sessão em `/auth/me`, e o backend continua responsável por autenticação/autorização.

Para os testes de navegador, inicie o frontend em `http://localhost:3000` e execute
na pasta `Antonieta.Tests`:

```powershell
npx playwright install chromium
npx playwright test --config playwright.security.config.ts
```

As chamadas para a API local são interceptadas nesses quatro testes; nenhum dado
do banco é criado ou alterado. Use `FRONTEND_URL` se o frontend estiver em outra porta.
O workflow do frontend executa os testes unitários, build e testes de navegador.
