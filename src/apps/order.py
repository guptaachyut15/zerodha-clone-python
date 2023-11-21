from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from src.utils.helpers import (
    has_balance,
    settle_balances,
    add_to_order_book,
    have_stocks,
)
from src.databases.mongodb import order_book
from src.utils.logger import LOG

router = APIRouter()


class InitiateLimitOrder(BaseModel):
    user_id: str
    price: int
    quantity: int
    type: str
    stock: str


@router.get("/book")
def get_order_book():
    return JSONResponse(status_code=200, content=order_book)


@router.post("/limit")
def make_limit_order(body: InitiateLimitOrder):
    data = body.model_dump()
    if data.get("type") == "Buy" and not has_balance(
        data["user_id"], data["quantity"], data["price"]
    ):
        return HTTPException(
            status_code=401,
            detail={"status": "failed", "message": "You dont have sufficient balance"},
        )
    if data.get("type") == "Sell" and not have_stocks(
        data["user_id"], data["quantity"], data.get("stock")
    ):
        return HTTPException(
            status_code=401,
            detail={"status": "failed", "message": "You dont have sufficient stocks"},
        )
    try:
        stockName = data["stock"]
        if stockName not in order_book:
            order_book[stockName] = {"Sell": [], "Buy": []}

        stockOrders = order_book[stockName]
        LOG.info(stockOrders)

        stockQuantity = data["quantity"]

        if data["type"] == "Buy":
            LOG.info("Recieved a buy order")
            # sorting sell orders in ascending order
            availableSellOrders = sorted(stockOrders["Sell"], key=lambda x: x["price"])
            while stockQuantity:
                if (
                    availableSellOrders
                    and data["price"] >= availableSellOrders[0]["price"]
                ):
                    matchedEntry = availableSellOrders[0]
                    LOG.info("Found one matching entry in sell orders", matchedEntry)
                    settle_balances(
                        matchedEntry["user_id"],
                        data["user_id"],
                        data["stock"],
                        matchedEntry["quantity"],
                        matchedEntry["price"],
                    )

                    if stockQuantity >= matchedEntry["quantity"]:
                        stockQuantity -= matchedEntry["quantity"]
                        availableSellOrders.pop(0)
                    else:
                        matchedEntry["quantity"] -= stockQuantity
                        stockQuantity = 0

                    LOG.info(
                        f"Bought {data['quantity'] - stockQuantity} at a price of {matchedEntry['price']} per share"
                    )
                else:
                    LOG.info("No more matching records in sell order book")
                    break
            stockOrders["Sell"] = availableSellOrders

        elif data["type"] == "Sell":
            LOG.info("Recieved a sell order")
            # sorting buy orders in descending order
            availableBuyOrders = sorted(
                stockOrders["Buy"], key=lambda x: x["price"], reverse=True
            )

            while stockQuantity:
                if (
                    availableBuyOrders
                    and availableBuyOrders[0]["price"] >= data["price"]
                ):
                    matchedEntry = availableBuyOrders[0]
                    LOG.info("Found one matching entry in buy orders", matchedEntry)
                    settle_balances(
                        data["user_id"],
                        matchedEntry["user_id"],
                        data["stock"],
                        matchedEntry["quantity"],
                        data["price"],
                    )

                    if stockQuantity >= matchedEntry["quantity"]:
                        stockQuantity -= matchedEntry["quantity"]
                        availableBuyOrders.pop(0)
                    else:
                        matchedEntry["quantity"] -= stockQuantity
                        stockQuantity = 0

                    LOG.info(
                        f"Sold {data['quantity'] - stockQuantity} at a price of {data['price']} per share"
                    )
                else:
                    LOG.info("No more matching records in buy order book")
                    break
            stockOrders["Buy"] = availableBuyOrders

        if stockQuantity:
            add_to_order_book(
                data["type"],
                data["stock"],
                stockQuantity,
                data["price"],
                data["user_id"],
            )
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": f"Your {data['quantity'] - stockQuantity} Orders have been executed and {stockQuantity} orders have been placed in order book",
                },
            )
        else:
            return JSONResponse(
                {"status": "success", "message": "Your whole Order has been executed"}
            )

    except Exception as err:
        LOG.error("Failed due to error", err)
        return HTTPException({"status": "failed", "message": "Processing failed"})
