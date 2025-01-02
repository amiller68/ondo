from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field
import httpx


def parse_date(date_value: Any) -> Optional[datetime]:
    if isinstance(date_value, list) and len(date_value) >= 2:
        try:
            return datetime.strptime(f"{date_value[0]} {date_value[1]}", "%Y %j")
        except (ValueError, IndexError):
            return None
    return None


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

            for item in items:
                try:
                    if not (isinstance(item, list) and len(item) > 1):
                        continue

                    name = item[0]
                    data = item[1][1]

                    if not (
                        isinstance(data, dict)
                        and "metadata" in data
                        and "created_at" in data
                    ):
                        continue

                    created_at = parse_date(data["created_at"])
                    if created_at is None:
                        continue

                    posts.append(
                        cls(
                            name=name,
                            title=data["metadata"]["title"],
                            description=data["metadata"]["description"],
                            created_at=created_at,
                        )
                    )
                except (IndexError, KeyError, ValueError):
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
                    if isinstance(item, list) and len(item) > 0 and item[0] == name
                ),
                None,
            )

            if not post_item or not (
                len(post_item) > 1
                and isinstance(post_item[1], list)
                and len(post_item[1]) > 1
                and post_item[1][1]
                and isinstance(post_item[1][1], dict)
                and "metadata" in post_item[1][1]
                and "created_at" in post_item[1][1]
            ):
                return None

            data = post_item[1][1]
            created_at = parse_date(data["created_at"])
            if created_at is None:
                return None

            # Get content
            content_response = await client.get(f"{base_url}/writing/{name}?html=true")
            if content_response.status_code != 200:
                return None

            return cls(
                name=name,
                title=data["metadata"]["title"],
                description=data["metadata"]["description"],
                created_at=created_at,
                content=content_response.text,
            )


class GalleryImage(BaseModel):
    name: str
    created_at: datetime
    base_url: str = Field(exclude=True)  # Add base_url but exclude from serialization

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
                    if not (isinstance(item, list) and len(item) > 1):
                        continue

                    name = item[0]
                    data = item[1][1]

                    if not (isinstance(data, dict) and "created_at" in data):
                        continue

                    created_at = parse_date(data["created_at"])
                    if created_at is None:
                        continue

                    images.append(
                        cls(name=name, created_at=created_at, base_url=base_url)
                    )
                except (IndexError, KeyError, ValueError):
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
                    if isinstance(item, list) and len(item) > 0 and item[0] == name
                ),
                None,
            )

            if not image_item or not (
                len(image_item) > 1
                and isinstance(image_item[1], list)
                and len(image_item[1]) > 1
                and image_item[1][1]
                and isinstance(image_item[1][1], dict)
                and "created_at" in image_item[1][1]
            ):
                return None

            data = image_item[1][1]
            created_at = parse_date(data["created_at"])
            if created_at is None:
                return None

            return cls(name=name, created_at=created_at, base_url=base_url)
