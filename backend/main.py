from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import databricks, layers, masterdata_ds21, swatches, tpm, utility

app = FastAPI(
    title="ScriPTA",
    description="REST API for managing Technical Packaging Material Data and InDesign Swatch and Layer Configurations",
    version="1.0.1"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(utility.router)
app.include_router(swatches.router)
app.include_router(layers.router)
app.include_router(tpm.router)
app.include_router(masterdata_ds21.router)
app.include_router(databricks.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
