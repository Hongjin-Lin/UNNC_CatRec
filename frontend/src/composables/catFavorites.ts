const STORAGE_KEY = 'favorite_cat_ids'

function load(): string[] {
  try {
    const raw = uni.getStorageSync(STORAGE_KEY)
    if (Array.isArray(raw)) return raw.map(String)
    if (typeof raw === 'string' && raw) {
      const parsed = JSON.parse(raw)
      return Array.isArray(parsed) ? parsed.map(String) : []
    }
  } catch {}
  return []
}

function save(ids: string[]) {
  try {
    uni.setStorageSync(STORAGE_KEY, ids)
  } catch {}
}

export function getFavoriteCatIds(): string[] {
  return load()
}

export function isFavoriteCat(id: string): boolean {
  return load().includes(String(id))
}

export function toggleFavoriteCat(id: string): boolean {
  const target = String(id)
  const ids = load()
  const idx = ids.indexOf(target)
  if (idx >= 0) {
    ids.splice(idx, 1)
    save(ids)
    return false
  }
  ids.push(target)
  save(ids)
  return true
}
