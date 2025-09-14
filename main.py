from __future__ import annotations
import os
import socket
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query, Path, status

from models.user import UserCreate, UserRead, UserUpdate
from models.order import OrderCreate, OrderRead, OrderUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# --------------------------------------------------------------------------
# In-memory "databases"
# --------------------------------------------------------------------------
users: Dict[UUID, UserRead] = {}
orders: Dict[UUID, OrderRead] = {}

app = FastAPI(
    title="User/Order API",
    description="Demo FastAPI app using Pydantic v2 models for User and Order",
    version="0.1.0",
)

# --------------------------------------------------------------------------
# Health endpoints
# --------------------------------------------------------------------------
# def make_health(echo: Optional[str], path_echo: Optional[str] = None) -> Health:
#     return Health(
#         status=200,
#         status_message="OK",
#         timestamp=datetime.utcnow().isoformat() + "Z",
#         ip_address=socket.gethostbyname(socket.gethostname()),
#         echo=echo,
#         path_echo=path_echo
#     )
#
# @app.get("/health", response_model=Health)
# def get_health_no_path(echo: str | None = Query(None)):
#     return make_health(echo=echo, path_echo=None)
#
# @app.get("/health/{path_echo}", response_model=Health)
# def get_health_with_path(
#     path_echo: str = Path(...),
#     echo: str | None = Query(None),
# ):
#     return make_health(echo=echo, path_echo=path_echo)

# --------------------------------------------------------------------------
# Order endpoints
# --------------------------------------------------------------------------
@app.post("/orders", response_model=OrderRead, status_code=201)
def create_order(order: OrderCreate):
    order_read = OrderRead(**order.model_dump())
    orders[order_read.id] = order_read
    return order_read

@app.get("/orders", response_model=List[OrderRead])
def list_orders(
    item: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    results = list(orders.values())
    if item is not None:
        results = [o for o in results if o.item == item]
    if status is not None:
        results = [o for o in results if o.status == status]
    return results

@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: UUID):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]

@app.patch("/orders/{order_id}", response_model=OrderRead)
def update_order(order_id: UUID, update: OrderUpdate):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    stored = orders[order_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    orders[order_id] = OrderRead(**stored)
    return orders[order_id]

@app.delete("/orders/{order_id}", response_model=OrderRead)
def delete_order(order_id: UUID):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    removed = orders.pop(order_id)
    return removed
# --------------------------------------------------------------------------
# User endpoints
# --------------------------------------------------------------------------
@app.post("/users", response_model=UserRead, status_code=201)
def create_user(user: UserCreate):
    user_read = UserRead(**user.model_dump())
    users[user_read.id] = user_read
    return user_read

@app.get("/users", response_model=List[UserRead])
def list_users(
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
):
    results = list(users.values())
    if first_name is not None:
        results = [u for u in results if u.first_name == first_name]
    if last_name is not None:
        results = [u for u in results if u.last_name == last_name]
    if email is not None:
        results = [u for u in results if u.email == email]
    return results

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: UUID):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.patch("/users/{user_id}", response_model=UserRead)
def update_user(user_id: UUID, update: UserUpdate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    stored = users[user_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    users[user_id] = UserRead(**stored)
    return users[user_id]

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return None
# --------------------------------------------------------------------------
# Root
# --------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the User/Order API. See /docs for OpenAPI UI."}

# --------------------------------------------------------------------------
# Entrypoint
# --------------------------------------------------------------------------
# check for image
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
