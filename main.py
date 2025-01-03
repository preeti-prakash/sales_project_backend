from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import orders, sales, users
from fastapi.staticfiles import StaticFiles



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sales-react-application-504211475748.us-central1.run.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# cors added
@app.get("/")
async def root():
    return {"message": "Welcome to the Sales Project API"}

# Include routers
app.include_router(orders.router)
app.include_router(sales.router)
app.include_router(users.router)
