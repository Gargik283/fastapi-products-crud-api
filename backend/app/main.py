from dotenv import load_dotenv
import os

from fastapi import FastAPI, HTTPException, Path, Query, Depends, Request
from fastapi.responses import JSONResponse

from backend.app.services.products import (
    get_all_products,
    add_product,
    remove_product,
    change_product,
    load_products
)

from backend.app.schema.product import Product, ProductUpdate

from typing import Dict


load_dotenv()

app = FastAPI()


# @app.middleware("http")
# async def lifecycle(request: Request, call_next):
#     print("Before Request")
#     response = await call_next(request)
#     print("After Request")
#     return response


def common_logic():
    return "Hello There"


@app.get("/", response_model=dict)
def root(dep=Depends(common_logic)):

    DB_PATH = os.getenv("BASE_URL")

    return JSONResponse(
        status_code=200,
        content={
            "message": "Welcome to FastAPI.",
            "dependency": dep,
            "data_path": DB_PATH,
        },
    )


@app.get("/products", response_model=Dict)
def list_products(
    dep=Depends(load_products),

    name: str = Query(
        default=None,
        min_length=1,
        max_length=50,
        description="Search by product name (case insensitive)",
        examples=["Wireless Headphones"]
    ),

    sort_by_price: bool = Query(
        default=False,
        description="Sort products by price"
    ),

    order: str = Query(
        default="asc",
        description="Sort order when sort_by_price=true (asc, desc)"
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of items to return"
    ),

    offset: int = Query(
        default=0,
        ge=0,
        description="Pagination offset"
    )
):

    products = dep

    # Search by product name
    if name:
        needle = name.strip().lower()

        products = [
            p for p in products
            if needle in p.get("name", "").lower()
        ]

    if not products:
        raise HTTPException(
            status_code=404,
            detail=f"No product found matching name = {name}"
        )

    # Sort by price
    if sort_by_price:

        if order.lower() not in ["asc", "desc"]:
            raise HTTPException(
                status_code=400,
                detail="Order must be either 'asc' or 'desc'"
            )

        reverse = order.lower() == "desc"

        products = sorted(
            products,
            key=lambda p: p.get("price", 0),
            reverse=reverse
        )

    total = len(products)

    # Pagination
    products = products[offset:offset + limit]

    return {
        "total": total,
        "items": products
    }


@app.get("/products/{product_id}", response_model=Dict)
def get_product_by_id(
    product_id: int = Path(
        ...,
        description="Integer ID of the product",
        examples=[1]
    )
):

    products = get_all_products()

    for product in products:

        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found!"
    )


@app.post("/products", status_code=201)
def create_product(product: Product):

    products = get_all_products()

    # Generate the next integer ID
    if products:
        new_id = max(p["id"] for p in products) + 1
    else:
        new_id = 1

    product_dict = product.model_dump(mode="json")

    product_dict["id"] = new_id

    try:
        add_product(product_dict)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return product_dict


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int = Path(
        ...,
        description="Product ID"
    )
):

    try:

        result = remove_product(str(product_id))

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@app.put("/products/{product_id}")
def update_product(
    product_id: int = Path(
        ...,
        description="Product ID"
    ),

    payload: ProductUpdate = ...
):

    try:

        updated_product = change_product(
            str(product_id),
            payload.model_dump(
                mode="json",
                exclude_unset=True
            )
        )

        return updated_product

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )