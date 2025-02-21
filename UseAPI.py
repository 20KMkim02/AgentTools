class CustomerBase(BaseModel):
    Name: str
    Telephone: str
    Before_cholesterol: int
    N_capsule: int
    Consistency: str
    Last_Check: str
    Update_cholesterol: int
    Routine_Health: str
    Eating_habit: str
    Cus_Instock: int
    Latest_buy: str
    Buy_Channels: str
    
@app.post("/tool/post_customer")
async def create_or_update_customer(item: CustomerBase):
    client = motor_client
    db = client["pcc_db"]
    collection = db["customers"]
    existing_customer = await collection.find_one({"Telephone": item.Telephone})
    if existing_customer:
        await collection.update_one({"Telephone": item.Telephone}, {"$set": item.dict()})
        return {"message": "Customer updated successfully", "customer": item}
    else:
        await collection.insert_one(item.dict())
        return {"message": "New customer added", "customer": item}
{
  "tools": [
    {
      "name": "post_customer",
      "description": "Tool สำหรับสร้างหรืออัปเดตข้อมูลลูกค้าในระบบฐานข้อมูล MongoDB",
      "parameters": [
        {
          "name": "Name",
          "description": "Customer's full name",
          "type": "string",
          "enum": null,
          "array_item": null
        },
        {
          "name": "Telephone",
          "description": "Customer's telephone number (unique identifier)",
          "type": "string",
          "enum": null,
          "array_item": null
        },
        {
          "name": "Before_cholesterol",
          "description": "Customer's cholesterol level before taking capsules",
          "type": "integer",
          "enum": null,
          "array_item": null
        },
        {
          "name": "N_capsule",
          "description": "Number of capsules taken",
          "type": "integer",
          "enum": null,
          "array_item": null
        },
        {
          "name": "Consistency",
          "description": "Customer's consistency in taking capsules",
          "type": "string",
          "enum": null,
          "array_item": null
        },
        {
          "name": "Last_Check",
          "description": "Date of the last cholesterol check (yyyy-mm-dd format)",
          "type": "string",
          "enum": null,
          "array_item": null
        },
        {
          "name": "Update_cholesterol",
          "description": "Latest updated cholesterol level",
          "type": "integer",
          "enum": null,
          "array_item": null
        },
        {
          "name": "Routine_Health",
          "description": "Health routine of the customer",
          "type": "string",
          "enum": null,
          "array_item": null
        },
        {
          "name": "Eating_habit",
          "description": "Customer's eating habits",
          "type": "string",
          "enum": null,
          "array_item": null
        },
        {
          "name": "Cus_Instock",
          "description": "Customer's remaining capsule stock",
          "type": "integer",
          "enum": null,
          "array_item": null
        },
        {
          "name": "Latest_buy",
          "description": "Date of the latest capsule purchase (yyyy-mm-dd format)",
          "type": "string",
          "enum": null,
          "array_item": null
        },
        {
          "name": "Buy_Channels",
          "description": "Purchase channels used by the customer",
          "type": "string",
          "enum": null,
          "array_item": null
        }
      ],
      "required": [
        "Name",
        "Telephone",
        "Before_cholesterol",
        "N_capsule",
        "Consistency",
        "Last_Check",
        "Update_cholesterol",
        "Routine_Health",
        "Eating_habit",
        "Cus_Instock",
        "Latest_buy",
        "Buy_Channels"
      ],
      "endpoint": "http://3.1.190.223:8000/tool/post_customer",
      "method": "POST"
    }
  ]
}

@app.get("/tool/get_customer")
async def get_init_user(telephone: str):
    client = motor_client
    db = client["pcc_db"]
    collection = db["customers"]
    customer = await collection.find_one({"Telephone": telephone})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer["_id"] = str(customer["_id"])
    return customer

import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
@app.get("/tool/Aproximate_usage")
async def Aproximate_usage(Latest_buy,Cus_Instock,Current_Date):
    """ช่วยในการคำนวนการบริโภคของลูกค้า จากการคิดCurrent Date difference"""
    try:
        Latest_buy_obj = datetime.strptime(Latest_buy, "%d/%m/%Y").date()
        diff = relativedelta(Current_Date, Latest_buy_obj) 
        months_diff = diff.years * 12 + diff.months
        if months_diff < 2:
            return 'ลูกค้ามีสินค้าคงคลังอยู่'
        if months_diff >= 2 or Cus_Instock <= 4:
            return 'ลูกค้ามีจำนวนคงคลังน้อยกว่า 1 เดือนแล้ว แนะนำโปรโมชั่น'
        else:
            return 'ลูกค้ามีสินค้าคงคลังอยู่'
    except Exception as e:
        print("Error in date processing:", str(e))
        return "เกิดข้อผิดพลาดในการคำนวณ"
    
@app.get("/tool/promotion")
async def get_promotion():
    return 'ซื้อ 3 แถม 2! ซื้อ 5 ลดทันที 50%! แคปซูลลดโคเลสเตอรอล ลดไขมันในเลือด ปรับสมดุลสุขภาพ ลดความเสี่ยงโรคหัวใจ รีบสั่งซื้อเลย!'

@app.get("/tool/capsule_day")
async def calculate_capsule_day(Update_cholesterol:int):
    if Update_cholesterol >300 :
        return 'ค่าคลอเลสเตอร์รอลของคุณ(ชื่อลูกค้า) อยู่ที่ (Update_cholesterol) ซึ่งอยู่ในเกณฑ์มีความเสี่ยงสูง ขอแนะนำให้รับประทานแคปซูล 6เม็ดต่อวัน แบ่งเป็น เช้า3 เย็น3เม็ด ค่ะ'
    if Update_cholesterol >200 :
        return 'ค่าคลอเลสเตอร์รอลของคุณ(ชื่อลูกค้า) อยู่ที่ (Update_cholesterol) ซึ่งอยู่ในเกณฑ์มีความเสี่ยงกลาง ขอแนะนำให้รับประทานแคปซูล 4เม็ดต่อวัน แบ่งเป็น เช้า2 เย็น2เม็ด ค่ะ'
    if Update_cholesterol <=200 :
        return 'ค่าคลอเลสเตอร์รอลของคุณ(ชื่อลูกค้า) อยู่ที่ (Update_cholesterol) ซึ่งอยู่ในเกณฑ์มีความเสี่ยงต่ำ ขอแนะนำให้รับประทานแคปซูล 2เม็ดต่อวัน แบ่งเป็น เช้า1 เย็น1เม็ด ค่ะ'