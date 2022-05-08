import uuid
from abc import ABC
from typing import Optional

from pydantic import BaseModel, ConfigError
from sqlalchemy.orm import registry


mapper_registry = registry()
BaseOrmModel = mapper_registry.generate_base()


class BaseDomainModel(BaseModel, ABC):
    class Config:
        orm_mode: bool = False
        orm_model: Optional[BaseOrmModel] = None

    def to_orm(self):
        config = self.Config()
        if config.orm_mode is False or config.orm_model is None:
            raise ConfigError(
                "You must have the config attribute orm_mode=True to use to_orm"
            )
        data = dict(self)
        for key, value in data.items():
            if type(value) == uuid.UUID:
                data[key] = str(value)
            elif isinstance(value, BaseDomainModel):
                data[key] = value.to_orm()
            elif isinstance(value, list):
                data[key] = [
                    v.to_orm() for v in value if isinstance(v, BaseDomainModel)
                ]

        return config.orm_model(**data)


class BaseDtoModel(BaseModel, ABC):
    pass
