from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.scenarios.replay import DeterministicReplay

app = FastAPI(title="Mock Governance Simulation Framework API")

class ScenarioRequest(BaseModel):
    scenario_name: str
    organization_id: str
    seed: Optional[int] = None

@app.get("/")
def health_check():
    return {"status": "ok", "service": "mock_simulation"}

@app.get("/scenarios")
def list_scenarios() -> List[str]:
    return list(ScenarioRegistry.list_scenarios().keys())

@app.post("/scenarios/run")
def run_scenario(req: ScenarioRequest) -> Dict[str, Any]:
    try:
        if req.scenario_name not in ScenarioRegistry.list_scenarios():
            raise HTTPException(status_code=404, detail=f"Scenario '{req.scenario_name}' not found.")

        seed_to_use = req.seed if req.seed is not None else 42
        return DeterministicReplay.run_scenario(req.scenario_name, req.organization_id, seed=seed_to_use)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
