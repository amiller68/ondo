from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import httpx
from ..utils import parse_date

class ListeningEntry(BaseModel):
    name: str
    title: str
    artist: str
    album_art_url: str
    tags: List[str]
    created_at: datetime
    content: Optional[str] = None

    @classmethod
    async def read_all(cls, base_url: str) -> List["ListeningEntry"]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/music/listening")
            if response.status_code != 200:
                return []

            items = response.json()
            entries = []

            for item in items:
                try:
                    if not isinstance(item, dict) or item.get("is_dir", True):
                        continue

                    name = item["path"]
                    data = item.get("object", {})

                    if not data or "properties" not in data or "created_at" not in data:
                        continue

                    created_at = parse_date(data["created_at"])
                    if created_at is None:
                        continue

                    entries.append(
                        cls(
                            name=name,
                            title=data["properties"]["title"],
                            artist=data["properties"]["artist"],
                            album_art_url=data["properties"]["album_art_url"],
                            tags=data["properties"].get("tags", []),
                            created_at=created_at,
                        )
                    )
                except (KeyError, ValueError):
                    continue

            return sorted(entries, key=lambda x: x.created_at, reverse=True)

    @classmethod
    async def read_one(cls, base_url: str, name: str) -> Optional["ListeningEntry"]:
        async with httpx.AsyncClient() as client:
            meta_response = await client.get(f"{base_url}/music/listening")
            if meta_response.status_code != 200:
                return None

            items = meta_response.json()
            entry_item = next(
                (
                    item
                    for item in items
                    if not item.get("is_dir") and item["path"] == name
                ),
                None,
            )

            if not entry_item or not entry_item.get("object"):
                return None

            data = entry_item["object"]
            if "properties" not in data or "created_at" not in data:
                return None

            created_at = parse_date(data["created_at"])
            if created_at is None:
                return None

            # Get content
            content_response = await client.get(f"{base_url}/music/listening/{name}?html=true")
            if content_response.status_code != 200:
                return None

            return cls(
                name=name,
                title=data["properties"]["title"],
                artist=data["properties"]["artist"],
                album_art_url=data["properties"]["album_art_url"],
                tags=data["properties"].get("tags", []),
                created_at=created_at,
                content=content_response.text,
            ) 