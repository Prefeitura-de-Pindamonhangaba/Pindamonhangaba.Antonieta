# Revisão de melhorias

Os itens da revisão inicial foram implementados:

| Item | Resultado |
| --- | --- |
| Autenticação geral | Rotas de negócio exigem JWT; login permanece público. |
| Permissões de usuários | Gestão de usuários exige perfil de administrador no backend. |
| Troca de ração | Entradas e distribuições estornam o saldo anterior e aplicam o novo movimento na mesma transação. |
| Exclusão de distribuição | Registro correto é excluído e quantidade retorna ao estoque uma única vez. |
| Quantidades e concorrência | Valores inválidos são rejeitados; operações não podem deixar saldo negativo; bloqueios são testados no PostgreSQL. |
| Erros de distribuição | Falta de estoque retorna 400; recursos ausentes retornam 404. |
| Contratos frontend/backend | Atualização por ID, filtros de movimentações, buscas de beneficiários, tipos de ração e dashboard usam contratos existentes e testados. |
| CORS | Usa as origens configuradas, remove espaços, tem padrão local e rejeita configuração com wildcard. |
| Sessão no frontend | Expiração é checada localmente, identidade/perfil são confirmados no backend e 401 encerra a sessão pelo cliente HTTP compartilhado. |
| Auditoria e privacidade | Operações de negócio registram responsável, entidade e campos afetados na mesma transação; valores pessoais de beneficiários não são copiados para logs. |
| DTOs e respostas | Distribuições aceitam frações na criação/edição, preservam observações e usam erros consistentes. |

A documentação pública da API permanece desativada. Exclusões de rações ou
beneficiários com movimentações vinculadas retornam 409 para preservar o histórico.
Edições de nome/descrição da ração não sobrescrevem o saldo de estoque.

## Validação das correções

Para cada correção, reproduza o defeito em um teste, aplique o ajuste e execute
novamente os testes afetados e a suíte correspondente antes de enviar os commits.

- Backend: `python -m unittest discover -s tests -v` em `Antonieta.Backend`.
- Concorrência PostgreSQL: comando e isolamento documentados em `Antonieta.Backend/tests/README.md`.
- Frontend: `npm test` e `npm run build` em `Antonieta.Frontend`.
- Navegador: `npx playwright test --config playwright.security.config.ts` em `Antonieta.Tests`, com o frontend ativo.

Os workflows executam os testes do backend, concorrência PostgreSQL, frontend,
build e testes de sessão no navegador. A suíte principal usa SQLite em memória;
a de concorrência usa schemas temporários exclusivos. Testes de navegador
interceptam a API e não alteram os dados da aplicação. Migrações Alembic não são
validadas por essas suítes.
