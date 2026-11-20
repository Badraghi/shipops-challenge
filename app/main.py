"""ShipOps API. Database-dependent behavior uses PostgreSQL via app.db."""

import logging
import os
import time

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, field_validator

from .db import ItemStore, get_store

logger = logging.getLogger("shipops")

app = FastAPI(title="ShipOps API", version="1.0.0")

REQUESTS = Counter(
    "shipops_http_requests_total",
    "HTTP requests handled by the service",
    ["method", "route", "status"],
)
ERRORS = Counter(
    "shipops_http_failed_requests_total",
    "HTTP requests with 4xx or 5xx responses",
    ["method", "route", "status"],
)
LATENCY = Histogram(
    "shipops_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "route"],
)


class ItemIn(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be empty")
        return value


class ItemOut(BaseModel):
    id: int
    name: str


@app.middleware("http")
async def measure_requests(request: Request, call_next):
    started = time.perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        route = request.scope.get("route")
        # Use the route template, never a concrete /items/123 value (cardinality safety).
        path = getattr(route, "path", "unmatched")
        if path != "/metrics":
            labels = (request.method, path, str(status_code))
            REQUESTS.labels(*labels).inc()
            LATENCY.labels(request.method, path).observe(time.perf_counter() - started)
            if status_code >= 400:
                ERRORS.labels(*labels).inc()


@app.get("/healthz")
def healthz():
    # Liveness MUST NOT touch the database.
    return {"status": "alive"}


@app.get("/readyz")
def readyz(store: ItemStore = Depends(get_store)):
    try:
        store.ping()
    except Exception as exc:
        # Do not expose database connection strings or credentials in HTTP errors.
        logger.warning("Readiness failed (%s)", type(exc).__name__)
        raise HTTPException(status_code=503, detail="database unavailable") from None
    return {"status": "ready"}


@app.get("/version")
def version():
    return {"version": os.getenv("RELEASE_VERSION", "dev")}


@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(item: ItemIn, store: ItemStore = Depends(get_store)):
    try:
        item_id, stored_name = store.create_item(item.name)
    except Exception as exc:
        logger.warning("Item creation failed (%s)", type(exc).__name__)
        raise HTTPException(status_code=503, detail="database unavailable") from None
    return ItemOut(id=item_id, name=stored_name)


@app.get("/items/{item_id}", response_model=ItemOut)
def read_item(item_id: int, store: ItemStore = Depends(get_store)):
    if item_id < 1:
        raise HTTPException(status_code=404, detail="item not found")
    try:
        item = store.get_item(item_id)
    except Exception as exc:
        logger.warning("Item retrieval failed (%s)", type(exc).__name__)
        raise HTTPException(status_code=503, detail="database unavailable") from None
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return ItemOut(id=item[0], name=item[1])


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
