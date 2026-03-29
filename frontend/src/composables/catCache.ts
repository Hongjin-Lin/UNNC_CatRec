import type { CatProfile } from '@/api/index'

// Simple in-memory cache for cat profiles fetched from the list page.
// Allows self-profile to render immediately without waiting for a network request.
const cache = new Map<string, CatProfile>()

export function setCatCache(cat: CatProfile) {
  cache.set(cat.id, cat)
}

export function getCatCache(id: string): CatProfile | undefined {
  return cache.get(id)
}
