
-- Script para criar usuário administrador inicial
-- Email: admin@antonieta.com
-- Senha: Admin@123 (ALTERE APÓS O PRIMEIRO LOGIN!)

INSERT INTO users (email, hashed_password, full_name, role, created_at, updated_at)
VALUES (
    'admin@antonieta.com',
    '$2b$12$cgscbBp/OF5kj/mb.uC2beSBOnDigc1iC1BHFXslrRFa6gTX725W.',
    'Administrador',
    'administrador',
    NOW(),
    NOW()
);
