from fastapi import FastAPI, Query, status
from pydantic import BaseModel, Field

app = FastAPI()

# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"message": "Welcome to Grand Stay Hotel"}


# ---------------- ROOMS DATA ----------------

rooms = [
    {"id": 1, "room_number": "101", "type": "Single", "price_per_night": 2000, "floor": 1, "is_available": True},
    {"id": 2, "room_number": "102", "type": "Double", "price_per_night": 3000, "floor": 1, "is_available": True},
    {"id": 3, "room_number": "201", "type": "Suite", "price_per_night": 5000, "floor": 2, "is_available": True},
    {"id": 4, "room_number": "202", "type": "Deluxe", "price_per_night": 4500, "floor": 2, "is_available": False},
    {"id": 5, "room_number": "301", "type": "Single", "price_per_night": 2200, "floor": 3, "is_available": True},
    {"id": 6, "room_number": "302", "type": "Double", "price_per_night": 3200, "floor": 3, "is_available": False},
]


# ---------------- GET ROOMS ----------------

@app.get("/rooms")
def get_rooms():
    total = len(rooms)
    available = len([r for r in rooms if r["is_available"]])
    return {"rooms": rooms, "total_rooms": total, "available_count": available}


@app.get("/rooms/summary")
def rooms_summary():
    total = len(rooms)
    available = len([r for r in rooms if r["is_available"]])
    occupied = total - available
    prices = [r["price_per_night"] for r in rooms]

    type_breakdown = {}
    for r in rooms:
        type_breakdown[r["type"]] = type_breakdown.get(r["type"], 0) + 1

    return {
        "total_rooms": total,
        "available": available,
        "occupied": occupied,
        "cheapest": min(prices),
        "most_expensive": max(prices),
        "type_breakdown": type_breakdown
    }


# ---------------- FILTER ----------------

def filter_rooms_logic(type=None, max_price=None, floor=None, is_available=None):
    result = rooms

    if type is not None:
        result = [r for r in result if r["type"].lower() == type.lower()]

    if max_price is not None:
        result = [r for r in result if r["price_per_night"] <= max_price]

    if floor is not None:
        result = [r for r in result if r["floor"] == floor]

    if is_available is not None:
        result = [r for r in result if r["is_available"] == is_available]

    return result


@app.get("/rooms/filter")
def filter_rooms(
    type: str = Query(None),
    max_price: int = Query(None),
    floor: int = Query(None),
    is_available: bool = Query(None)
):
    filtered = filter_rooms_logic(type, max_price, floor, is_available)
    return {"filtered_rooms": filtered, "count": len(filtered)}

@app.get("/rooms/search")
def search_rooms(keyword: str):
    result = [r for r in rooms if keyword.lower() in r["type"].lower() or keyword.lower() in r["room_number"]]
    return {"results": result}

@app.get("/rooms/sort")
def sort_rooms():
    return {"sorted": sorted(rooms, key=lambda x: x["price_per_night"])}

