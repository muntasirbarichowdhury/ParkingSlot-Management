from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Parking Slot Management API",
    version="1.0.0",
)


class ParkingSlot(BaseModel):
    id: int
    title: str
    description: str
    status: Literal["available", "occupied"]
    priority: Literal["low", "medium", "high"]


# Simple in-memory storage
parking_slots = [
    ParkingSlot(
        id=1,
        title="Parking Slot A-01",
        description="Ground floor near main entrance",
        status="available",
        priority="high",
    ),
    ParkingSlot(
        id=2,
        title="Parking Slot A-02",
        description="Ground floor near security desk",
        status="occupied",
        priority="medium",
    ),
    ParkingSlot(
        id=3,
        title="Parking Slot A-03",
        description="First floor near elevator",
        status="available",
        priority="low",
    ),
]


# GET - Get all parking slots
@app.get("/parking-slots")
def get_all_parking_slots():
    return parking_slots


# GET - Get a single parking slot
@app.get("/parking-slots/{slot_id}")
def get_parking_slot(slot_id: int):
    for slot in parking_slots:
        if slot.id == slot_id:
            return slot

    raise HTTPException(
        status_code=404,
        detail="Parking slot not found",
    )


# POST - Create a new parking slot
@app.post("/parking-slots")
def create_parking_slot(slot: ParkingSlot):
    for existing_slot in parking_slots:
        if existing_slot.id == slot.id:
            raise HTTPException(
                status_code=400,
                detail="Parking slot ID already exists",
            )

    parking_slots.append(slot)
    return slot


# PUT - Update an existing parking slot
@app.put("/parking-slots/{slot_id}")
def update_parking_slot(slot_id: int, updated_slot: ParkingSlot):
    for index, existing_slot in enumerate(parking_slots):
        if existing_slot.id == slot_id:
            parking_slots[index] = updated_slot
            return updated_slot

    raise HTTPException(
        status_code=404,
        detail="Parking slot not found",
    )


# DELETE - Delete a parking slot
@app.delete("/parking-slots/{slot_id}")
def delete_parking_slot(slot_id: int):
    for index, slot in enumerate(parking_slots):
        if slot.id == slot_id:
            deleted_slot = parking_slots.pop(index)

            return {
                "message": "Parking slot deleted successfully",
                "slot": deleted_slot,
            }

    raise HTTPException(
        status_code=404,
        detail="Parking slot not found",
    )