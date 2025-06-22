# Ondo API Documentation

## API Structure

All API endpoints are prefixed with `/api/v0/` and return either JSON or HTML components depending on the request headers.

### Blog API

- `GET /api/v0/blog/posts` - Get list of blog posts (returns HTML component)
- `GET /api/v0/blog/posts/{category}/{name}` - Get single blog post (returns HTML component)

### Gallery API

- `GET /api/v0/gallery/items` - Get gallery items grid (returns HTML component)
- `GET /api/v0/gallery/items/{category}/{name}` - Get single gallery item (returns HTML component)

### Music API

- `GET /api/v0/music/content` - Get music tracks table (returns HTML component)

### Cache API

- `GET /api/v0/cache/stats` - Get cache statistics
- `POST /api/v0/cache/invalidate` - Invalidate cache entries (optional pattern parameter)

## ISR (Incremental Static Regeneration)

All content endpoints implement ISR with:
- 1 hour TTL (3600 seconds)
- 60 second stale-while-revalidate window
- Automatic invalidation based on leaky API root hash changes

## Response Types

The API endpoints use `ComponentResponseHandler` which:
- Returns JSON when `HX-Request` header is absent
- Returns HTML components when `HX-Request` header is present (HTMX requests)