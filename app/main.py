from fastapi import FastAPI

app = FastAPI(
    title="StayEase API",
    description="Hotel Booking Backend API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to StayEase API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "running"
    }
