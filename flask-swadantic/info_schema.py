from dataclasses import dataclass
from typing import Optional


@dataclass
class InfoSchema:
    title: str
    summary: Optional[str] = None
    description: Optional[str] = None
    version: str = "1.0.0"
