class Vector2:
    def __init__(self, _x: int | None, _y: int | None) -> None:
        self.x = _x if _x is not None else 0
        self.y = _y if _y is not None else 0
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
