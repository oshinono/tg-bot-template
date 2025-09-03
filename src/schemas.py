from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class BaseOut(BaseSchema):
    pass


class BaseCreate(BaseSchema):
    pass


class BaseUpdate(BaseSchema):
    pass
