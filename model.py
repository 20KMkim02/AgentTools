from .database import Base
from sqlalchemy import Column , Integer , String ,Date

# Step 2 : ORM Class
class CustomerDB(Base):
    __tablename__='Customer'
    id=Column(Integer,primary_key=True)
    Name=Column(String,index=True)
    Telephone=Column(String(10),index=True)
    Before_cholesterol=Column(Integer,index=True)
    N_capsule=Column(Integer,index=True)
    Consistency=Column(String,index=True)
    Last_Check=Column(Date,index=True)
    Update_cholesterol=Column(Integer,index=True)
    Routine_Health=Column(String,index=True)
    Eating_habit=Column(String,index=True)
    Cus_Instock=Column(Integer,index=True)
    Latest_buy=Column(Date,index=True)
    Buy_Channels=Column(String,index=True)
