from pydantic import BaseModel

class update_beneficiary_dto(BaseModel):
    """
    Data Transfer Object (DTO) para atualizar um beneficiário.
    """
    id: int
    name: str
    document: str
    address: str
    contact: str
    monthly_limit: int  # Add monthly_limit field
    mother_name: str = None  # Optional field for mother's name
    birth_date: str = None  # Optional field for birth date
    qtd_dogs: int = 0  # Optional field for quantity of dogs
    qtd_castred_dogs: int = 0  # Optional field for quantity of castrated dogs
    qtd_cats: int = 0  # Optional field for quantity of cats
    qtd_castred_cats: int = 0  # Optional field for quantity of castrated cats
    government_benefit: bool = False  # Optional field for government benefit status
    receives_basic_basket: bool = False  # Optional field for basic basket receipt status
    how_did_you_hear: str = None  # Optional field for how they heard about the program
    observations: str = None  # Optional field for additional observations