<div align="center">
  <img src=".\Antonieta.Frontend\assets\Antonieta logotipo-02.svg" alt="Projeto Antonieta Banner" width="100%">
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

### Backend

```bash
# Clone o repositório
cd Antonieta.Backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
.\venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
copy .env.example .env

# Execute as migrations
alembic upgrade head

# Inicie o servidor
uvicorn main:app --reload
```

### Frontend

```bash
# Navegue até a pasta do frontend
cd Antonieta.Frontend

# Instale as dependências
npm install

# Configure as variáveis de ambiente
copy .env.example .env

# Inicie o servidor de desenvolvimento
npm run dev
```

## 🗄️ Estrutura do Projeto

### Backend
```
Antonieta.Backend/
├── alembic/            # Migrations
├── controllers/        # Controladores da API
├── models/            # Modelos do banco de dados
├── services/          # Lógica de negócio
├── schemas/           # Schemas de validação
└── main.py           # Arquivo principal
```

### Frontend
```
Antonieta.Frontend/
├── components/        # Componentes Vue
├── pages/            # Páginas da aplicação
├── services/         # Serviços de API
├── models/           # Tipos TypeScript
└── layouts/          # Layouts da aplicação
```

## 📦 Funcionalidades

- Gestão de beneficiários
- Controle de estoque de rações
- Registro de entradas de ração
- Distribuição de rações
- Dashboard com métricas
- Autenticação e autorização
- Relatórios de distribuição

## 🔐 Variáveis de Ambiente

### Backend
```env
DATABASE_URL=postgresql://user:password@localhost:5432/antonieta
SECRET_KEY=your-secret-key
```

### Frontend
```env
NUXT_PUBLIC_BACKEND_URL=https://api.pindamonhangaba.sp.gov.br
```

## 📄 Documentação da API

A documentação da API está disponível em:
- Desenvolvimento: http://localhost:8000/docs
- Produção: https://api.pindamonhangaba.sp.gov.br/docs

## 👥 Contribuindo

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença [MIT](LICENSE).

## ✨ Autores

* **Abraão Moreira** - *Analista de Tecnologia de Informação* - [GitHub](https://github.com/abraaom)

---
Desenvolvido pelo Departamento de Sistemas - Secretaria de Tecnologia, Inovação e Projetos - Prefeitura de Pindamonhangaba © 2025