from prometheus_client import Counter, generate_latest
from fastapi import APIRouter, Response

router = APIRouter()

requests_counter = Counter("tracker_requests_total", "Total HTTP requests")

@router.get("/metrics")
def get_metrics():
    return Response(generate_latest(), media_type="text/plain")
