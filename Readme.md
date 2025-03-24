***eBay Used Cars Backend API***

This project is for the eBay Used Cars Backend API. It is built using Flask and MongoDB and provides RESTful endpoints to manage car listings, user authentication, reviews, and administrative operations.

## Requirements
- Python 3.8 or later
- MongoDB running locally on port 27017

## Installation and Setup

1. **Obtain the Project Files:**  
   Place all project files in a folder on your computer.

2. **(Optional) Create and Activate a Virtual Environment:**  
   - Open a terminal in the project folder.
   - Run:
     ```
     python -m venv venv
     venv\Scripts\activate   # Windows
     # or
     source venv/bin/activate   # macOS/Linux
     ```

3. **Install Required Python Packages:**  
   Use the provided `requirements.txt` file:
     ```
     pip install -r requirements.txt
     ```
   The key dependencies are:
   - Flask==3.1.0
   - pymongo==4.11.1
   - PyJWT==2.10.1
   - bcrypt==4.2.1

## Configuration

- **MongoDB Connection:**  
The API connects to MongoDB at `mongodb://localhost:27017/` and uses the database named `ebay_used_cars`.

- **JWT Secret Key:**  
Defined in `globals.py` as `SECRET_KEY = 'mysecret'`.

- **Utilities:**  
The `utils.py` module provides a function to recursively convert MongoDB ObjectId values to strings for consistent JSON responses.

## Running the Server

To start the API server, run:
    ```
    python app.py
    ```

The server will start in debug mode on port 5001. Access it at `http://localhost:5001`.

## API Endpoints Overview

### **Authentication:**
- **GET /auth/login:**  
  Authenticates a user (buyer or seller) via Basic Auth and returns a JWT token.
- **GET /auth/login (Admin):**  
  Authenticates an admin user and returns an admin JWT token.
- **GET /auth/profile:**  
  Retrieves the profile of the authenticated user.
- **DELETE /auth/delete:**  
  Deletes the account of the authenticated user.
- **GET /auth/logout:**  
  Logs out the user by blacklisting their JWT token.

### **Listings:**
- **POST /listings:**  
  Creates a new car listing. The request body must include:  
  - `vehicle_model`  
  - `price`  
  - `mileage`  
  - `location`  
  - `car_type`  
  - `listing_age`  
  The system automatically initializes the `reviews` field (as an empty list) and sets `views` to 0.
  
- **GET /listings:**  
  Retrieves all listings, supporting filtering by attributes, pagination (via `page` and `page_size` query parameters), and sorting (if extended in the future).
  
- **GET /listings/{id}:**  
  Retrieves details of a specific listing by its ID and increments its view count.
  
- **GET /listings/stats/average_price_by_type:**  
  Returns the average price for each car type (rounded to 2 decimal places) for active listings.
  
- **GET /listings/stats/summary:**  
  Provides overall summary statistics for active listings (total count, average, minimum, and maximum price) along with a count per car type.
  
- **PUT /listings/{listing_id}:**  
  Updates an existing listing. Only the owner can update.
  
- **PUT /listings/{listing_id}/mark_sold:**  
  Marks a listing as sold (owner only).
  
- **DELETE /listings/{listing_id}:**  
  Deletes a listing (owner only).
  
- **POST /listings/{listing_id}/report:**  
  Reports a listing.

### **Reviews:**
- **POST /listings/{listing_id}/reviews:**  
  Adds a review with a rating (1–5) and review text to a listing. Returns the new review’s ID.
  
- **GET /listings/{listing_id}/reviews:**  
  Retrieves all reviews for a listing.
  
- **PUT /listings/{listing_id}/reviews/{review_id}:**  
  Updates an existing review (only the review creator can update).
  
- **DELETE /listings/{listing_id}/reviews/{review_id}:**  
  Deletes a review (requires admin privileges).

### **Admin Operations:**
- **GET /admin/listings:**  
  Retrieves all reported or sold listings (active listings are excluded). Supports filtering by seller ID.
  
- **DELETE /admin/listings/{id}:**  
  Deletes a reported or sold listing.
  
- **GET /admin/users:**  
  Retrieves all registered users.
  
- **DELETE /admin/users/{id}:**  
  Deletes a user account.
  
- **PUT /admin/users/{id}/role:**  
  Updates a user’s role (e.g., promoting a user to admin).

## Automated Testing

A Postman collection named “TEST EBAY USED CARS” is provided. This collection uses global variables:
- `baseURL`
- `jwt-token-user`
- `jwt-token-admin`
- `listing_id`
- `review_id`

To run the tests:
1. Import the collection into Postman.
2. Use Postman’s Collection Runner to execute all tests and verify that responses match the expected status codes and messages.

## MongoDB Collections Export

Export each MongoDB collection (e.g., `users`, `listings`, `blacklist`) to JSON files using the mongoexport command. 

Run:
    ```
    mongoexport --uri="mongodb://localhost:27017/ebay_used_cars" --collection=users --out=users.json
    mongoexport --uri="mongodb://localhost:27017/ebay_used_cars" --collection=listings --out=listings.json
    mongoexport --uri="mongodb://localhost:27017/ebay_used_cars" --collection=blacklist --out=blacklist.json
    ```

## Submission Package

Final submission included:
- A ZIP file containing all back-end API code files.
- A ZIP file containing the exported JSON files for each MongoDB collection.
- PDF documents for:
  - Complete code listing of the back-end API.
  - Summary of all API endpoints.
  - Printout of automated Postman test results.
  - API documentation generated via Postman.

## Final Note

This project was developed as an assignment. All necessary code files, database exports, and documentation are included in the submission package.
