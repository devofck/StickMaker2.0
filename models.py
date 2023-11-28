from pydantic import BaseModel, PositiveInt


class User(BaseModel):
    tg_id: PositiveInt
    status: PositiveInt
