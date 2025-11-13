from typing import Union
import uvicorn

from fastapi import FastAPI
from refuge_esn81.router.animals import animalsRouter
from refuge_esn81.router.species import speciesRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Refuge ESN81 API",
    description="API for managing animal refuge data including animals and species",
    version="1.0.0",
    contact={
        "name": "Refuge ESN81",
        "email": "contact@refuge-esn81.com",
    },
    license_info={
        "name": "MIT",
    },
)
app.include_router(animalsRouter)
app.include_router(speciesRouter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, port=9000)
