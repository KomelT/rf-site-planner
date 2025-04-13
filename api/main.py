from logging import INFO, basicConfig, getLogger
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.CoveragePredictionRequest import CoveragePredictionRequest
from redis import StrictRedis
from services.geoserver import store_tiff_in_geoserver
from services.splat import Splat

basicConfig(level=INFO)
logger = getLogger(__name__)

# Initialize Redis client for binary data
redis_client = StrictRedis(host="redis", port=6379, decode_responses=False)

# Initialize SPLAT service
splat_service = Splat(splat_path="/usr/bin")

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_coverage(task_id: str, request: CoveragePredictionRequest):
    try:
        logger.info(f"Starting SPLAT! coverage prediction for task {task_id}.")
        geotiff_data = splat_service.coverage_prediction(request)

        store_tiff_in_geoserver(task_id, geotiff_data)

        redis_client.setex(f"{task_id}:status", 3600, "completed")
        logger.info(f"Task {task_id} marked as completed.")
    except Exception as e:
        logger.error(f"Error in SPLAT! task {task_id}: {e}")
        redis_client.setex(f"{task_id}:status", 3600, "failed")
        redis_client.setex(f"{task_id}:error", 3600, str(e))
        raise


@app.post("/predict")
async def predict(
    payload: CoveragePredictionRequest, background_tasks: BackgroundTasks
) -> JSONResponse:
    task_id = str(uuid4())
    redis_client.setex(f"{task_id}:status", 3600, "processing")
    background_tasks.add_task(run_coverage, task_id, payload)
    return JSONResponse({"task_id": task_id})


@app.get("/task/status/{task_id}")
async def get_status(task_id: str):
    status = redis_client.get(f"{task_id}:status")
    if not status:
        logger.warning(f"Task {task_id} not found in Redis.")
        return JSONResponse({"error": "Task not found"}, status_code=404)

    status = status.decode("utf-8")
    if status == "completed":
        return JSONResponse({"status": "completed"})
    elif status == "failed":
        error = redis_client.get(f"{task_id}:error")
        return JSONResponse({"status": "failed", "error": error.decode("utf-8")})

    return JSONResponse({"status": status})
