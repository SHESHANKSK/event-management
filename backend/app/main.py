from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.web.routers import user_router, event_router, attendance_router

app = FastAPI(title="Event Management System")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(event_router.router)
app.include_router(attendance_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Management System API"}
