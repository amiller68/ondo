from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import httpx
from ..utils import parse_date

class AudioTrack(BaseModel):
    name: str
    created_at: datetime
    base_url: str = Field(exclude=True)

    def get_url(self) -> str:
        return f"{self.base_url}/music/me/{self.name}"

    @classmethod
    async def read_all(cls, base_url: str) -> List["AudioTrack"]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/music/me")
            if response.status_code != 200:
                return []

            items = response.json()
            tracks = []

            for item in items:
                try:
                    if not isinstance(item, dict) or item.get("is_dir", True):
                        continue

                    name = item["path"]
                    data = item.get("object", {})

                    if not data or "created_at" not in data:
                        continue

                    created_at = parse_date(data["created_at"])
                    if created_at is None:
                        continue

                    tracks.append(
                        cls(
                            name=name,
                            created_at=created_at,
                            base_url=base_url,
                        )
                    )
                except (KeyError, ValueError):
                    continue

            return sorted(tracks, key=lambda x: x.created_at, reverse=True)

    @classmethod
    async def read_one(cls, base_url: str, name: str) -> Optional["AudioTrack"]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/music/me")
            if response.status_code != 200:
                return None

            items = response.json()
            track_item = next(
                (
                    item
                    for item in items
                    if not item.get("is_dir") and item["path"] == name
                ),
                None,
            )

            if not track_item or not track_item.get("object"):
                return None

            data = track_item["object"]
            if "created_at" not in data:
                return None

            created_at = parse_date(data["created_at"])
            if created_at is None:
                return None

            return cls(
                name=name,
                created_at=created_at,
                base_url=base_url,
            ) 