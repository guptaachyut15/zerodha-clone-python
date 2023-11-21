from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from src.apps.order import router as order_router
from src.apps.user import router as user_router
from src.apps.auth import router as auth_router
from src.utils.logger import LOG, initialize_logging
from src.utils.security import has_access


initialize_logging()
app = FastAPI()


@app.get("/")
def home():
    LOG.info("In the home page")
    return HTMLResponse("<h1>Home page</h1>")


app.include_router(auth_router, prefix="/auth")
app.include_router(order_router, prefix="/order", dependencies=[Depends(has_access)])
app.include_router(user_router, prefix="/user", dependencies=[Depends(has_access)])
