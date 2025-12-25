from fastapi import FastAPI, HTTPException
from app.limiter import is_allowed

app = FastAPI(title="Traffic Citadel API")

# Configuration: 5 requests every 60 seconds (Let's make it tight for testing)
RATE_LIMIT = 5
WINDOW_SIZE = 60

@app.get("/")
def home():
    return {"message": "Traffic Citadel is Online"}

@app.get("/access/{user_id}")
def access_resource(user_id: str):
    """
    This endpoint asks Redis: "Has this user done too much recently?"
    """
    
    # Call your new "Sliding Window" logic
    allowed = is_allowed(user_id, RATE_LIMIT, WINDOW_SIZE)

    if not allowed:
        # If False, kick them out with a 429 Error
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Slow down!")

    return {"status": "Access Granted", "user": user_id}