import hashlib
from typing import Any

class IDGenerator:
    """
    Deterministic ID generation for replay consistency.
    Never uses UUID4 randomness in the simulation path.
    """
    @staticmethod
    def generate_id(seed: int, entity_type: str, *args: Any) -> str:
        """
        Derives an ID from the scenario seed, entity type, and additional args.
        """
        raw_str = f"{seed}:{entity_type}:{':'.join(map(str, args))}"
        hashed = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
        return f"{entity_type.lower()}_{hashed[:12]}"
