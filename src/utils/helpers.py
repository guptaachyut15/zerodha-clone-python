from bson.objectid import ObjectId
from src.databases.mongodb import order_book, MongoDB
from src.constants.collections import Collections

mongo_db = MongoDB()


def has_balance(user_id, quantity, price):
    user = mongo_db.get_document(
        Collections.COLLECTION_USERS, {"_id": ObjectId(user_id)}
    )
    if user.get("balance", {}).get("INR", 0) < price * quantity:
        return False
    else:
        return True


def have_stocks(user_id, quantity, stock):
    user = mongo_db.get_document(
        Collections.COLLECTION_USERS, {"_id": ObjectId(user_id)}
    )
    return user.get("balance", {}).get(stock, 0) >= quantity


def add_to_order_book(type, stock_name, quantity, price, user_id):
    order_details = {"user_id": user_id, "quantity": quantity, "price": price}
    order_book[stock_name][type].append(order_details)
    print(f"A {type} order for {stock_name} has been added to the orderbook")


def settle_balances(seller_id, buyer_id, stock_name, quantity, matched_price):
    buyer = mongo_db.get_document(
        Collections.COLLECTION_USERS, {"_id": ObjectId(buyer_id)}
    )
    buyer.get("balance", {})["INR"] -= matched_price * quantity
    if not buyer.get("balance", {}).get(stock_name):
        buyer["balance"][stock_name] = 0
    buyer["balance"][stock_name] += quantity
    mongo_db.update_document(
        Collections.COLLECTION_USERS,
        {"_id": ObjectId(buyer_id)},
        {"balance": buyer["balance"]},
    )
    seller = mongo_db.get_document(
        Collections.COLLECTION_USERS, {"_id": ObjectId(seller_id)}
    )
    seller["balance"]["INR"] += matched_price * quantity
    seller["balance"][stock_name] -= quantity
    mongo_db.update_document(
        Collections.COLLECTION_USERS,
        {"_id": ObjectId(seller_id)},
        {"balance": seller["balance"]},
    )
    return
