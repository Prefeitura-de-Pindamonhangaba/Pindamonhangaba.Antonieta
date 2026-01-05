# Guia de Migração - Flag "old" para Registros Antigos

## 📋 Resumo

Este documento descreve as alterações implementadas para marcar registros antigos de beneficiários e distribuições com uma flag `old`, ocultando-os da visualização normal dos usuários, mas mantendo-os no sistema.

## 🎯 Objetivo

Reiniciar a base de dados de cadastro de beneficiários, considerando apenas cadastros realizados a partir de **5 de janeiro de 2026**. Os registros anteriores são marcados como "antigos" e não aparecem nas listagens normais.

## 🔧 Alterações Realizadas

### 1. Modelos de Dados

#### Beneficiary Model
- **Adicionado**: Campo `old` (Boolean, default=False, indexed)
- **Localização**: `models/beneficiary_model.py`

#### Distribution Model
- **Adicionado**: Campo `old` (Boolean, default=False, indexed)
- **Localização**: `models/distribution_model.py`

### 2. Migração de Banco de Dados

- **Arquivo**: `alembic/versions/14ad4711b267_add_old_flag_to_beneficiary_and_.py`
- **Ações**:
  - Adiciona coluna `old` às tabelas `beneficiary` e `distribution`
  - Cria índices para otimizar queries
  - Define valor padrão `FALSE` para registros existentes

### 3. Serviços Atualizados

#### Beneficiary Services (`services/beneficiary_services.py`)
- `get_all_beneficiaries_service()`: Filtra `old == False`
- `get_beneficiary_by_id_service()`: Filtra `old == False`

#### Distribution Services (`services/distribution_services.py`)
- `get_all_distribution_service()`: Filtra `old == False`
- `get_distribution_by_id_service()`: Filtra `old == False`

### 4. Script de Migração de Dados

- **Arquivo**: `mark_old_records.py`
- **Função**: Marca todos os registros criados antes de 2026-01-05 como `old=True`

## 🚀 Como Aplicar as Mudanças

### Passo 1: Aplicar a Migração do Banco de Dados

```bash
cd Antonieta.Backend
alembic upgrade head
```

Isso irá:
- Adicionar a coluna `old` às tabelas
- Definir todos os registros existentes como `old=FALSE`

### Passo 2: Marcar Registros Antigos

Execute o script para marcar registros anteriores a 2026-01-05:

```bash
cd Antonieta.Backend
python mark_old_records.py
```

O script irá:
- Mostrar quantos registros serão afetados
- Solicitar confirmação do usuário
- Marcar beneficiários e distribuições antigas como `old=TRUE`
- Exibir estatísticas finais

### Passo 3: Verificar a Aplicação

Reinicie a aplicação:

```bash
# Se estiver usando Docker
docker-compose restart backend

# Ou se estiver rodando localmente
# Reinicie o servidor FastAPI
```

## 📊 Comportamento Esperado

### Antes da Migração
- Todos os beneficiários e distribuições são visíveis
- Queries retornam todos os registros

### Depois da Migração
- Apenas beneficiários com `old=FALSE` são visíveis
- Apenas distribuições com `old=FALSE` são visíveis
- Registros antigos permanecem no banco de dados
- Consultas diretas ao banco ainda podem acessar registros antigos

## 🔍 Consultas Úteis

### Ver todos os beneficiários (incluindo antigos)
```sql
SELECT * FROM beneficiary;
```

### Ver apenas beneficiários ativos
```sql
SELECT * FROM beneficiary WHERE old = FALSE;
```

### Ver apenas beneficiários antigos
```sql
SELECT * FROM beneficiary WHERE old = TRUE;
```

### Estatísticas
```sql
-- Contar beneficiários ativos vs antigos
SELECT 
    old,
    COUNT(*) as total
FROM beneficiary
GROUP BY old;

-- Contar distribuições ativas vs antigas
SELECT 
    old,
    COUNT(*) as total
FROM distribution
GROUP BY old;
```

## 🔄 Rollback (Reverter Alterações)

Se necessário reverter as alterações:

```bash
cd Antonieta.Backend
alembic downgrade -1
```

⚠️ **ATENÇÃO**: Isso removerá a coluna `old` e todos os dados serão perdidos!

## 📝 Próximos Passos (Sugestões)

1. **Interface de Administração**: Criar uma página admin para visualizar registros antigos
2. **Relatórios**: Adicionar opção para incluir registros antigos em relatórios
3. **Auditoria**: Registrar quando um beneficiário é marcado como antigo
4. **Filtro**: Adicionar toggle na interface para mostrar/ocultar registros antigos
5. **Exportação**: Criar funcionalidade para exportar dados históricos

## ⚠️ Observações Importantes

- Os registros antigos **não são deletados**, apenas ocultados
- Relações entre beneficiários e distribuições são mantidas
- O campo `old` é indexado para otimizar performance
- Novos registros sempre terão `old=FALSE` por padrão
- A data de corte é **2026-01-05 00:00:00**

## 🐛 Troubleshooting

### Erro: "column old does not exist"
- Execute `alembic upgrade head`

### Registros antigos ainda aparecem
- Verifique se executou o `mark_old_records.py`
- Reinicie a aplicação

### Não consigo ver nenhum beneficiário
- Verifique se todos os registros foram marcados como `old=TRUE`
- Execute consulta SQL para confirmar: `SELECT COUNT(*) FROM beneficiary WHERE old = FALSE;`

## 📞 Suporte

Em caso de dúvidas ou problemas, consulte a documentação do projeto ou entre em contato com a equipe de desenvolvimento.
