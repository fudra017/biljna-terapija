#### schemas/biljka.py

from pydantic import BaseModel
from pydantic.config import ConfigDict

from pydantic import BaseModel

class BiljkaBase(BaseModel):
    naziv: str
    opis: str | None = None

class BiljkaCreate(BiljkaBase):
    pass

class BiljkaOut(BiljkaBase):
    id: int

#    class Config:
#        from_attributes = True

    class Config:
        model_config = ConfigDict(from_attributes=True)

