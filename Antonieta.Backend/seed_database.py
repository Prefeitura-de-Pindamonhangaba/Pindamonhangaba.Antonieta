"""
Script para popular o banco de dados com dados de teste/desenvolvimento.

Uso:
    python seed_database.py
"""

from datetime import datetime, timedelta
from passlib.context import CryptContext
from database import get_db
import sys
import random

# Importar todos os modelos
import models.user_model
import models.ration_stock_model
import models.ration_input_model
import models.beneficiary_model
import models.distribution_model
import models.audit_log_model

from models.user_model import User
from models.ration_stock_model import RationStock
from models.ration_input_model import RationInput
from models.beneficiary_model import Beneficiary
from models.distribution_model import Distribution
from models.audit_log_model import AuditLog

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

def clear_database(db):
    """Limpa todas as tabelas (cuidado em produção!)"""
    print("🗑️  Limpando banco de dados...")
    
    # Ordem de deleção importa por causa das foreign keys
    db.query(AuditLog).delete()  # Primeiro deletar audit_logs
    db.query(Distribution).delete()
    db.query(RationInput).delete()
    db.query(Beneficiary).delete()
    db.query(RationStock).delete()
    db.query(User).delete()
    
    db.commit()
    print("✅ Banco de dados limpo!")

def create_users(db):
    """Cria usuários de teste"""
    print("\n👥 Criando usuários...")
    
    users = [
        {
            "email": "admin@antonieta.com",
            "password": "Admin@123",
            "full_name": "Administrador Sistema",
            "role": "administrador"
        },
        {
            "email": "usuario@antonieta.com",
            "password": "User@123",
            "full_name": "Usuário Comum",
            "role": "comum"
        }
    ]
    
    created_users = []
    for user_data in users:
        user = User(
            email=user_data["email"],
            hashed_password=pwd_context.hash(user_data["password"]),
            full_name=user_data["full_name"],
            role=user_data["role"]
        )
        db.add(user)
        created_users.append(user)
        print(f"  ✓ {user_data['full_name']} ({user_data['email']}) - Senha: {user_data['password']}")
    
    db.commit()
    print(f"✅ {len(created_users)} usuários criados!")
    return created_users

def create_ration_stocks(db, admin_user):
    """Cria tipos de ração"""
    print("\n🍖 Criando tipos de ração...")
    
    rations = [
        {
            "name": "Ração para Cães Adultos",
            "description": "Ração premium para cães adultos de todas as raças",
            "unit": "kg",
            "stock": 500.0
        },
        {
            "name": "Ração para Gatos Adultos",
            "description": "Ração premium para gatos adultos",
            "unit": "kg",
            "stock": 300.0
        },
        {
            "name": "Ração para Filhotes",
            "description": "Ração especial para filhotes de cães e gatos",
            "unit": "kg",
            "stock": 200.0
        }
    ]
    
    created_rations = []
    for ration_data in rations:
        ration = RationStock(
            name=ration_data["name"],
            description=ration_data["description"],
            unit=ration_data["unit"],
            stock=ration_data["stock"],
            created_by=admin_user.id
        )
        db.add(ration)
        created_rations.append(ration)
        print(f"  ✓ {ration_data['name']} - Estoque: {ration_data['stock']}{ration_data['unit']}")
    
    db.commit()
    print(f"✅ {len(created_rations)} tipos de ração criados!")
    return created_rations

def create_ration_inputs(db, rations, admin_user):
    """Cria entradas de ração"""
    print("\n📦 Criando entradas de ração...")
    
    created_inputs = []
    base_date = datetime.now() - timedelta(days=60)
    
    for i in range(10):
        ration = random.choice(rations)
        amount = random.uniform(50, 200)
        date = base_date + timedelta(days=random.randint(0, 50))
        
        ration_input = RationInput(
            ration_stock_id=ration.id,
            amount=amount,
            date=date,
            description=f"Doação recebida - Lote {i+1}",
            created_by=admin_user.id
        )
        db.add(ration_input)
        created_inputs.append(ration_input)
    
    db.commit()
    print(f"✅ {len(created_inputs)} entradas de ração criadas!")
    return created_inputs

def create_beneficiaries(db, admin_user):
    """Cria beneficiários de teste"""
    print("\n🧑‍🤝‍🧑 Criando beneficiários...")
    
    neighborhoods = ["Centro", "Vila Esperança", "Jardim das Flores", "Moreira César", "Alto do Cardoso"]
    streets = ["Rua das Acácias", "Avenida Principal", "Rua São José", "Rua dos Lírios", "Avenida Brasil"]
    
    # Beneficiários antigos (antes de hoje)
    old_beneficiaries = []
    for i in range(15):
        beneficiary = Beneficiary(
            name=f"Beneficiário Antigo {i+1}",
            document=f"000.000.00{i:02d}-00",
            street=random.choice(streets),
            number=str(random.randint(1, 999)),
            neighborhood=random.choice(neighborhoods),
            city="Pindamonhangaba",
            state="SP",
            contact=f"(12) 99999-{random.randint(1000, 9999)}",
            qtd_dogs=random.randint(1, 5),
            qtd_castred_dogs=random.randint(0, 3),
            qtd_cats=random.randint(0, 4),
            qtd_castred_cats=random.randint(0, 2),
            government_benefit=random.choice([True, False]),
            receives_basic_basket=random.choice([True, False]),
            old=True,  # Marcar como antigo
            created_by=admin_user.id,
            created_at=datetime.now() - timedelta(days=random.randint(30, 365))
        )
        db.add(beneficiary)
        old_beneficiaries.append(beneficiary)
    
    # Beneficiários novos (de hoje em diante)
    new_beneficiaries = []
    for i in range(10):
        beneficiary = Beneficiary(
            name=f"Beneficiário Novo {i+1}",
            document=f"111.111.11{i:02d}-11",
            street=random.choice(streets),
            number=str(random.randint(1, 999)),
            neighborhood=random.choice(neighborhoods),
            city="Pindamonhangaba",
            state="SP",
            contact=f"(12) 98888-{random.randint(1000, 9999)}",
            mother_name=f"Mãe do Beneficiário {i+1}",
            birth_date="1980-01-01",
            qtd_dogs=random.randint(1, 5),
            qtd_castred_dogs=random.randint(0, 3),
            qtd_cats=random.randint(0, 4),
            qtd_castred_cats=random.randint(0, 2),
            government_benefit=random.choice([True, False]),
            receives_basic_basket=random.choice([True, False]),
            cadunico_code=f"CU{random.randint(100000, 999999)}",
            income_range="Até 1/4 salário mínimo",
            old=False,  # Beneficiário ativo
            created_by=admin_user.id
        )
        db.add(beneficiary)
        new_beneficiaries.append(beneficiary)
    
    db.commit()
    print(f"  ✓ {len(old_beneficiaries)} beneficiários ANTIGOS (old=True)")
    print(f"  ✓ {len(new_beneficiaries)} beneficiários NOVOS (old=False)")
    print(f"✅ {len(old_beneficiaries) + len(new_beneficiaries)} beneficiários criados!")
    return old_beneficiaries, new_beneficiaries

