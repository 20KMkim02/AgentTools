from typing import List,Optional
from fastapi import FastAPI ,Depends , HTTPException ,Query
from sqlalchemy.orm import Session 

from .schema import ItemResponse,CustomerBase
from .database import get_db, engine, Base
from .model import CustomerDB


#Sync Schema -> สร้างฐานข้อมูล เทียบclass ORM กับ Database ถ้าตัวไหนหายไปจะได้สร้างรองรับไว้ก่อน
Base.metadata.create_all(bind=engine)

app =FastAPI()

#---------------------------------------------------------------------------

@app.post('/post_customer',response_model=ItemResponse)
def create_Cust(item:CustomerBase,db:Session= Depends(get_db)):
    db_item= CustomerDB(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    print(db_item)
    return db_item

@app.get("/get_customer/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(CustomerDB).filter(CustomerDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.delete("/delete_customer/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(CustomerDB).filter(CustomerDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}

