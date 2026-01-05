"""
Script para marcar registros antigos (anteriores a 2026-01-05) como old=True.
Este script deve ser executado após aplicar a migração de banco de dados.

Uso:
    python mark_old_records.py
"""

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db, engine
import sys

# Importar todos os modelos para evitar problemas de referência circular
import models.user_model
import models.ration_stock_model
import models.ration_input_model
import models.beneficiary_model
import models.distribution_model
import models.audit_log_model

from models.beneficiary_model import Beneficiary
from models.distribution_model import Distribution

# Data de corte: 5 de janeiro de 2026
CUTOFF_DATE = datetime(2026, 1, 5, 0, 0, 0)

def mark_old_records():
    """Marca todos os beneficiários e distribuições anteriores à data de corte como old=True"""
    
    db = next(get_db())
    
    try:
        # Contar registros antes da atualização
        total_beneficiaries = db.query(Beneficiary).filter(
            Beneficiary.created_at < CUTOFF_DATE
        ).count()
        
        total_distributions = db.query(Distribution).filter(
            Distribution.created_at < CUTOFF_DATE
        ).count()
        
        print(f"\n📊 Estatísticas:")
        print(f"  - Beneficiários a serem marcados como antigos: {total_beneficiaries}")
        print(f"  - Distribuições a serem marcadas como antigas: {total_distributions}")
        
        # Confirmação do usuário
        response = input("\n⚠️  Deseja continuar com a marcação destes registros? (sim/não): ")
        
        if response.lower() not in ['sim', 's', 'yes', 'y']:
            print("❌ Operação cancelada pelo usuário.")
            return
        
        print("\n🔄 Marcando registros antigos...")
        
        # Marcar beneficiários antigos
        beneficiaries_updated = db.query(Beneficiary).filter(
            Beneficiary.created_at < CUTOFF_DATE
        ).update({"old": True}, synchronize_session=False)
        
        # Marcar distribuições antigas
        distributions_updated = db.query(Distribution).filter(
            Distribution.created_at < CUTOFF_DATE
        ).update({"old": True}, synchronize_session=False)
        
        # Commit das alterações
        db.commit()
        
        print(f"\n✅ Operação concluída com sucesso!")
        print(f"  - Beneficiários marcados: {beneficiaries_updated}")
        print(f"  - Distribuições marcadas: {distributions_updated}")
        
        # Estatísticas finais
        active_beneficiaries = db.query(Beneficiary).filter(Beneficiary.old == False).count()
        old_beneficiaries = db.query(Beneficiary).filter(Beneficiary.old == True).count()
        
        active_distributions = db.query(Distribution).filter(Distribution.old == False).count()
        old_distributions = db.query(Distribution).filter(Distribution.old == True).count()
        
        print(f"\n📈 Estatísticas finais:")
        print(f"  Beneficiários:")
        print(f"    - Ativos: {active_beneficiaries}")
        print(f"    - Antigos: {old_beneficiaries}")
        print(f"  Distribuições:")
        print(f"    - Ativas: {active_distributions}")
        print(f"    - Antigas: {old_distributions}")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao marcar registros: {str(e)}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🗄️  Script de Marcação de Registros Antigos")
    print("=" * 60)
    print(f"📅 Data de corte: {CUTOFF_DATE.strftime('%d/%m/%Y')}")
    print(f"📌 Registros anteriores a esta data serão marcados como antigos")
    print("=" * 60)
    
    mark_old_records()
