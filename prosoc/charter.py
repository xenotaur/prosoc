import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

# Path to the charter YAML file
CHARTER_YAML_PATH = Path(__file__).parent / "charter.yml"

class ExampleSet(BaseModel):
    positive: List[str] = Field(default_factory=list)
    negative: List[str] = Field(default_factory=list)

class CharterPrinciple(BaseModel):
    id: str
    name: str
    description: str
    severity: Optional[str] = None
    examples: ExampleSet

class Charter(BaseModel):
    principles: List[CharterPrinciple]

def load_charter(path: Path = CHARTER_YAML_PATH) -> List[CharterPrinciple]:
    """
    Load and validate the YAML-formatted charter from disk.

    Args:
        path (Path): Path to the YAML charter file.

    Returns:
        List of validated CharterPrinciple objects.

    Raises:
        ValidationError: if the charter does not conform to the expected schema.
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    charter = Charter(**raw)
    return charter.principles

# Example usage:
# try:
#     charter_rules = load_charter()
#     for rule in charter_rules:
#         print(rule.id, rule.name)
# except ValidationError as e:
#     print("Charter validation failed:", e)
