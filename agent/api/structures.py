from __future__ import annotations

from .constants import CommandType, StatusCode, TowerType, EnemyType


class Vector2:
    """兩個整數組成的二維向量。"""

    def __init__(self, _x: int | None, _y: int | None) -> None:
        self.x = _x if _x is not None else 0
        """x 座標，若傳 None 則設為 0。"""

        self.y = _y if _y is not None else 0
        """y 座標，若傳 None 則設為 0。"""

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class ApiException(Exception):
    """代表一次失敗的 API 呼叫後回傳的錯誤，附帶關於錯誤來源、錯誤種類、說明文字的資訊。"""

    def __init__(self, source_fn: CommandType, code: StatusCode, what: str) -> None:
        super().__init__(
            f"API call {source_fn.name}({source_fn.value}) fails with status code {code.name}({code.value}): {what}"
        )
        self.source_fn = source_fn
        """見 class CommandType。"""

        self.code = code
        """見 class StatusCode。"""

        self.what = what
        """完整錯誤訊息內容。"""


class Tower:
    """關於一座防禦塔的屬性、數值資訊。"""

    def __init__(
        self,
        _type: TowerType,
        position: Vector2,
        level_a: int,
        level_b: int,
        aim: bool,
        anti_air: bool,
        reload: int,
        range: int,
        damage: int,
        bullet_effect: str,
    ) -> None:
        self.type = _type
        """塔的型別，見 class TowerType"""

        self.position = position
        """塔的座標，地圖左上角為 (0, 0)。"""

        self.level_a = level_a
        """塔的等級分支一。"""

        self.level_b = level_b
        """
        塔的等級分支二。  
        (level_a, level_b) =
        - (1, 1): 1
        - (2, 1): 2a
        - (1, 2): 2b
        - (3, 1): 3a
        - (1, 3): 3b
        """

        self.aim = aim
        """是否能瞄準敵人。"""

        self.anti_air = anti_air
        """是否能攻擊空中單位。"""

        self.reload = reload
        """每分鐘攻擊次數。"""

        self.range = range
        """瞄準範圍半徑。"""

        self.damage = damage
        """攻擊傷害。"""

        self.bullet_effect = bullet_effect
        """
        特殊效果。
        - none: 無
        - fire: 燃燒的持續傷害
        - freeze: 緩速
        - deep_freeze: 強化緩速
        - knockback: 擊退 knockback_resist = False 的敵人
        - far_knockback: 擊退所有敵人
        """

    @classmethod
    def from_dict(cls, data: dict) -> "Tower | None":
        if not data:
            return None
        return cls(
            _type=TowerType(data["type"]),
            position=Vector2(data["position"]["x"], data["position"]["y"]),
            level_a=data["level_a"],
            level_b=data["level_b"],
            aim=data["aim"],
            anti_air=data["anti_air"],
            reload=data["reload"],
            range=data["range"],
            damage=data["damage"],
            bullet_effect=data["bullet_effect"],
        )

    def __str__(self) -> str:
        return f"Tower(type={self.type.name}, position={self.position}, level_a={self.level_a}, level_b={self.level_b})"

    def __repr__(self) -> str:
        return self.__str__()


class Enemy:
    """關於一個敵人的屬性、數值資訊。"""

    def __init__(
        self,
        type: EnemyType,
        position: Vector2,
        progress_ratio: float,
        income_impact: int,
        health: int,
        max_health: int,
        damage: int,
        max_speed: int,
        flying: bool,
        knockback_resist: bool,
        kill_reward: int,
    ) -> None:
        self.type = type
        """敵人型別。"""

        self.position = position
        """敵人位置。"""

        self.progress_ratio = progress_ratio
        """敵人走完的路程比例。"""

        self.health = health
        """敵人當前生命值。"""

        self.max_health = max_health
        """敵人最大生命值。"""

        self.flying = flying
        """是不是空中單位。"""

        self.damage = damage
        """對塔能造成的傷害。"""

        self.max_speed = max_speed
        """最高速度。"""

        self.knockback_resist = knockback_resist
        """擊退抵抗，若為 true 則不會被擊退。"""

        self.kill_reward = kill_reward
        """擊殺該敵人會獲得的獎勵。"""

        self.income_impact = income_impact
        """派兵到對手場地後對 income 的影響，可正可負。"""

    @classmethod
    def from_dict(cls, data: dict) -> "Enemy":
        return cls(
            type=EnemyType(data["type"]),
            position=Vector2(data["position"]["x"], data["position"]["y"]),
            progress_ratio=data["progress_ratio"],
            income_impact=data["income_impact"],
            health=data["health"],
            max_health=data["max_health"],
            damage=data["damage"],
            max_speed=data["max_speed"],
            flying=data["flying"],
            knockback_resist=data["knockback_resist"],
            kill_reward=data["kill_reward"],
        )

    def __str__(self) -> str:
        return f"Enemy(type={self.type.name}, position={self.position}, progress ratio={self.progress_ratio}, health={self.health}/{self.max_health})"

    def __repr__(self) -> str:
        return self.__str__()
