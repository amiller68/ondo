from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import httpx
from ..utils import parse_date

class GalleryImage(BaseModel):
    name: str
    created_at: datetime
    cid: str
    base_url: str = Field(exclude=True)

    def get_url(self, thumbnail: bool = False) -> str:
        """Get the URL for the image, optionally as thumbnail"""
        suffix = "?thumbnail=true" if thumbnail else ""
        return f"{self.base_url}/gallery/{self.name}{suffix}"

    @classmethod
    async def read_all(cls, base_url: str) -> List["GalleryImage"]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/gallery?deep=true")

            if response.status_code != 200:
                return []

            items = response.json()
            images = []

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

                    # Remove leading slashes from name
                    clean_name = name.lstrip('/')

                    images.append(
                        cls(
                            name=clean_name,
                            created_at=created_at,
                            cid=item["cid"],
                            base_url=base_url,
                        )
                    )
                except (KeyError, ValueError):
                    continue

            return sorted(images, key=lambda x: x.created_at, reverse=True)

    @classmethod
    async def read_one(cls, base_url: str, category: str, name: str) -> Optional["GalleryImage"]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/gallery/{category}")
            if response.status_code != 200:
                return None

            items = response.json()
            print(f"JESUS FUCKING CHRIST READING gallery_item: {items}")
            full_path = f"{name}"
            image_item = next(
                (
                    item
                    for item in items
                    if not item.get("is_dir") and item["path"] == full_path
                ),
                None,
            )

            if not image_item or not image_item.get("object"):
                return None

            data = image_item["object"]
            if "created_at" not in data:
                return None

            created_at = parse_date(data["created_at"])
            if created_at is None:
                return None

            

            return cls(
                name=f"{category}/{name}",
                created_at=created_at,
                cid=image_item["cid"],
                base_url=base_url,
            )