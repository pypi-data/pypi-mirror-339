"""
Organization models for iiko.services API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Organization(BaseModel):
    """Organization model"""
    id: str = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    country: Optional[str] = Field(None, description="Country")
    restaurant_address: Optional[str] = Field(None, description="Restaurant address")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    use_uae_addressing_system: Optional[bool] = Field(None, description="Use UAE addressing system")
    version: Optional[str] = Field(None, description="Version")
    currency: Optional[str] = Field(None, description="Currency")
    timezone: Optional[str] = Field(None, description="Timezone")
    default_delivery_terminal_id: Optional[str] = Field(None, description="Default delivery terminal ID")
    default_courier_id: Optional[str] = Field(None, description="Default courier ID")
    is_active: Optional[bool] = Field(None, description="Is active")
    is_delivery_enabled: Optional[bool] = Field(None, description="Is delivery enabled")
    is_draft_order_enabled: Optional[bool] = Field(None, description="Is draft order enabled")
    is_pickup_enabled: Optional[bool] = Field(None, description="Is pickup enabled")
    is_table_service_enabled: Optional[bool] = Field(None, description="Is table service enabled")
    external_revision: Optional[str] = Field(None, description="External revision")
    additional_info: Optional[Dict[str, Any]] = Field(None, description="Additional info")


class OrganizationsRequest(BaseModel):
    """Request model for organizations"""
    return_additional_info: Optional[bool] = Field(False, description="Return additional info")
    include_disabled: Optional[bool] = Field(False, description="Include disabled organizations")


class OrganizationsResponse(BaseModel):
    """Response model for organizations"""
    organizations: List[Organization] = Field(..., description="Organizations")
