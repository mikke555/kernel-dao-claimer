from typing import Optional

from pydantic import BaseModel


class Data(BaseModel):
    balance: str
    updatedAt: str
    proof: list[str]
    createdAt: str
    totalBalance: str
    isTop100User: bool
    user: str
    sk: str
    pk: str


class ProofResponse(BaseModel):
    data: Optional[Data] = None
    time: str
