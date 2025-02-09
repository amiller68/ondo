from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field
import httpx


def parse_date(date_value: Any) -> Optional[datetime]:
    if isinstance(date_value, list) and len(date_value) >= 9:
        try:
            # New format has [year, month, day, hour, minute, second, microsecond, _, _]
            return datetime.strptime(
                f"{date_value[0]} {date_value[1]}",
                "%Y %j",
            )
        except (ValueError, IndexError):
            return None
    return None


class FileObject(BaseModel):
    cid: str
    path: str
    is_dir: bool
    object: Optional[dict]


class BlogPostMetadata(BaseModel):
    title: str
    description: str


class BlogPost(BaseModel):
    name: str
    title: str
    description: str
    created_at: datetime
    content: Optional[str] = None

    @classmethod
    async def read_all(cls, base_url: str) -> List["BlogPost"]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/writing")

            if response.status_code != 200:
                return []

            items = response.json()
            posts = []

            print(items)

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

                    posts.append(
                        cls(
                            name=name,
                            title=data["properties"]["title"],
                            description=data["properties"]["description"],
                            created_at=created_at,
                        )
                    )
                except (KeyError, ValueError):
                    continue

            return sorted(posts, key=lambda x: x.created_at, reverse=True)

    @classmethod
    async def read_one(cls, base_url: str, name: str) -> Optional["BlogPost"]:
        async with httpx.AsyncClient() as client:
            # Get metadata
            meta_response = await client.get(f"{base_url}/writing")
            if meta_response.status_code != 200:
                return None

            items = meta_response.json()
            post_item = next(
                (
                    item
                    for item in items
                    if not item.get("is_dir") and item["path"] == name
                ),
                None,
            )

            if not post_item or not post_item.get("object"):
                return None

            data = post_item["object"]
            if "properties" not in data or "created_at" not in data:
                return None

            created_at = parse_date(data["created_at"])
            if created_at is None:
                return None

            # Get content
            content_response = await client.get(f"{base_url}/writing/{name}?html=true")
            if content_response.status_code != 200:
                return None

            return cls(
                name=name,
                title=data["properties"]["title"],
                description=data["properties"]["description"],
                created_at=created_at,
                content=content_response.text,
            )


class GalleryImage(BaseModel):
    name: str
    created_at: datetime
    cid: str
    base_url: str = Field(exclude=True)

    def get_url(self, thumbnail: bool = False) -> str:
        """Get the URL for the image, optionally as thumbnail"""
        suffix = "?thumbnail=true" if thumbnail else ""
        return f"{self.base_url}/visual/{self.name}{suffix}"

    @classmethod
    async def read_all(cls, base_url: str) -> List["GalleryImage"]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/visual")

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

                    images.append(
                        cls(
                            name=name,
                            created_at=created_at,
                            cid=item["cid"],
                            base_url=base_url,
                        )
                    )
                except (KeyError, ValueError):
                    continue

            return sorted(images, key=lambda x: x.created_at, reverse=True)

    @classmethod
    async def read_one(cls, base_url: str, name: str) -> Optional["GalleryImage"]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/visual")
            if response.status_code != 200:
                return None

            items = response.json()
            image_item = next(
                (
                    item
                    for item in items
                    if not item.get("is_dir") and item["path"] == name
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
                name=name,
                created_at=created_at,
                cid=image_item["cid"],
                base_url=base_url,
            )


class AudioTrack(BaseModel):
    name: str
    created_at: datetime
    cid: str
    base_url: str = Field(exclude=True)

    def get_url(self) -> str:
        """Get the URL for the audio track"""
        return f"{self.base_url}/audio/{self.name}"

    @classmethod
    async def read_all(cls, base_url: str) -> List["AudioTrack"]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/audio")

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
                            cid=item["cid"],
                            base_url=base_url,
                        )
                    )
                except (KeyError, ValueError):
                    continue

            return sorted(tracks, key=lambda x: x.created_at, reverse=True)

    @classmethod
    async def read_one(cls, base_url: str, name: str) -> Optional["AudioTrack"]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/audio")
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
                cid=track_item["cid"],
                base_url=base_url,
            )
