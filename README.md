# 🏨 FastAPI Hotel Room Booking Backend System

This project is a complete backend application built using **FastAPI** that simulates a real-world hotel room booking system.  
It demonstrates REST API design, backend workflows, data validation, CRUD operations, and advanced API features.

---

## 🚀 Project Objective

The goal of this project is to build a real-world backend system implementing:

- GET APIs
- POST APIs with Pydantic validation
- Helper functions
- CRUD operations
- Multi-step workflows
- Search, Sorting, and Pagination

This project was developed as part of the **FastAPI Internship Training**.

---

## 🧩 Features Implemented

### 🏨 Room Management
- View all rooms
- Get room by ID
- Room summary statistics
- Add new room
- Update room details
- Delete room (business rules applied)

### 📅 Booking Workflow
- Create booking
- Check room availability
- Check-in workflow
- Checkout workflow
- Active bookings tracking

### 🔎 Advanced API Features
- Room filtering (type, price, floor, availability)
- Keyword search (room number & type)
- Sorting (price, floor, type)
- Pagination support
- Combined browse endpoint (search + sort + pagination)

### ✅ Data Validation
- Implemented using **Pydantic Models**
- Field validation (min_length, gt, le etc.)

---

## 🧠 Backend Concepts Covered

- REST API Design
- FastAPI Routing & Dependency Handling
- Business Logic Implementation
- Helper Functions
- Status Code Handling
- Multi-Step Workflow Design
- Query Parameter Filtering
- Error Handling

---

## 🛠️ Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn

---

## 📦 Installation & Setup

### 1️⃣ Clone Repository
git clone <https://github.com/PraveenKrSharma2002/fastapi-hotel-booking>
cd fastapi-hotel-booking


### 2️⃣ Install Dependencies
pip install -r requirements.txt


### 3️⃣ Run Server
uvicorn main:app --reload


---

## 📚 API Documentation (Swagger)

After running the server: http://127.0.0.1:8000/docs


---

## 📸 Screenshots

All tested API screenshots are available in the `screenshots/` folder.

---

## 🎯 Learning Outcome

Through this project, I gained hands-on experience in:

- Backend API development
- Designing real-world workflows
- Data validation & error handling
- Structuring scalable FastAPI applications
- Testing APIs using Swagger UI

---

## 🙏 Acknowledgement

This project was developed as part of the **FastAPI Internship Training at Innomatics Research Labs**.

---

## 📬 Contact

If you have suggestions or feedback, feel free to connect.
