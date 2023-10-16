from typing import Optional
from pydantic import BaseModel


class Food(BaseModel):
    id: int
    search_term: str
    name: str
    category: str
    subcategory: str
    brand: str
    item_url: str
    cals_per_g: float
    fat_per_g: float
    carb_per_g: float
    prot_per_g: float
    serving_size: Optional[float] = None
    max_servings: Optional[int] = None


class Problem(BaseModel):
    target_kcals: float
    max_fat_pct: float
    min_prot_pct: float
    foods: list[Food]
    penalty_protein: float
    penalty_fat: float
    penalty_kcals: float
