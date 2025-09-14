from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class OrderBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Order ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    item: str = Field(
        ...,
        description="Name of the ordered item.",
        example="Laptop"
    )
    quantity: int = Field(
        ...,
        ge=1,
        description="Quantity of the item.",
        example=2
    )
    price: float = Field(
        ...,
        ge=0,
        description="Price per item in USD.",
        example=999.99
    )
    status: Optional[str] = Field(
        default="pending",
        description="Order status (pending/shipped/delivered/cancelled).",
        example="pending",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "item": "Lepro LED Desk Lamp",
                    "quantity": 1,
                    "price": 21.76,
                    "status": "shipped",
                }
            ]
        }
    }


class OrderCreate(OrderBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "item": "Lepro LED Desk Lamp",
                    "quantity": 1,
                    "price": 21.76,
                    "status": "shipped",
                }
            ]
        }
    }


class OrderUpdate(BaseModel):
    item: Optional[str] = Field(None, json_schema_extra={"example": "Smartphone"})
    quantity: Optional[int] = Field(None, json_schema_extra={"example": "4"})
    price: Optional[float] = Field(None, json_schema_extra={"example": "599.99"})
    status: Optional[str] = Field(None, json_schema_extra={"example": "pending"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"item": "Smartphone", "quantity": 4, "price": 599.99, "status": "pending"},
                {"item": "Laptop", "quantity": 1, "price": 1299.99, "status": "shipped"},
            ]
        }
    }

class OrderRead(OrderBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "item": "Lepro LED Desk Lamp",
                    "quantity": 1,
                    "price": 21.76,
                    "status": "shipped",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }