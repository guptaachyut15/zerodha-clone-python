from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.apps.order import router as order_router
from src.apps.user import router as user_router

app = FastAPI()


@app.get("/")
def home():
    print("In the home page")
    return HTMLResponse("<h1>Home page</h1>")


app.include_router(order_router, prefix="/order")
app.include_router(user_router, prefix="/user")
