<div align="center">
  <img src=".\Antonieta.Frontend\assets\Antonieta logotipo-02.svg" alt="Projeto Antonieta Banner" width="50%">

  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)](https://vuejs.org/)
  [![Nuxt](https://img.shields.io/badge/Nuxt-3.0+-00DC82?style=for-the-badge&logo=nuxt.js&logoColor=white)](https://nuxt.com/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-4.5+-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
  [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-CC2927?style=for-the-badge&logo=swagger&logoColor=white)](https://www.sqlalchemy.org/)
  [![Naive UI](https://img.shields.io/badge/Naive_UI-2.0+-18A058?style=for-the-badge&logo=vue.js&logoColor=white)](https://www.naiveui.com/)
</div>

# Projeto Antonieta - Sistema de Distribuição de Rações

Sistema desenvolvido para gerenciar a distribuição de rações do Projeto Antonieta da Prefeitura de Pindamonhangaba.

## 🚀 Tecnologias

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Python 3.10+
- Alembic (Migrations)

### Frontend
- Vue.js 3
- Nuxt 3
- Naive UI
- TypeScript

## 📋 Pré-requisitos

- Python 3.10 ou superior
- Node.js 16 ou superior
- PostgreSQL
- Git

## 🔧 Instalação

### Opção 1: Instalação com Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/abraaom/Pindamonhangaba.Antonieta.git
cd Pindamonhangaba.Antonieta

# Inicie o banco de dados
docker-compose up -d

# O PostgreSQL estará disponível em:
# Host: localhost
# Porta: 5433
# Usuário: antonieta_usr
# Senha: antonieta_passd
# Database: antonieta_db
```

### Opção 2: Instalação Manual

#### Backend

```bash
# Navegue até a pasta do backend
cd Antonieta.Backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Execute as migrations
alembic upgrade head

# Crie o usuário administrador inicial
python create_admin_user.py

# Execute o SQL gerado no PostgreSQL:
# psql -U antonieta_usr -d antonieta_db -h localhost -p 5433 -f insert_admin_user.sql

# Inicie o servidor
uvicorn main:app --reload --port 8000
```

**Credenciais padrão do administrador:**
- Email: `admin@antonieta.com`
- Senha: `Admin@123`
- ⚠️ **IMPORTANTE:** Altere a senha após o primeiro login!

#### Frontend

```bash
# Navegue até a pasta do frontend
cd Antonieta.Frontend

# Instale as dependências
npm install

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env se necessário

# Inicie o servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em: http://localhost:3000

## 🗄️ Estrutura do Projeto

```
Pindamonhangaba.Antonieta/
├── Antonieta.Backend/     # API Backend
│   ├── alembic/           # Migrations do banco de dados
│   ├── controllers/       # Controladores da API (endpoints)
│   ├── models/            # Modelos do SQLAlchemy
│   ├── services/          # Lógica de negócio
│   ├── dtos/              # Data Transfer Objects
│   ├── database.py        # Configuração do banco
│   ├── main.py            # Arquivo principal da aplicação
│   ├── requirements.txt   # Dependências Python
│   └── create_admin_user.py  # Script para criar admin inicial
├── Antonieta.Frontend/    # Frontend Web
│   ├── components/        # Componentes Vue reutilizáveis
│   ├── pages/             # Páginas da aplicação
│   ├── services/          # Serviços de comunicação com API
│   ├── models/            # Tipos e modelos TypeScript
│   ├── layouts/           # Layouts da aplicação
│   ├── middleware/        # Middlewares de autenticação
│   ├── composables/       # Composables Vue (useAuth, etc)
│   └── nuxt.config.ts     # Configuração do Nuxt
├── Antonieta.Tests/       # Testes automatizados
│   ├── tests/             # Casos de teste E2E
│   ├── pages/             # Page Objects
│   └── playwright.config.ts  # Configuração do Playwright
├── docker-compose.yml     # Configuração Docker
└── readme.md              # Este arquivo
```

## 📦 Funcionalidades

### Gestão de Beneficiários
- ✅ Cadastro completo de beneficiários
- ✅ Pesquisa e filtros avançados
- ✅ Edição e exclusão de registros
- ✅ Histórico de distribuições por beneficiário

### Controle de Estoque
- ✅ Registro de entradas de ração
- ✅ Controle de estoque por tipo de ração
- ✅ Alertas de estoque baixo
- ✅ Relatório de movimentação

### Distribuições
- ✅ Registro de distribuição de rações
- ✅ Controle de quantidade por beneficiário
- ✅ Histórico completo de distribuições
- ✅ Validações de estoque automáticas

### Dashboard
- ✅ Métricas em tempo real
- ✅ Gráficos de distribuição
- ✅ Indicadores de estoque
- ✅ Resumo de beneficiários ativos

### Administração
- ✅ Gestão de usuários
- ✅ Controle de permissões (comum/administrador)
- ✅ Log de auditoria
- ✅ Autenticação JWT

### Relatórios
- ✅ Relatório de distribuições
- ✅ Relatório de beneficiários
- ✅ Exportação de dados
- ✅ Histórico de movimentações

## 🔐 Variáveis de Ambiente

### Backend (.env)
```env
# Banco de Dados
DATABASE_URL=postgresql://antonieta_usr:antonieta_passd@localhost:5433/antonieta_db

# JWT/Autenticação
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ambiente
ENVIRONMENT=development
```

### Frontend (.env)
```env
# URL da API
NUXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 🧪 Testes

O projeto inclui testes E2E usando Playwright:

```bash
cd Antonieta.Tests

# Instalar dependências
npm install

# Executar testes
npm test

# Executar com interface gráfica
npm run test:ui

# Relatório de testes
npm run test:report
```

## 📄 Documentação da API

A documentação interativa da API (Swagger) está disponível em:
- **Desenvolvimento:** http://localhost:8000/docs
- **Redoc:** http://localhost:8000/redoc
- **Produção:** https://api.pindamonhangaba.sp.gov.br/docs

### Principais Endpoints

#### Autenticação
- `POST /auth/token` - Login (retorna JWT)
- `GET /auth/me` - Dados do usuário autenticado
- `POST /auth/register` - Registro de novo usuário (apenas admin)

#### Beneficiários
- `GET /beneficiaries` - Lista beneficiários
- `POST /beneficiaries` - Cria beneficiário
- `GET /beneficiaries/{id}` - Detalhes do beneficiário
- `PUT /beneficiaries/{id}` - Atualiza beneficiário
- `DELETE /beneficiaries/{id}` - Remove beneficiário

#### Distribuições
- `GET /distributions` - Lista distribuições
- `POST /distributions` - Registra distribuição
- `GET /distributions/{id}` - Detalhes da distribuição

#### Estoque
- `GET /ration-stocks` - Lista estoque de rações
- `POST /ration-inputs` - Registra entrada de ração
- `GET /dashboard` - Métricas do dashboard

## 🚨 Troubleshooting

### Erro de conexão com banco de dados
```bash
# Verifique se o PostgreSQL está rodando
docker-compose ps

# Reinicie o container do banco
docker-compose restart db

# Verifique os logs
docker-compose logs db
```

### Erro nas migrations
```bash
cd Antonieta.Backend

# Reverter última migration
alembic downgrade -1

# Aplicar migrations novamente
alembic upgrade head

# Criar nova migration
alembic revision --autogenerate -m "descrição"
```

### Frontend não conecta ao backend
1. Verifique se o backend está rodando em `http://localhost:8000`
2. Confirme a variável `NUXT_PUBLIC_BACKEND_URL` no `.env`
3. Verifique CORS no backend (deve permitir `http://localhost:3000`)

### Menu de administração não aparece
Se após fazer login com um usuário administrador o menu não aparecer:
1. Limpe o cache do navegador (Ctrl+Shift+Delete)
2. Faça logout e login novamente
3. Verifique no console do navegador se há erros
4. Confirme que o role do usuário no banco é `'administrador'`

## 🎯 Roadmap

- [ ] Módulo de relatórios avançados
- [ ] Exportação para Excel/PDF
- [ ] Notificações por email
- [ ] App mobile
- [ ] API de integração com outros sistemas
- [ ] Dashboard analítico avançado
- [ ] Sistema de agendamento de distribuições

## 👥 Contribuindo

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- **Email:** abraao.moreira@pindamonhangaba.sp.gov.br
- **Departamento:** Secretaria de Tecnologia, Inovação e Projetos
- **Prefeitura:** Pindamonhangaba - SP

## ✨ Autores

* **Abraão Moreira** - *Analista de Tecnologia de Informação* - [GitHub](https://github.com/abraaom)

## 🙏 Agradecimentos

- Prefeitura Municipal de Pindamonhangaba
- Secretaria de Tecnologia, Inovação e Projetos
- Equipe do Projeto Antonieta
- Comunidade open source

---

<div align="center">
  
**Desenvolvido com ❤️ pelo Departamento de Sistemas**  
**Secretaria de Tecnologia, Inovação e Projetos**  
**Prefeitura de Pindamonhangaba © 2025**

</div>