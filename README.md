# Zerodha Clone in Python

This project initially began as a clone of Zerodha's limit order system, and has since evolved to include several backend features for a simplified mock stock trading platform.

## Features

1. **User Authentication**
   - Users can sign up and log in using a username and access_token.
   - Access_tokens and usernames are securely stored as sha256 strings.
   
2. **Authorization and Authentication**
   - Upon successful login, a JWT token is generated (valid for 30 minutes initially).
   - The JWT token for production will be managed by Firebase or a similar service, eliminating the 30-minute validity limit. The primary purpose of the token will be to validate client requests (authorization).

3. **User Data Management**
   - User data, including INR and stock details, is stored in a MongoDB collection named "Users."
   
4. **Order Book**
   - The order book is currently an in-memory store, containing information about open orders.
   
5. **Limit Orders**
   - Users can trigger limit orders (buy or sell) for specific stocks.
   - If executable, the order is processed; otherwise, it is added to the order book for future execution.

6. **Order Book Access**
   - Users have access to view the order book, which contains information about pending and executed orders.

7. **Balance and Portfolio**
   - Users can view their account balance and the stocks they currently own.

## How to Run

1. **Create a Virtual Environment:**

    ```bash
    python3 -m venv venv
    ```

2. **Activate the Virtual Environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt

4. **Run the application:**
   -Using Uvicorn
    ```bash
    uvicorn src.main:app --reload --port 8080
    ```
## Environment Variables

Before running the Zerodha Clone, ensure you have set the following environment variables in a `.env` file at the root of your project. These variables are crucial for the proper functioning of the application.

| Variable                  | Description                                                | Example Value                                      |
|---------------------------|------------------------------------------------------------|----------------------------------------------------|
| `MONGODB_CONNECTION_STRING`| The connection string for your MongoDB database.            | `mongodb://username:password@localhost:27017/zerodha_clone` |
| `LOG_LEVEL`               | Specifies the logging level for the application.           | `info` (Other possible values: `debug`, `warning`, `error`, `critical`) |
| `JWT_SECRET_KEY`          | Secret key used for JWT (JSON Web Token) generation.        | `your_secret_key_here`                             |
| `SALT`                    | Salt value used for additional security measures.          | `your_salt_value_here`                             |

Make sure to replace the placeholder values with your actual configuration. Keeping sensitive information, such as secret keys and connection strings, secure is essential for the proper and secure functioning of the application.

The application should now be running locally. Access it through your web browser at http://localhost:8080.


Feel free to explore, contribute, or provide feedback!

