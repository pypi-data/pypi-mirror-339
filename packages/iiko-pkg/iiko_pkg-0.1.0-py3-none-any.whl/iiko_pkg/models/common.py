"""
Common models for iiko.services API
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class Coordinates(BaseModel):
    """Coordinates model"""
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")


class Address(BaseModel):
    """Address model"""
    city: Optional[str] = Field(None, description="City")
    street: Optional[str] = Field(None, description="Street")
    house: Optional[str] = Field(None, description="House number")
    building: Optional[str] = Field(None, description="Building")
    apartment: Optional[str] = Field(None, description="Apartment")
    entrance: Optional[str] = Field(None, description="Entrance")
    floor: Optional[str] = Field(None, description="Floor")
    comment: Optional[str] = Field(None, description="Comment")
    coordinates: Optional[Coordinates] = Field(None, description="Coordinates")


class Customer(BaseModel):
    """Customer model"""
    id: Optional[str] = Field(None, description="Customer ID")
    name: Optional[str] = Field(None, description="Customer name")
    surname: Optional[str] = Field(None, description="Customer surname")
    comment: Optional[str] = Field(None, description="Comment")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email")
    birthday: Optional[str] = Field(None, description="Birthday")
    gender: Optional[str] = Field(None, description="Gender")
    address: Optional[Address] = Field(None, description="Address")


class ErrorInfo(BaseModel):
    """Error information model"""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    description: Optional[str] = Field(None, description="Error description")
    additional_data: Optional[Dict[str, Any]] = Field(None, description="Additional data")
