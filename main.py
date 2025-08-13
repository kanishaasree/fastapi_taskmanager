# from fastapi import FastAPI
# from sqlmodel import SQLModel
# from database import engine
# from routes import tasks, auth

# app = FastAPI()

# @app.on_event("startup")
# async def on_startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)

# @app.get("/greet/{name}")
# async def root(name: str):
#     return {"message": f"Hello! {name}"}

# app.include_router(auth.router)
# app.include_router(tasks.router)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from database import engine
from routes import tasks, auth
import time

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/greet/{name}")
async def root(name: str):
    return {"message": f"Hello! {name}"}

app.include_router(auth.router)
app.include_router(tasks.router)
