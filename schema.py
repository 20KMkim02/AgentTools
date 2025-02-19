from pydantic import BaseModel
from .database import SessionLocal
from datetime import date
#Step 3 : Pydantic Model

#1Base
class CustomerBase(BaseModel):
    Name:str
    Telephone : str
    Before_cholesterol : int
    N_capsule:int
    Consistency:str
    Last_Check:date
    Update_cholesterol:int
    Routine_Health:str
    Eating_habit:str
    Cus_Instock:int
    Latest_buy:date
    Buy_Channels:str


#2Request
class ItemCreate(CustomerBase):
    pass

#3Response
class ItemResponse(CustomerBase):
    id : int
    class Config:
        from_attributes= True