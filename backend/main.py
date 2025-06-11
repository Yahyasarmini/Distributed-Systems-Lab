# main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import uvicorn
from contextlib import asynccontextmanager

# Pydantic Models
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    quantity: int = Field(..., ge=0, description="Item quantity")

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[int] = Field(None, ge=0)

class Item(BaseModel):
    id: int
    name: str
    quantity: int

# In-memory storage (will be replaced with database in next lab)
items_storage: List[Item] = [
    Item(id=1, name="Apple", quantity=42),
    Item(id=2, name="Banana", quantity=25),
    Item(id=3, name="Orange", quantity=30)
]
next_id = 4

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    12-Factor IX: Disposability - Graceful startup and shutdown
    """
    print("🚀 Starting FastAPI Items API...")
    print(f"📦 Loaded {len(items_storage)} initial items")
    yield
    print("🛑 Shutting down FastAPI Items API...")

# FastAPI App with external configuration
app = FastAPI(
    title="Item API",
    version="1.0.0",
    description="Simple API for managing items - 12-Factor compliant",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 12-Factor VI: Processes - Configure CORS from environment
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint for 12-Factor IX: Disposability
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for load balancers and monitoring"""
    return {
        "status": "healthy",
        "items_count": len(items_storage),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Item Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/items", response_model=List[Item], tags=["Items"])
async def get_all_items():
    """
    Get all items
    
    12-Factor VI: Processes - Stateless operation
    """
    return items_storage

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(item: ItemCreate):
    """
    Create a new item
    
    12-Factor VI: Processes - No shared state between requests
    """
    global next_id
    
    new_item = Item(
        id=next_id,
        name=item.name,
        quantity=item.quantity
    )
    
    items_storage.append(new_item)
    next_id += 1
    
    return new_item

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(item_id: int):
    """
    Get item by ID
    
    Returns 404 if item not found
    """
    item = next((item for item in items_storage if item.id == item_id), None)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    return item

@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(item_id: int, item_update: ItemUpdate):
    """
    Update item
    
    Partial updates supported - only provided fields will be updated
    """
    item_index = next(
        (index for index, item in enumerate(items_storage) if item.id == item_id), 
        None
    )
    
    if item_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    # Update only provided fields
    existing_item = items_storage[item_index]
    update_data = item_update.dict(exclude_unset=True)
    
    updated_item = Item(
        id=existing_item.id,
        name=update_data.get("name", existing_item.name),
        quantity=update_data.get("quantity", existing_item.quantity)
    )
    
    items_storage[item_index] = updated_item
    return updated_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
async def delete_item(item_id: int):
    """
    Delete item
    
    Returns 204 No Content on successful deletion
    Returns 404 if item not found
    """
    item_index = next(
        (index for index, item in enumerate(items_storage) if item.id == item_id), 
        None
    )
    
    if item_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    items_storage.pop(item_index)
    # FastAPI automatically returns 204 No Content

# 12-Factor III: Config - All configuration from environment
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    log_level = os.getenv("LOG_LEVEL", "info")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=os.getenv("ENVIRONMENT") == "development"
    )