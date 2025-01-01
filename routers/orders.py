from fastapi import APIRouter, HTTPException
from home.database import client
from home.utils import execute_query
from models.pydanticmodels import OrderCreate

router = APIRouter(prefix="/orders")

@router.get("/", response_model=list[OrderCreate])
async def get_orders():
    query = """
        SELECT order_id, order_date, customer_name, state, city 
        FROM `boreal-pride-319909.sales_data.orders`
    """
    try:
        results = execute_query(client, query)
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {e}")
    
@router.get("/details")
async def get_order_details():
    query = """
        SELECT order_id, amount, profit, quantity, category, sub_category 
        FROM `boreal-pride-319909.sales_data.order_details`
    """
    try:
        results = execute_query(client, query)
        return {"data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {e}")

@router.post("/", response_model=OrderCreate)
async def create_order(order: OrderCreate):
    query = f"""
        INSERT INTO `boreal-pride-319909.sales_data.orders` 
        (order_id, order_date, customer_name, state, city)
        VALUES ('{order.order_id}', '{order.order_date}', 
                '{order.customer_name}', '{order.state}', '{order.city}')
    """
    try:
        execute_query(client, query)
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {e}")
