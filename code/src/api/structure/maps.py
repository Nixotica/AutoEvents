from typing import List


class MapPool:
    def __init__(self, maps: List[int]):
        self._maps = maps

    def maps(self) -> List[int]:
        return self._maps