@app.get("/rooms/page")
def paginate_rooms(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    return {"data": rooms[start:end]}

@app.get("/rooms/browse")
def browse_rooms():
    return {"data": rooms}

@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            return room
    return {"error": "Room not found"}


# ---------------- BOOKINGS ----------------

bookings = []
booking_counter = 1


@app.get("/bookings")
def get_bookings():
    return {"bookings": bookings, "total": len(bookings)}


# ---------------- MODELS ----------------

class BookingRequest(BaseModel):
    guest_name: str = Field(..., min_length=2)
    room_id: int = Field(..., gt=0)
    nights: int = Field(..., gt=0, le=30)
    phone: str = Field(..., min_length=10)
    meal_plan: str = "none"
    early_checkout: bool = False


class NewRoom(BaseModel):
    room_number: str = Field(..., min_length=1)
    type: str = Field(..., min_length=2)
    price_per_night: int = Field(..., gt=0)
    floor: int = Field(..., gt=0)
    is_available: bool = True


# ---------------- HELPERS ----------------

def find_room(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            return room
    return None


def calculate_stay_cost(price_per_night, nights, meal_plan, early_checkout):
    total = price_per_night * nights

    if meal_plan == "breakfast":
        total += 500 * nights
    elif meal_plan == "all-inclusive":
        total += 1200 * nights

    discount = 0
    if early_checkout:
        discount = total * 0.10
        total -= discount

    return total, discount


# ---------------- CREATE BOOKING ----------------

@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(request: BookingRequest):
    global booking_counter

    room = find_room(request.room_id)

    if not room:
        return {"error": "Room not found"}

    if not room["is_available"]:
        return {"error": "Room is already occupied"}

    room["is_available"] = False

    total_cost, discount = calculate_stay_cost(
        room["price_per_night"],
        request.nights,
        request.meal_plan,
        request.early_checkout
    )

    booking = {
        "booking_id": booking_counter,
        "guest_name": request.guest_name,
        "room": room,
        "nights": request.nights,
        "meal_plan": request.meal_plan,
        "total_cost": total_cost,
        "discount": discount,
        "status": "confirmed"
    }

    bookings.append(booking)
    booking_counter += 1

    return booking


# ---------------- CRUD ROOMS ----------------

@app.post("/rooms", status_code=status.HTTP_201_CREATED)
def add_room(room: NewRoom):

    for r in rooms:
        if r["room_number"] == room.room_number:
            return {"error": "Room number already exists"}

    new_room = {
        "id": len(rooms) + 1,
        "room_number": room.room_number,
        "type": room.type,
        "price_per_night": room.price_per_night,
        "floor": room.floor,
        "is_available": room.is_available
    }

    rooms.append(new_room)
    return new_room


@app.put("/rooms/{room_id}")
def update_room(
    room_id: int,
    price_per_night: int = Query(None),
    is_available: bool = Query(None)
):

    for r in rooms:
        if r["id"] == room_id:

            if price_per_night is not None:
                r["price_per_night"] = price_per_night

            if is_available is not None:
                r["is_available"] = is_available

            return r

    return {"error": "Room not found"}


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):

    for r in rooms:
        if r["id"] == room_id:

            if not r["is_available"]:
                return {"error": "Cannot delete occupied room"}

            rooms.remove(r)
            return {"message": "Room deleted"}

    return {"error": "Room not found"}


# ---------------- WORKFLOW ----------------

@app.post("/checkin/{booking_id}")
def checkin(booking_id: int):

    for b in bookings:
        if b["booking_id"] == booking_id:
            b["status"] = "checked_in"
            return b

    return {"error": "Booking not found"}


@app.get("/bookings/active")
def active_bookings():

    active = [
        b for b in bookings
        if b["status"] in ["confirmed", "checked_in"]
    ]

    return {"active_bookings": active}


@app.post("/checkout/{booking_id}")
def checkout(booking_id: int):

    for b in bookings:
        if b["booking_id"] == booking_id:

            b["status"] = "checked_out"

            room = find_room(b["room"]["id"])
            if room:
                room["is_available"] = True

            return b

    return {"error": "Booking not found"}

@app.get("/rooms/search")
def search_rooms(keyword: str):

    result = [
        r for r in rooms
        if keyword.lower() in r["room_number"].lower()
        or keyword.lower() in r["type"].lower()
    ]

    if not result:
        return {"message": "No rooms found"}

    return {
        "results": result,
        "total_found": len(result)
    }

@app.get("/rooms/sort")
def sort_rooms(
    sort_by: str = "price_per_night",
    order: str = "asc"
):

    valid_fields = ["price_per_night", "floor", "type"]

    if sort_by not in valid_fields:
        return {"error": "Invalid sort field"}

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order"}

    sorted_rooms = sorted(
        rooms,
        key=lambda x: x[sort_by],
        reverse=(order == "desc")
    )

    return {"sorted_rooms": sorted_rooms}

@app.get("/rooms/page")
def paginate_rooms(
    page: int = 1,
    limit: int = 2
):

    total = len(rooms)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_rooms": total,
        "total_pages": total_pages,
        "data": rooms[start:end]
    }

@app.get("/bookings/search")
def search_bookings(guest_name: str):

    result = [
        b for b in bookings
        if guest_name.lower() in b["guest_name"].lower()
    ]

    return {"results": result}

@app.get("/bookings/sort")
def sort_bookings(sort_by: str = "total_cost"):

    if sort_by not in ["total_cost", "nights"]:
        return {"error": "Invalid sort field"}

    sorted_data = sorted(bookings, key=lambda x: x[sort_by])

    return {"sorted_bookings": sorted_data}

@app.get("/rooms/browse")
def browse_rooms(
    keyword: str = None,
    sort_by: str = "price_per_night",
    order: str = "asc",
    page: int = 1,
    limit: int = 3
):

    result = rooms

    # search
    if keyword:
        result = [
            r for r in result
            if keyword.lower() in r["type"].lower()
            or keyword.lower() in r["room_number"].lower()
        ]

    # sort
    result = sorted(
        result,
        key=lambda x: x[sort_by],
        reverse=(order == "desc")
    )

    # pagination
    total = len(result)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "data": result[start:end]
    }

@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            return room
    return {"error": "Room not found"}