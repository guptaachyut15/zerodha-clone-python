# zerodha-clone-python
Started of as a zerodha limit order clone, This clone now supports following backend features:
1. Signup and login by using a username and access_token
  a. Access_tokens and usernnames are stored as sha256 strings for security
2. (Authorisation and authentication)On successful login a jwt token is generated (valid for 30 min for now) which can be used to trigger various requests
   a. The jwt token for the production will be handled by firbase or some similar thing which will remove the 30min mark for the validity and then the function of jwt token will be to validate the requests from the client(authorisation)
4. Users data related to INR and stock details are stored in a mongodb collection named Users
5. The order book is an in memory(for now) store and stores information regarding the open orders if any
6. A user can trigger a limit order(either buy or sell) for a particular stock and that will be executed if it can or else it will be added in the orderbook waiting to get triggered
7. A user can access the orderbook
8. Users can view their balance and the stocks they own

## How to run

python3 -m venv venv

venv\Scripts\activate

uvicorn src.main:app --reload --port 8080
