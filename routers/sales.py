from fastapi import APIRouter, HTTPException
from home.database import client
from home.utils import execute_query
from models.pydanticmodels import SalesTargetCreate


router = APIRouter(prefix="/sales")

@router.get("/", response_model=list[SalesTargetCreate])
async def get_sales_targets():
    query = """
        SELECT month, category, target 
        FROM `boreal-pride-319909.sales_data.sales_targets`
    """
    try:
        results = execute_query(client, query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sales targets: {e}")

@router.post("/", response_model=SalesTargetCreate)
async def create_sales_target(sales_target: SalesTargetCreate):
    query = f"""
        INSERT INTO `boreal-pride-319909.sales_data.sales_targets` 
        (month, category, target)
        VALUES ('{sales_target.month}', 
                '{sales_target.category}', {sales_target.target})
    """
    try:
        execute_query(client, query)
        return sales_target
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating sales target: {e}")
