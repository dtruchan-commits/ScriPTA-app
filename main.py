from fastapi import FastAPI

from routers import layers, masterdata, swatches, tpm, utility

app = FastAPI(
    title="ScriPTA",
    description="REST API for managing Technical Packaging Material Data and InDesign Swatch and Layer Configurations",
    version="1.0.1"
)

# Include routers
app.include_router(utility.router)
app.include_router(swatches.router)
app.include_router(layers.router)
app.include_router(tpm.router)
app.include_router(masterdata.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
