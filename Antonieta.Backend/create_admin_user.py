"""
Script para gerar SQL de criação do usuário administrador inicial.
Execute este script para gerar o SQL com a senha hasheada.
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

# Defina as credenciais do usuário administrador inicial
email = "admin@antonieta.com"
senha = "Admin@123"  # ALTERE ESTA SENHA!
nome_completo = "Administrador"
role = "administrador"

# Gera o hash da senha
hashed_password = pwd_context.hash(senha)

# Gera o SQL
sql = f"""
-- Script para criar usuário administrador inicial
-- Email: {email}
-- Senha: {senha} (ALTERE APÓS O PRIMEIRO LOGIN!)

INSERT INTO users (email, hashed_password, full_name, role, created_at, updated_at)
VALUES (
    '{email}',
    '{hashed_password}',
    '{nome_completo}',
    '{role}',
    NOW(),
    NOW()
);
"""

print(sql)
print("\n" + "="*80)
print("IMPORTANTE: Execute o SQL acima no seu banco de dados PostgreSQL")
print(f"Login: {email}")
print(f"Senha: {senha}")
print("ALTERE A SENHA APÓS O PRIMEIRO LOGIN!")
print("="*80)

# Também salva em um arquivo
with open('insert_admin_user.sql', 'w', encoding='utf-8') as f:
    f.write(sql)

print("\nArquivo 'insert_admin_user.sql' criado com sucesso!")
