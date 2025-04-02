import uvicorn
from fastapi import FastAPI
from uvicorn import lifespan

from routers import catrogry as catrogry_router
from routers import users as users_router
from routers import document as document_router

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:3000","http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(catrogry_router.router)
app.include_router(users_router.router)
app.include_router(document_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
