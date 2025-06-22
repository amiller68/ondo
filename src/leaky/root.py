from typing import Optional

import httpx


async def fetch_root_hash(base_url: str) -> Optional[str]:
    """
    Fetch the current root hash from leaky API.

    Args:
        base_url: The base URL of the leaky API

    Returns:
        The root hash string if successful, None otherwise
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/v0/root")
            if response.status_code == 200:
                data = response.json()
                return data.get("hash")
            return None
    except Exception:
        return None
