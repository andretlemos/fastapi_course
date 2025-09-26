from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
    12701: {"weight": 0.6, "content": "glassware", "status": "placed"},
    12702: {"weight": 2.3, "content": "books", "status": "shipped"},
    12703: {"weight": 1.1, "content": "electronics", "status": "delivered"},
    12704: {"weight": 3.5, "content": "furniture", "status": "in transit"},
    12705: {"weight": 0.9, "content": "clothing", "status": "returned"},
    12706: {"weight": 4.0, "content": "appliances", "status": "processing"},
    12707: {"weight": 1.8, "content": "toys", "status": "placed"},
}


@app.get("/shipment/latest")
def get_latest_shipment():
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    if not id:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="this id is not existed"
        )

    return shipments[id]


@app.post("/shipment")
def submit_shipment(data: dict[str, Any]) -> dict[str, Any]:
    content = data["content"]
    weight = data["weight"]

    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            description="Maximum weight limit is 25 kgs",
        )

    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": "placed",
    }

    return {"id": new_id}


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> Any:
    return shipments[id][field]


@app.put("/shipment")
def shipment_update(
    id: int,
    content: str,
    weight: float,
    status: str,
) -> dict[str, Any]:
    shipments[id] = {
        "content": content,
        "weight": weight,
        "status": "placed",
    }
    return shipments[id]

@app.patch("/shipment")
def patch_shipment(id: int,
    content: str | None = None,
    weight: float | None = None,
    status: str | None = None):
    shipment = shipments[id]
    if content:
        shipment["content"] = content
    if weight:
        shipment["weight"] = weight
    if status:
        shipment["weight"] = status
    
    shipment[id] = shipment
    return shipment

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
