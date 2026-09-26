from pydantic import BaseModel, Field
from typing import Optional, Literal


# CREATE PYDANTIC

class Product(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="Unique product ID"
    )

    name: str = Field(
        min_length=3,
        max_length=80,
        title="Product Name",
        description="Readable product name",
        examples=["Wireless Headphones", "Bluetooth Speaker"],
    )

    description: str = Field(
        max_length=200,
        description="Short product description"
    )

    category: str = Field(
        min_length=3,
        max_length=50,
        description="Product category",
        examples=["Electronics", "Fashion", "Grocery"],
    )

    brand: str = Field(
        min_length=2,
        max_length=40,
        examples=["ShopEase"]
    )

    price: float = Field(
        gt=0,
        description="Product price in INR"
    )

    currency: Literal["INR"] = Field(
        default="INR",
        description="Product currency"
    )

    stock: int = Field(
        ge=0,
        description="Available stock"
    )

    rating: float = Field(
        ge=0,
        le=5,
        description="Rating out of 5"
    )

    reviews: int = Field(
        ge=0,
        description="Number of reviews"
    )

    in_stock: bool = Field(
        description="Whether the product is currently in stock"
    )


# UPDATE PYDANTIC

class ProductUpdate(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=80
    )

    description: Optional[str] = Field(
        default=None,
        max_length=200
    )

    category: Optional[str] = None

    brand: Optional[str] = None

    price: Optional[float] = Field(
        default=None,
        gt=0
    )

    currency: Optional[Literal["INR"]] = None

    stock: Optional[int] = Field(
        default=None,
        ge=0
    )

    rating: Optional[float] = Field(
        default=None,
        ge=0,
        le=5
    )

    reviews: Optional[int] = Field(
        default=None,
        ge=0
    )

    in_stock: Optional[bool] = None