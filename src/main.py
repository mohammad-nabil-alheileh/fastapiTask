from fastapi import FastAPI
from presentation.routers import books, members
from infrastructure.db.init_db import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(books.router)
app.include_router(members.router)

# poetry  # use python3.13 # don't make the default version for terminal 
# # poetry lock
# # poetry install

