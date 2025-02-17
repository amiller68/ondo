from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import httpx
from ..utils import parse_date

class BlogPostMetadata(BaseModel):
    title: str
    description: str

class BlogPost(BaseModel):
    name: str
    title: str
    description: str
    created_at: datetime
    content: Optional[str] = None
    category: str = "thoughts"  # Default category

    @classmethod
    async def read_all(cls, base_url: str, category: Optional[str] = None) -> List["BlogPost"]:
        async with httpx.AsyncClient() as client:
            # Get posts for specific category
            url = f"{base_url}/blog"
            if category:
                url = f"{url}/{category}"
            
            response = await client.get(url)
            if response.status_code != 200:
                return []

            items = response.json()
            posts = []

            for item in items:
                try:
                    if not isinstance(item, dict) or item.get("is_dir", True):
                        continue

                    name = item["path"]  # This is just the filename now, not the full path
                    data = item.get("object", {})

                    if not data or "properties" not in data or "created_at" not in data:
                        continue

                    created_at = parse_date(data["created_at"])
                    if created_at is None:
                        continue

                    posts.append(
                        cls(
                            name=name,  # Just use the filename
                            title=data["properties"]["title"],
                            description=data["properties"]["description"],
                            created_at=created_at,
                            category=category or "thoughts",  # Use the provided category
                        )
                    )
                except (KeyError, ValueError):
                    continue

            return sorted(posts, key=lambda x: x.created_at, reverse=True)

    @classmethod
    async def read_one(cls, base_url: str, name: str) -> Optional["BlogPost"]:
        # Extract category from name
        parts = name.split("/")
        if len(parts) != 2:
            return None
        
        category, post_name = parts
        
        async with httpx.AsyncClient() as client:
            # Get metadata from category endpoint
            meta_response = await client.get(f"{base_url}/blog/{category}")
            if meta_response.status_code != 200:
                return None

            items = meta_response.json()
            post_item = next(
                (
                    item
                    for item in items
                    if not item.get("is_dir") and item["path"] == post_name  # Match just the filename
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
            content_response = await client.get(f"{base_url}/blog/{category}/{post_name}?html=true")
            if content_response.status_code != 200:
                return None

            return cls(
                name=post_name,  # Just use the filename
                title=data["properties"]["title"],
                description=data["properties"]["description"],
                created_at=created_at,
                content=content_response.text,
                category=category,
            ) 