from pydantic import BaseModel, ConfigDict


class InformacaoTecnica(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    valor: str
