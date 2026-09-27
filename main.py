from fastapi import FastAPI

from database import engine
import models
from routers import auth, transactions


app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(transactions.router)


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running!"}


try:
    with engine.connect():
        print("PostgreSQL connected successfully!")
except Exception as e:
    print("Database connection failed!")
    print(e)