from math import pi
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Fluid Flow Analysis System",
    description="Simple API for estimating pressure loss in a straight pipe using the Darcy-Weisbach equation.",
    version="1.0.0",
)


class CalculationInput(BaseModel):
    length_m: float = Field(..., gt=0, description="Pipe length in meters")
    diameter_m: float = Field(..., gt=0, description="Inner diameter in meters")
    flow_rate_m3s: float = Field(..., gt=0, description="Volumetric flow rate in m^3/s")
    density_kgm3: float = Field(997.0, gt=0, description="Fluid density in kg/m^3")
    viscosity_pas: float = Field(0.001, gt=0, description="Dynamic viscosity in Pa*s")
    friction_factor_mode: Literal["auto", "manual"] = "auto"
    manual_friction_factor: float | None = Field(
        default=None, gt=0, description="Used only when friction_factor_mode='manual'"
    )


class CalculationResult(BaseModel):
    area_m2: float
    velocity_ms: float
    reynolds_number: float
    flow_regime: str
    friction_factor: float
    pressure_drop_pa: float
    pressure_drop_kpa: float


def calculate_area(diameter_m: float) -> float:
    return pi * diameter_m**2 / 4


def calculate_velocity(flow_rate_m3s: float, area_m2: float) -> float:
    return flow_rate_m3s / area_m2


def calculate_reynolds(density_kgm3: float, velocity_ms: float, diameter_m: float, viscosity_pas: float) -> float:
    return density_kgm3 * velocity_ms * diameter_m / viscosity_pas


def estimate_friction_factor(reynolds_number: float) -> tuple[float, str]:
    if reynolds_number < 2300:
        return 64 / reynolds_number, "laminar"
    if reynolds_number < 4000:
        return 0.3164 / (reynolds_number ** 0.25), "transitional"
    return 0.3164 / (reynolds_number ** 0.25), "turbulent"


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/calculate", response_model=CalculationResult)
def calculate(data: CalculationInput) -> CalculationResult:
    area = calculate_area(data.diameter_m)
    velocity = calculate_velocity(data.flow_rate_m3s, area)
    reynolds = calculate_reynolds(data.density_kgm3, velocity, data.diameter_m, data.viscosity_pas)

    if reynolds <= 0:
        raise HTTPException(status_code=400, detail="Invalid Reynolds number.")

    if data.friction_factor_mode == "manual":
        if data.manual_friction_factor is None:
            raise HTTPException(
                status_code=400,
                detail="manual_friction_factor is required when friction_factor_mode='manual'.",
            )
        friction_factor = data.manual_friction_factor
        if reynolds < 2300:
            regime = "laminar"
        elif reynolds < 4000:
            regime = "transitional"
        else:
            regime = "turbulent"
    else:
        friction_factor, regime = estimate_friction_factor(reynolds)

    pressure_drop_pa = friction_factor * (data.length_m / data.diameter_m) * (data.density_kgm3 * velocity**2 / 2)

    return CalculationResult(
        area_m2=area,
        velocity_ms=velocity,
        reynolds_number=reynolds,
        flow_regime=regime,
        friction_factor=friction_factor,
        pressure_drop_pa=pressure_drop_pa,
        pressure_drop_kpa=pressure_drop_pa / 1000,
    )
