from fastapi import FastAPI,HTTPException
from app.recommender import Recommender

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Recommendation API!"}

@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, top_n: int = 5):
    recommender = Recommender()
    recommendations = recommender.get_recommendations(user_id, top_n)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found for the given user ID.")
    return {"recommendations": recommendations}