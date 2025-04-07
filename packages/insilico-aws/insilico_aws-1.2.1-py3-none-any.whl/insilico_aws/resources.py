
from typing import Optional, Any


from pydantic import BaseModel, model_validator


class Algorithm(BaseModel):
    name: str
    region_name: str
    arn: Optional[str] = None
    account_id: Optional[str] = None
    supported_regions: dict[str, str]
    training_instance_type: list[str]
    training_data_required: Optional[list[str]] = None
    inference_instance_type: list[str]
    training_max_run_hours: int
    training_volume_size_gb: int
    training_parameters: list[dict[str, Any]]
    inference_parameters: list[dict[str, Any]]

    @model_validator(mode='after')
    def validate_resource(self):
        if self.arn:
            return self
        if self.region_name not in self.supported_regions:
            raise ValueError(
                f"Algorithm {self.name} is not available in {self.region_name}, "
                f"choose one of: {' '.join(self.supported_regions.keys())}"
            )
        if not self.account_id:
            self.account_id = self.supported_regions[self.region_name]
        self.arn = (
            f"arn:aws:sagemaker:{self.region_name}:"
            f"{self.account_id}:"
            f"algorithm/{self.name}"
        )
        return self
