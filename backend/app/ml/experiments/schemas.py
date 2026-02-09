from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import uuid

class ExperimentLog(BaseModel):
    """
    Schema for an ML Experiment Log Entry.
    Ensures consistent data structure for all experiments.
    """
    experiment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    model_name: str
    model_version: str
    dataset_version: str
    task: str  # e.g., "classification", "ocr_finetuning", "routing_eval"
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    metrics: Dict[str, float] = Field(default_factory=dict)
    output_artifacts: Optional[str] = None
    git_commit_hash: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "experiment_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2023-10-27T10:00:00",
                "model_name": "resnet18",
                "model_version": "v1.0",
                "dataset_version": "doc_class_v2",
                "task": "classification",
                "hyperparameters": {"epochs": 10, "lr": 0.001},
                "metrics": {"accuracy": 0.95, "loss": 0.12},
                "git_commit_hash": "a1b2c3d"
            }
        }
