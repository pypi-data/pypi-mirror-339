"""
Menu models for iiko.services API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class ProductSize(BaseModel):
    """Product size model"""
    id: str = Field(..., description="Size ID")
    name: str = Field(..., description="Size name")
    priority: int = Field(..., description="Priority")
    is_default: bool = Field(..., description="Is default size")


class ProductModifier(BaseModel):
    """Product modifier model"""
    id: str = Field(..., description="Modifier ID")
    group_id: str = Field(..., description="Group ID")
    name: str = Field(..., description="Modifier name")
    description: Optional[str] = Field(None, description="Description")
    price: float = Field(..., description="Price")
    max_amount: int = Field(..., description="Maximum amount")
    min_amount: int = Field(..., description="Minimum amount")
    default_amount: int = Field(..., description="Default amount")
    product_id: Optional[str] = Field(None, description="Product ID")
    is_deleted: bool = Field(..., description="Is deleted")
    is_hidden: bool = Field(..., description="Is hidden")
    is_required: bool = Field(..., description="Is required")
    is_multiple_choice: bool = Field(..., description="Is multiple choice")
    is_splittable: bool = Field(..., description="Is splittable")
    modifier_type: str = Field(..., description="Modifier type")


class ProductGroup(BaseModel):
    """Product group model"""
    id: str = Field(..., description="Group ID")
    name: str = Field(..., description="Group name")
    description: Optional[str] = Field(None, description="Description")
    is_deleted: bool = Field(..., description="Is deleted")
    is_hidden: bool = Field(..., description="Is hidden")
    is_included_in_menu: bool = Field(..., description="Is included in menu")
    is_group_modifier: bool = Field(..., description="Is group modifier")
    modifiers: Optional[List[ProductModifier]] = Field(None, description="Modifiers")


class Product(BaseModel):
    """Product model"""
    id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Description")
    additional_info: Optional[str] = Field(None, description="Additional info")
    code: Optional[str] = Field(None, description="Code")
    article_number: Optional[str] = Field(None, description="Article number")
    price: float = Field(..., description="Price")
    category_id: str = Field(..., description="Category ID")
    is_deleted: bool = Field(..., description="Is deleted")
    is_hidden: bool = Field(..., description="Is hidden")
    is_included_in_menu: bool = Field(..., description="Is included in menu")
    order: int = Field(..., description="Order")
    tags: Optional[List[str]] = Field(None, description="Tags")
    sizes: Optional[List[ProductSize]] = Field(None, description="Sizes")
    modifiers: Optional[List[ProductModifier]] = Field(None, description="Modifiers")
    modifier_groups: Optional[List[ProductGroup]] = Field(None, description="Modifier groups")
    image_urls: Optional[List[str]] = Field(None, description="Image URLs")
    weight: Optional[float] = Field(None, description="Weight")
    measure_unit: Optional[str] = Field(None, description="Measure unit")
    energy_value: Optional[float] = Field(None, description="Energy value")
    energy_unit: Optional[str] = Field(None, description="Energy unit")
    protein: Optional[float] = Field(None, description="Protein")
    fat: Optional[float] = Field(None, description="Fat")
    carbohydrate: Optional[float] = Field(None, description="Carbohydrate")
    fiber: Optional[float] = Field(None, description="Fiber")
    organic: Optional[bool] = Field(None, description="Organic")
    vegetarian: Optional[bool] = Field(None, description="Vegetarian")
    gluten_free: Optional[bool] = Field(None, description="Gluten free")
    lactose_free: Optional[bool] = Field(None, description="Lactose free")
    spicy: Optional[bool] = Field(None, description="Spicy")
    allergens: Optional[List[str]] = Field(None, description="Allergens")


class ProductCategory(BaseModel):
    """Product category model"""
    id: str = Field(..., description="Category ID")
    name: str = Field(..., description="Category name")
    description: Optional[str] = Field(None, description="Description")
    is_deleted: bool = Field(..., description="Is deleted")
    is_hidden: bool = Field(..., description="Is hidden")
    is_included_in_menu: bool = Field(..., description="Is included in menu")
    order: int = Field(..., description="Order")
    parent_id: Optional[str] = Field(None, description="Parent category ID")
    image_urls: Optional[List[str]] = Field(None, description="Image URLs")
    products: Optional[List[Product]] = Field(None, description="Products")


class Menu(BaseModel):
    """Menu model"""
    id: str = Field(..., description="Menu ID")
    name: str = Field(..., description="Menu name")
    description: Optional[str] = Field(None, description="Description")
    categories: List[ProductCategory] = Field(..., description="Categories")
    products: List[Product] = Field(..., description="Products")
    groups: List[ProductGroup] = Field(..., description="Groups")
    version: str = Field(..., description="Version")
    organization_id: str = Field(..., description="Organization ID")
    price_category_id: Optional[str] = Field(None, description="Price category ID")


class MenuRequest(BaseModel):
    """Request model for menu"""
    organization_ids: List[str] = Field(..., description="Organization IDs")
    price_category_id: Optional[str] = Field(None, description="Price category ID")
    include_deleted: Optional[bool] = Field(False, description="Include deleted items")
    include_hidden: Optional[bool] = Field(False, description="Include hidden items")


class MenuResponse(BaseModel):
    """Response model for menu"""
    correlation_id: Optional[str] = Field(None, alias="correlationId", description="Correlation ID")
    groups: List[ProductGroup] = Field(..., description="Groups")
    product_categories: List[ProductCategory] = Field(..., alias="productCategories", description="Product categories")
    products: List[Product] = Field(..., description="Products")
    sizes: Optional[List[ProductSize]] = Field(None, description="Sizes")
    revision: Optional[Union[str, int]] = Field(None, description="Revision")
