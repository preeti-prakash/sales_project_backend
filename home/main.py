from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import orders, sales, users

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Necessary HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Sales Project API"}

# Include routers
app.include_router(orders.router)
app.include_router(sales.router)
app.include_router(users.router)
