from typing import List, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Parking Slot Management API")


class ParkingSlot(BaseModel):
    id: int
    title: str
    description: str
    status: Literal["available", "occupied"]
    priority: Literal["low", "medium", "high"]


parking_slots_db: dict[int, ParkingSlot] = {}


@app.get("/parking-slots", response_model=List[ParkingSlot])
def get_all_parking_slots():
    return list(parking_slots_db.values())


@app.get("/parking-slots/{slot_id}", response_model=ParkingSlot)
def get_parking_slot(slot_id: int):
    if slot_id not in parking_slots_db:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    return parking_slots_db[slot_id]


@app.post("/parking-slots", response_model=ParkingSlot, status_code=201)
def create_parking_slot(slot: ParkingSlot):
    if slot.id in parking_slots_db:
        raise HTTPException(status_code=400, detail="Duplicate parking slot ID")
    parking_slots_db[slot.id] = slot
    return slot


@app.put("/parking-slots/{slot_id}", response_model=ParkingSlot)
def update_parking_slot(slot_id: int, slot: ParkingSlot):
    if slot_id not in parking_slots_db:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    parking_slots_db[slot_id] = slot
    return slot


@app.delete("/parking-slots/{slot_id}", status_code=200)
def delete_parking_slot(slot_id: int):
    if slot_id not in parking_slots_db:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    del parking_slots_db[slot_id]
    return {"message": "Parking slot deleted successfully"}
