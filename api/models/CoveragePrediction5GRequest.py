from typing import List, Optional

from pydantic import BaseModel, Field

from models.CoveragePredictionRequest import CoveragePredictionRequest


class CoverageBeamRequest(BaseModel):
    azimuth: float = Field(
        ge=0,
        le=360,
        description="Beam azimuth in degrees (0-360, where 0 is north).",
    )
    beam_width: float = Field(
        gt=0,
        le=360,
        description="Horizontal beam width in degrees (0-360).",
    )
    name: Optional[str] = Field(
        None,
        description="Optional beam name used in API response.",
    )


class CoveragePrediction5GRequest(CoveragePredictionRequest):
    beams: List[CoverageBeamRequest] = Field(
        min_length=1,
        description="List of 5G beams to simulate. Each beam is simulated separately.",
    )
