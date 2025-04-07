
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
from .family_tree_member import FamilyTreeMember

allowed_outputs = ["pdf", "png", "jpg", "svg", "jpeg", "json"]

class IncorrectTreeType(Exception):
    pass


class TreeType(Enum):
    QUICK = "quick"
    FAMILY = "family"
    CUSTOM = "custom"
    CIRCLE = "circle"
    FULL = "full"
    def __eq__(self, other):
        return self.value == other



@dataclass
class GeneratorOptions:
    image_format = "-Tjpg"
    output_path = None
    with_images = True
    span: Optional[Dict[int, List[FamilyTreeMember]]] = None
    highlight = False
    radius = None
    font = "Arial"

    def __init__(self, image_format=None, output_path=None, with_images=True, span=None, highlight=False, radius=None, font =None):
        self.image_format = image_format or "jpg"
        self.output_path = output_path
        self.with_images = with_images
        self.span = span
        self.highlight = highlight
        self.radius = radius
        self.font = font or "Arial"
        self.validate_file_format()

    def validate_file_format(self):
        if self.image_format not in allowed_outputs:
            raise ValueError(f"Invalid image format: {self.image_format}. Allowed formats are: {allowed_outputs}")