def create_distributions(db, rations, old_beneficiaries, new_beneficiaries, admin_user):
    """Cria distribuições de ração"""
    print("\n📋 Criando distribuições...")
    
    # Distribuições antigas (para beneficiários antigos)
    old_distributions = []
    for beneficiary in old_beneficiaries[:10]:  # Alguns beneficiários antigos receberam ração
        for _ in range(random.randint(1, 3)):
            ration = random.choice(rations)
            amount = random.uniform(5, 20)
            date = datetime.now() - timedelta(days=random.randint(30, 365))
            
            distribution = Distribution(
                ration_id=ration.id,
                beneficiary_id=beneficiary.id,
                amount=amount,
                date=date,
                observations="Distribuição realizada antes do corte",
                old=True,  # Distribuição antiga
                created_by=admin_user.id,
                created_at=date
            )
            db.add(distribution)
            old_distributions.append(distribution)
            
            # Atualizar estoque
            ration.stock -= amount
    
    # Distribuições novas (para beneficiários novos)
    new_distributions = []
    for beneficiary in new_beneficiaries[:7]:  # Alguns beneficiários novos já receberam
        for _ in range(random.randint(1, 2)):
            ration = random.choice(rations)
            amount = random.uniform(5, 15)
            date = datetime.now() - timedelta(hours=random.randint(1, 12))
            
            distribution = Distribution(
                ration_id=ration.id,
                beneficiary_id=beneficiary.id,
                amount=amount,
                date=date,
                observations="Distribuição atual",
                old=False,  # Distribuição ativa
                created_by=admin_user.id
            )
            db.add(distribution)
            new_distributions.append(distribution)
            
            # Atualizar estoque
            ration.stock -= amount
    
    db.commit()
    print(f"  ✓ {len(old_distributions)} distribuições ANTIGAS (old=True)")
    print(f"  ✓ {len(new_distributions)} distribuições NOVAS (old=False)")
    print(f"✅ {len(old_distributions) + len(new_distributions)} distribuições criadas!")
    return old_distributions, new_distributions

def main():
    """Função principal"""
    print("=" * 60)
    print("🌱 Script de População do Banco de Dados")
    print("=" * 60)
    print("⚠️  ATENÇÃO: Este script irá LIMPAR todos os dados existentes!")
    print("=" * 60)
    
    response = input("\n❓ Deseja continuar? (sim/não): ")
    
    if response.lower() not in ['sim', 's', 'yes', 'y']:
        print("❌ Operação cancelada pelo usuário.")
        return
    
    db = next(get_db())
    
    try:
        # Limpar banco
        clear_database(db)
        
        # Criar dados
        users = create_users(db)
        admin_user = users[0]  # Primeiro usuário é admin
        
        rations = create_ration_stocks(db, admin_user)
        create_ration_inputs(db, rations, admin_user)
        
        old_beneficiaries, new_beneficiaries = create_beneficiaries(db, admin_user)
        old_distributions, new_distributions = create_distributions(
            db, rations, old_beneficiaries, new_beneficiaries, admin_user
        )
        
        print("\n" + "=" * 60)
        print("✅ BANCO DE DADOS POPULADO COM SUCESSO!")
        print("=" * 60)
        print("\n📊 Resumo:")
        print(f"  👥 Usuários: {len(users)}")
        print(f"  🍖 Tipos de ração: {len(rations)}")
        print(f"  🧑‍🤝‍🧑 Beneficiários: {len(old_beneficiaries) + len(new_beneficiaries)}")
        print(f"      • Antigos (old=True): {len(old_beneficiaries)}")
        print(f"      • Novos (old=False): {len(new_beneficiaries)}")
        print(f"  📋 Distribuições: {len(old_distributions) + len(new_distributions)}")
        print(f"      • Antigas (old=True): {len(old_distributions)}")
        print(f"      • Novas (old=False): {len(new_distributions)}")
        
        print("\n🔑 Credenciais de Acesso:")
        print("  Admin:")
        print("    Email: admin@antonieta.com")
        print("    Senha: Admin@123")
        print("  Usuário Comum:")
        print("    Email: usuario@antonieta.com")
        print("    Senha: User@123")
        
        print("\n💡 Dica: Os registros marcados como 'old=True' não aparecerão")
        print("   nas listagens normais, mas continuam no banco de dados.")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao popular banco: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
