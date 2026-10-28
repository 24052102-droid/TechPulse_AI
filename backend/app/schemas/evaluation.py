from typing import Dict, Any
from pydantic import BaseModel


class EvaluationReportResponse(BaseModel):
    report_date: str
    phase: str
    models: Dict[str, Any]
    classification: Dict[str, Any]
