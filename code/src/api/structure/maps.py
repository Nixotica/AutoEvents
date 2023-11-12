from __future__ import annotations
from typing import List


class Map:
    def __init__(self, uuid: str):
        self._uuid = uuid


# def get_random_map_uid() -> str:
#     url = "https://trackmania.exchange/mapsearch2/search?api=on&random=1"
#     headers = {
#         "Content-Type": "application/json",
#         "User-Agent": "Get-random-map / nixotica@gmail.com"
#     }
#     max_author_time = 70000
#     min_author_time = 30000
#     actual_author_time = 0
#     while actual_author_time > max_author_time or actual_author_time < min_author_time:
#         map_info = requests.post(url, headers=headers).json()
#         actual_author_time = map_info["results"][0]["AuthorTime"]
#     return map_info["results"][0]["TrackUID"]


class PlaylistMap(Map):
    def __init__(
        self,
        uuid: str,
        position: int,
    ):
        super().__init__(uuid)

        self._position = position

    def __eq__(self, other: PlaylistMap) -> bool:
        return self._uuid == other._uuid and self._position == other._position

    @staticmethod
    def _list_from_campaign_response(response: List[dict]) -> List[PlaylistMap]:
        """
        Given the payload response from a campaign, return the list of PlaylistMaps:

        :param response: The response from a campaign, e.g.
            [
                {
                    "id": 314741,
                    "position": 0,
                    "mapUid": "tknxMmzHqPOImrE7FWNzzdvCia2"
                },
                ...
            ]
        :returns: List of playlist maps
        """
        playlist_maps = []
        for map_info in response:
            playlist_maps.append(
                PlaylistMap(
                    map_info["mapUid"],
                    map_info["position"],
                )
            )
        return playlist_maps
