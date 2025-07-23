from fastapi import APIRouter, HTTPException, status
import logging
from services.beneficiary_services import (
    get_all_beneficiaries_service, 
    get_beneficiary_by_id_service, 
    create_beneficiary_service, 
    update_beneficiary_service, 
    delete_beneficiary_service
)
from dtos.update_beneficiary_dto import update_beneficiary_dto
from dtos.create_beneficiary_dto import create_beneficiary_dto
from sqlalchemy.exc import IntegrityError

# Configurar logger específico para o controller
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/beneficiary", tags=["Beneficiary"])

@router.get("/")
async def get_all_beneficiaries():
    """
    Retorna todos os beneficiários cadastrados
    """
    try:
        logger.info("Iniciando busca de todos os beneficiários")
        result = await get_all_beneficiaries_service()
        logger.info(f"Busca concluída. Encontrados {len(result[0])} beneficiários")
        return result
    except Exception as e:
        logger.error(f"Erro ao buscar beneficiários: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao buscar beneficiários"
        )

@router.get("/{beneficiary_id}")
async def get_beneficiary_by_id(beneficiary_id: int):
    """
    Retorna um beneficiário específico pelo ID
    """
    try:
        logger.info(f"Buscando beneficiário com ID: {beneficiary_id}")
        beneficiary = await get_beneficiary_by_id_service(beneficiary_id=beneficiary_id)
        
        if not beneficiary:
            logger.warning(f"Beneficiário com ID {beneficiary_id} não encontrado")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Beneficiário com ID {beneficiary_id} não encontrado"
            )
        
        logger.info(f"Beneficiário encontrado: {beneficiary.name}")
        return beneficiary
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar beneficiário ID {beneficiary_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao buscar beneficiário"
        )

@router.post("/")
async def create_beneficiary(beneficiary_dto: create_beneficiary_dto):
    """
    Cria um novo beneficiário
    """
    try:
        logger.info(f"Iniciando criação de novo beneficiário: {beneficiary_dto.name}")
        logger.debug(f"Dados recebidos: {beneficiary_dto.model_dump_json()}")
        
        new_beneficiary = await create_beneficiary_service(beneficiary_dto=beneficiary_dto)
        
        logger.info(f"Beneficiário criado com sucesso - ID: {new_beneficiary.id}, Nome: {new_beneficiary.name}")
        return new_beneficiary
        
    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao criar beneficiário {beneficiary_dto.name}: {str(e)}")
        if "document" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um beneficiário cadastrado com este documento"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados duplicados ou inválidos"
            )
    except ValueError as e:
        logger.warning(f"Dados inválidos para beneficiário {beneficiary_dto.name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Dados inválidos: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Erro inesperado ao criar beneficiário {beneficiary_dto.name}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao criar beneficiário"
        )

@router.put("/")
async def update_beneficiary(beneficiary_dto: update_beneficiary_dto):
    """
    Atualiza um beneficiário existente
    """
    try:
        logger.info(f"Iniciando atualização do beneficiário ID: {beneficiary_dto.id}")
        logger.debug(f"Dados recebidos: {beneficiary_dto.model_dump_json()}")
        
        updated_beneficiary = await update_beneficiary_service(beneficiary_dto=beneficiary_dto)
        
        if not updated_beneficiary:
            logger.warning(f"Beneficiário com ID {beneficiary_dto.id} não encontrado para atualização")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Beneficiário com ID {beneficiary_dto.id} não encontrado"
            )
        
        logger.info(f"Beneficiário atualizado com sucesso - ID: {updated_beneficiary.id}, Nome: {updated_beneficiary.name}")
        return updated_beneficiary
        
    except HTTPException:
        raise
    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao atualizar beneficiário ID {beneficiary_dto.id}: {str(e)}")
        if "document" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe outro beneficiário cadastrado com este documento"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados duplicados ou inválidos"
            )
    except ValueError as e:
        logger.warning(f"Dados inválidos para atualização do beneficiário ID {beneficiary_dto.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Dados inválidos: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar beneficiário ID {beneficiary_dto.id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao atualizar beneficiário"
        )

@router.delete("/{beneficiary_id}")
async def delete_beneficiary(beneficiary_id: int):
    """
    Deleta um beneficiário
    """
    try:
        logger.info(f"Iniciando deleção do beneficiário ID: {beneficiary_id}")
        
        success = await delete_beneficiary_service(beneficiary_id=beneficiary_id)
        
        if not success:
            logger.warning(f"Beneficiário com ID {beneficiary_id} não encontrado para deleção")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Beneficiário com ID {beneficiary_id} não encontrado"
            )
        
        logger.info(f"Beneficiário ID {beneficiary_id} deletado com sucesso")
        return {"message": "Beneficiário deletado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao deletar beneficiário ID {beneficiary_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao deletar beneficiário"
        )