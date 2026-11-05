from fastapi import APIRouter, Depends, HTTPException, Query
from decimal import Decimal
from typing import Dict, Any
from app.services.cache import get_revenue_summary
from app.core.auth import authenticate_request as get_current_user

router = APIRouter()

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    property_id: str,
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=1, le=9998),
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    if (month is None) != (year is None):
        raise HTTPException(status_code=422, detail="Provide both month and year, or neither for all-time revenue")

    tenant_id = getattr(current_user, "tenant_id", "default_tenant") or "default_tenant"
    
    revenue_data = await get_revenue_summary(property_id, tenant_id, month, year)
    
    total_revenue = int(Decimal(revenue_data['total']) * 1000)
    
    return {
        "property_id": revenue_data['property_id'],
        "total_revenue": total_revenue,
        "currency": revenue_data['currency'],
        "reservations_count": revenue_data['count']
    }
