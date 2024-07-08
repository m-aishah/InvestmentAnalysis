from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class InvestmentOptionsSchema(BaseModel):
    budget_min: int = Field(0, title="Minimum Budget", description="Minimum budget for property investment")
    budget_max: int = Field(..., title="Maximum Budget", description="Maximum budget for property investment")
    location: Optional[str] = Field(None, title="Location", description="Location preference for property investment")
    size_min: Optional[int] = Field(0, title="Minimum Size", description="Minimum property size in square meters", ge=0)
    size_max: Optional[int] = Field(None, title="Maximum Size", description="Maximum property size in square meters")
    bedrooms_min: Optional[int] = Field(0, title="Minimum Bedrooms", description="Minimum number of bedrooms", ge=0)
    bedrooms_max: Optional[int] = Field(None, title="Maximum Bedrooms", description="Maximum number of bedrooms")
    bathrooms_min: Optional[float] = Field(0, title="Minimum Bathrooms", description="Minimum number of bathrooms", ge=0)
    bathrooms_max: Optional[float] = Field(None, title="Maximum Bathrooms", description="Maximum number of bathrooms")
    family_size: Optional[int] = Field(None, title="Family Size", description="Number of family members")
    property_type: Optional[str] = Field(None, title="Property Type", description="Type of property (e.g., house, apartment)")
    sort_by: Optional[str] = Field(None, title="Sort By", description="Sort the results by a specific field (e.g., price, size)")

def custom_json_schema(model):
    schema = model.schema()
    properties_formatted = {
        k: {
            "title": v.get("title"),
            "type": v.get("type")
        } for k, v in schema["properties"].items()
    }
    return {
        "type": "object",
        "default": {},
        "properties": properties_formatted,
        "required": schema.get("required", [])
    }