from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class HeatEquationInput(BaseModel):
    alpha: float = Field(..., gt=0, description="Коэффициент температуропроводности")
    length: float = Field(..., gt=0, description="Длина области")
    nx: int = Field(..., gt=2, description="Число точек по пространству")
    nt: int = Field(..., gt=1, description="Число шагов по времени")
    dt: float = Field(..., gt=0, description="Шаг по времени")
    initial_condition: List[float] = Field(..., min_items=1, description="Начальное условие")
    boundary_conditions: Dict[str, float] = Field(..., description="Граничные условия")

class Schrodinger2DInput(BaseModel):
    radius: float = Field(5.0, gt=0, description="Радиус круговой полости")
    points: int = Field(100, gt=10, le=1000, description="Число точек сетки на одно измерение")
    mass: float = Field(1.0, gt=0, description="Масса частицы в атомных единицах")
    potential: Optional[str] = Field(
        None,
        description="Тип потенциала: 'circle' (по умолчанию) или 'box'"
    )

class SolutionResponse(BaseModel):
    success: bool = Field(..., description="Флаг успешного выполнения")
    energies: List[float] = Field(..., description="Собственные значения энергии")
    message: Optional[str] = Field(None, description="Сообщение об ошибке")
