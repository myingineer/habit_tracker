from fastapi import FastAPI
from .Routers import habits_router, users_router, auth_router, analytic_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(habits_router.router)
app.include_router(users_router.router)
app.include_router(auth_router.router)
app.include_router(analytic_router.router)

@app.get("/")
async def root():
    return {
        "status": "success", 
        "message": "Welcome to the Habit Tracker API! Read the documentation to get started."
    }