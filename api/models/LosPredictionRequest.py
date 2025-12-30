from typing import Literal, Optional

import matplotlib.pyplot as plt
from pydantic import BaseModel, Field

AVAILABLE_COLORMAPS = plt.colormaps()


class LosPredictionRequest(BaseModel):
    # Transmitter
    tx_lat: float = Field(
        ge=-90, le=90, description="Transmitter latitude in degrees (-90 to 90)"
    )
    tx_lon: float = Field(
        ge=-180, le=180, description="Transmitter longitude in degrees (-180 to 180)"
    )
    tx_height: float = Field(
        1, ge=1, description="Transmitter height above ground in meters (>= 1 m)"
    )
    tx_power: float = Field(gt=0, description="Transmitter power in dBm (>= 1 dBm)")
    tx_gain: float = Field(1, ge=0, description="Transmitter antenna gain in dB (>= 0)")
    tx_loss: Optional[float] = Field(
        0.0, ge=0, description="TX loss in dB (default: 0.0)"
    )
    frequency_mhz: float = Field(
        868.5, ge=20, le=30000, description="Operating frequency in MHz (20-30000 MHz)"
    )

    # Receiver
    rx_lat: float = Field(
        ge=-90, le=90, description="Receiver latitude in degrees (-90 to 90)"
    )
    rx_lon: float = Field(
        ge=-180, le=180, description="Receiver longitude in degrees (-180 to 180)"
    )
    rx_height: float = Field(
        1, ge=1, description="Receiver height above ground in meters (>= 1 m)"
    )
    rx_gain: float = Field(1, ge=0, description="Receiver antenna gain in dB (>= 0)")
    rx_loss: float = Field(0, ge=0, description="Receiver system loss in dB (>= 0)")

    # Environment
    ground_dielectric: Optional[float] = Field(
        15.0, ge=1, description="Ground dielectric constant (default: 15.0)"
    )
    ground_conductivity: Optional[float] = Field(
        0.005, ge=0, description="Ground conductivity in S/m (default: 0.005)"
    )
    atmosphere_bending: Optional[float] = Field(
        301.0,
        ge=0,
        description="Atmospheric bending constant in N-units (default: 301.0)",
    )
    radio_climate: Literal[
        "equatorial",
        "continental_subtropical",
        "maritime_subtropical",
        "desert",
        "continental_temperate",
        "maritime_temperate_land",
        "maritime_temperate_sea",
    ] = Field(
        "continental_temperate",
        description="Radio climate, e.g., 'equatorial', 'continental_temperate' (default: 'continental_temperate')",
    )
    polarization: Literal["horizontal", "vertical"] = Field(
        "vertical",
        description="Signal polarization, 'horizontal' or 'vertical' (default: 'vertical')",
    )
    clutter_height: float = Field(
        0, ge=0, description="Ground clutter height in meters (>= 0)"
    )

    # Simulation options
    situation_fraction: Optional[float] = Field(
        50,
        gt=1,
        le=100,
        description="Percentage of locations within the modeled area where the signal prediction is expected to be valid (default 50).",
    )
    time_fraction: Optional[float] = Field(
        90,
        gt=1,
        le=100,
        description="Percentage of times where the signal prediction is expected to be valid (default 90).",
    )
    high_resolution: bool = Field(
        False,
        description="Use optional 1-arcsecond / 30 meter resolution terrain tiles instead of the default 3-arcsecond / 90 meter (default: False).",
    )
    itm_model: bool = Field(
        True,
        description="Include ITM model instead of newer ITWOM (default: True).",
    )
