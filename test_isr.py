#!/usr/bin/env python3
"""Test ISR registration"""

import asyncio
from src.server.isr import isr_registry

# Force import of pages to trigger registrations
from src.server.pages import blog, gallery, music

async def main():
    print("ISR Routes registered:")
    for route in isr_registry._routes:
        print(f"  - {route.path} (template: {route.template})")
        if route.slug_fetcher:
            print(f"    Dynamic route with slug fetcher")
        else:
            print(f"    Static route")
    
    print(f"\nTotal routes: {len(isr_registry._routes)}")

if __name__ == "__main__":
    asyncio.run(main())